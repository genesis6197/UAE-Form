"""
Contact Form -> Personalised Email Sender
─────────────────────────────────────────────────────────────────────────────
Receives submissions from the Assiduus Global contact form (name, email,
phone), saves each one as a row in a Google Sheet, builds the email body
from your Word template (same <<greeting>> / <<company>> placeholder
system as your batch script), addresses the person by their first name
only (normalised to Capitalised-first-letter), attaches a file, and
sends it.

Submissions are saved to Google Sheets rather than a local file because
Render's free tier has no persistent disk — anything written to disk is
wiped on every restart/redeploy. See the "Google Sheets setup" comment
further down for the one-time setup steps.

Sends via the Gmail API (https://developers.google.com/gmail/api) using
OAuth2, instead of SendGrid or raw SMTP. This means email is sent as the
real hr@assiduus.in Gmail/Workspace inbox, with no third-party mail
provider involved.

One-time setup (do this once, locally — see get_refresh_token.py for the
full walkthrough):
    pip install -r requirements.txt
    pip install google-auth-oauthlib   # only needed for the one-time script
    python get_refresh_token.py
This prints a refresh token. Set the following as environment variables
(never hardcode credentials):
    Windows (PowerShell):
        setx GOOGLE_OAUTH_CLIENT_ID     "xxxxx.apps.googleusercontent.com"
        setx GOOGLE_OAUTH_CLIENT_SECRET "xxxxxxxxxxxxxxxxxxxx"
        setx GOOGLE_OAUTH_REFRESH_TOKEN "1//xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        setx SENDER_EMAIL               "hr@assiduus.in"
    macOS/Linux:
        export GOOGLE_OAUTH_CLIENT_ID="xxxxx.apps.googleusercontent.com"
        export GOOGLE_OAUTH_CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxx"
        export GOOGLE_OAUTH_REFRESH_TOKEN="1//xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        export SENDER_EMAIL="hr@assiduus.in"

The refresh token lets the server mint new short-lived access tokens on
its own at send time — no repeated logins, no browser needed at runtime.
It keeps working indefinitely unless you revoke access at
https://myaccount.google.com/permissions.

Run:
    python app.py
    -> server listens on http://localhost:5000
─────────────────────────────────────────────────────────────────────────────
"""

import os
from html import escape, unescape
import re
import base64
import logging
import sys
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

import mammoth
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from googleapiclient.discovery import build as build_google_service
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Config ─────────────────────────────────────────────────────────────────

# Credentials are read from environment variables, not hardcoded.
# See get_refresh_token.py for how to obtain these one time.
GOOGLE_OAUTH_CLIENT_ID     = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_OAUTH_REFRESH_TOKEN = os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN")
SENDER_EMAIL               = os.environ.get("SENDER_EMAIL")  # e.g. hr@assiduus.in

GMAIL_TOKEN_URI = "https://oauth2.googleapis.com/token"
GMAIL_SCOPES    = ["https://www.googleapis.com/auth/gmail.send"]
EMAIL_SUBJECT   = "Thanks for reaching out to Assiduus Global"

# Files live inside the repo (in /assets) instead of a local Windows path,
# so the exact same code works on your machine AND on Render.
BASE_DIR = Path(__file__).resolve().parent

# Same idea as your batch script: write the email body in Word, save as
# .docx, and type <<greeting>> wherever the salutation should go.
# <<company>> also works if your template uses it.
WORD_BODY_PATH  = BASE_DIR / "assets" / "Email_format.docx"

# File attached to every reply — change to whatever you want to send
ATTACHMENT_PATH = BASE_DIR / "assets" / "Overview.pdf"

# Allow the form (served from a different origin, e.g. a file:// preview
# or a different domain) to call this API. Lock this down to your real
# domain before going to production.
ALLOWED_ORIGIN = "*"

LOG_FILE_PATH = "form_email.log"

# Every submission gets appended as a new row in this Google Sheet instead
# of a local file — Render's free tier has no persistent disk, so anything
# written to disk disappears on every restart/redeploy. A Google Sheet
# lives outside Render entirely, so it survives that just fine and your
# team can view submissions live without downloading anything.
#
# Setup (one-time):
# 1. Go to https://console.cloud.google.com, create/select a project.
# 2. Enable the "Google Sheets API" and "Google Drive API" for it
#    (APIs & Services > Library > search each > Enable).
# 3. APIs & Services > Credentials > Create Credentials > Service Account.
#    Give it any name, no roles needed. Create it.
# 4. Open the new service account > Keys > Add Key > Create new key > JSON.
#    This downloads a .json file — keep it secret, never commit it.
# 5. Create a Google Sheet (or use an existing one). Add a header row:
#    timestamp_utc | name | email | phone | company | message | form
#    The last column tags every row with which regional form it came from,
#    for internal reference. See FORM_LABEL below.
# 6. Share that Sheet with the service account's email address (looks like
#    xxxxx@xxxxx.iam.gserviceaccount.com — find it inside the JSON file's
#    "client_email" field). Give it "Editor" access.
# 7. Set these environment variables on Render (Settings > Environment):
#      GOOGLE_SERVICE_ACCOUNT_JSON = <paste the ENTIRE contents of the
#                                     downloaded .json file as one line>
#      GOOGLE_SHEET_ID             = <the long ID from the sheet's URL,
#                                     e.g. docs.google.com/spreadsheets/d/
#                                     THIS_PART/edit>
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
GOOGLE_SHEET_WORKSHEET = os.environ.get("GOOGLE_SHEET_WORKSHEET", "Sheet1")
CSV_FIELDS = ["timestamp_utc", "name", "email", "phone", "company", "message", "form"]

# Written into the "form" column of every saved row, so submissions from each
# regional deployment stay tellable apart in one sheet. Override per deployment
# with the FORM_LABEL environment variable.
FORM_LABEL = os.environ.get("FORM_LABEL", "UAE")

# Email settings: override these in your hosting environment.
EMAIL_CC = os.environ.get("EMAIL_CC", "Hardik.jaisingh@assiduus.in")
SIGNATURE_NAME = os.environ.get("SIGNATURE_NAME", "Hardik Jaisingh")
SIGNATURE_TITLE = os.environ.get("SIGNATURE_TITLE", "Chief of Staff")
SIGNATURE_EMAIL = os.environ.get("SIGNATURE_EMAIL", "Hardik.jaisingh@assiduus.in")
SIGNATURE_PATH = BASE_DIR / "assets" / "email_signature.html"


def load_signature():
    """Read the editable signature for each email; escape configurable text."""
    signature = SIGNATURE_PATH.read_text(encoding="utf-8")
    for key, value in (("name", SIGNATURE_NAME), ("title", SIGNATURE_TITLE), ("email", SIGNATURE_EMAIL)):
        signature = signature.replace("{{signature_" + key + "}}", escape(value, quote=True))
    return signature


def get_cc_recipients(to_address):
    """Accept comma/semicolon-separated addresses; reject malformed settings."""
    recipients = []
    seen = {to_address.lower()}
    for value in re.split(r"[,;]", EMAIL_CC):
        address = value.strip()
        if not address:
            continue
        if "\r" in address or "\n" in address or not EMAIL_RE.fullmatch(address):
            raise ValueError("EMAIL_CC must contain comma-separated email addresses.")
        if address.lower() not in seen:
            recipients.append(address)
            seen.add(address.lower())
    return recipients


# ── Logging ────────────────────────────────────────────────────────────────

logger = logging.getLogger("form_email")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s", "%Y-%m-%d %H:%M:%S")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(fmt)
logger.addHandler(ch)

if LOG_FILE_PATH:
    fh = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

# ── Helpers ────────────────────────────────────────────────────────────────

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def format_first_name(full_name: str) -> str:
    """
    Takes whatever the form sent ('Jordan Lee', 'JORDAN', 'jordan lee') and
    returns just the first name with only its first letter capitalised:
    'JORDAN LEE' -> 'Jordan', 'jordan lee' -> 'Jordan'.
    """
    full_name = (full_name or "").strip()
    if not full_name:
        return "there"
    first = full_name.split()[0]
    return first.capitalize()  # 'JORDAN' -> 'Jordan', 'jORDAN' -> 'Jordan'


def load_word_body(path, logger):
    """Same loader as your batch script — converts the .docx to HTML."""
    doc_path = Path(path)
    if not doc_path.exists():
        logger.critical("Word body file not found: %s", doc_path.resolve())
        raise FileNotFoundError(doc_path)

    with open(doc_path, "rb") as f:
        result = mammoth.convert_to_html(f)

    for msg in result.messages:
        logger.warning("Mammoth [%s]: %s", msg.type, msg.message)

    logger.info("Word body loaded and converted: %s", doc_path.name)
    return result.value


def substitute_placeholders(html, greeting, company_display, logger):
    """
    Identical logic to your batch script: replaces <<greeting>> and
    <<company>>, including cases where Mammoth splits a placeholder across
    multiple HTML tags.
    """
    html = re.sub(r'&lt;&lt;\s*greeting\s*&gt;&gt;', lambda m: greeting,        html, flags=re.IGNORECASE)
    html = re.sub(r'&lt;&lt;\s*company\s*&gt;&gt;',  lambda m: company_display, html, flags=re.IGNORECASE)
    html = re.sub(r'<<\s*greeting\s*>>',              lambda m: greeting,        html, flags=re.IGNORECASE)
    html = re.sub(r'<<\s*company\s*>>',               lambda m: company_display, html, flags=re.IGNORECASE)

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["p", "li", "td", "div", "span", "h1", "h2", "h3", "h4"]):
        plain = tag.get_text()
        changed = False

        if re.search(r'<<\s*greeting\s*>>', plain, re.IGNORECASE):
            new_plain = re.sub(r'<<\s*greeting\s*>>', lambda m: unescape(greeting), plain, flags=re.IGNORECASE)
            tag.clear(); tag.append(new_plain); changed = True

        if re.search(r'<<\s*company\s*>>', plain, re.IGNORECASE):
            new_plain = re.sub(r'<<\s*company\s*>>', lambda m: unescape(company_display), tag.get_text(), flags=re.IGNORECASE)
            tag.clear(); tag.append(new_plain); changed = True

        if changed:
            logger.debug("Placeholder substituted in tag <%s>: %s", tag.name, tag.get_text()[:80])

    result = str(soup)
    remaining = re.findall(r'<<\s*(?:greeting|company)\s*>>', result, re.IGNORECASE)
    if remaining:
        logger.warning("Could not substitute placeholder(s): %s", remaining)

    return result


_gspread_client = None
_worksheet = None


def get_worksheet():
    """Lazily connects to Google Sheets on first use and caches the
    worksheet handle for subsequent calls (avoids re-authenticating on
    every single form submission)."""
    global _gspread_client, _worksheet
    if _worksheet is not None:
        return _worksheet

    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set.")
    if not GOOGLE_SHEET_ID:
        raise RuntimeError("GOOGLE_SHEET_ID environment variable is not set.")

    import json
    creds_info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(creds_info, scopes=scopes)
    _gspread_client = gspread.authorize(credentials)

    spreadsheet = _gspread_client.open_by_key(GOOGLE_SHEET_ID)
    try:
        _worksheet = spreadsheet.worksheet(GOOGLE_SHEET_WORKSHEET)
    except gspread.exceptions.WorksheetNotFound:
        _worksheet = spreadsheet.sheet1

    # Add the header row if the sheet is currently empty.
    if not _worksheet.get_all_values():
        _worksheet.append_row(CSV_FIELDS)

    return _worksheet


def save_submission(full_name: str, email: str, phone: str, company: str = "", message: str = ""):
    """Appends one row per submission to the configured Google Sheet."""
    row = [
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        full_name,
        email,
        phone or "",
        company or "",
        message or "",
        FORM_LABEL,
    ]
    worksheet = get_worksheet()
    worksheet.append_row(row, value_input_option="USER_ENTERED")
    logger.info("Submission saved to Google Sheet")


# Load the Word template once at startup, same as the batch script loads it
# once before looping over the Excel file.
try:
    WORD_HTML = load_word_body(WORD_BODY_PATH, logger)
except FileNotFoundError:
    WORD_HTML = None
    logger.critical(
        "Server starting WITHOUT a body template — every /submit call will "
        "fail until WORD_BODY_PATH points to a real .docx file."
    )


def build_email_message(to_address: str, full_name: str, phone: str, language: str = "en", company: str = "") -> dict:
    """Builds a base64url-encoded RFC 2822 MIME message in the format the
    Gmail API's messages.send expects: {"raw": "<base64url string>"}."""
    if WORD_HTML is None:
        raise RuntimeError("Email body template failed to load — check WORD_BODY_PATH.")

    # Emails are English regardless of the form language (including older clients).
    language = "en"
    first_name = format_first_name(full_name)
    greeting = f"Dear {escape(first_name)}"
    company_display = escape(" ".join((company or "").split())) or "your brand"
    personalised_html = substitute_placeholders(WORD_HTML, greeting, company_display, logger)
    subject = EMAIL_SUBJECT
    signature_html = load_signature()

    full_html = f"""\
<!DOCTYPE html>
<html lang="{language}">
<head><meta charset="utf-8"></head>
<body style="font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#000000;margin:0;padding:0;">
  {personalised_html}
  {signature_html}
</body>
</html>
"""

    message = MIMEMultipart("mixed")
    message["To"] = to_address
    cc_recipients = get_cc_recipients(to_address)
    if cc_recipients:
        message["Cc"] = ", ".join(cc_recipients)
    message["From"] = f"{SIGNATURE_NAME} <{SENDER_EMAIL}>"
    message["Subject"] = subject
    message["Content-Language"] = language
    message.attach(MIMEText(full_html, "html", "utf-8"))

    attachment_path = Path(ATTACHMENT_PATH)
    if attachment_path.exists():
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header(
            "Content-Disposition", "attachment", filename=attachment_path.name
        )
        message.attach(part)
    else:
        logger.warning("Attachment not found at %s — sending without it.", attachment_path)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
    return {"raw": raw}


_gmail_service = None


def get_gmail_service():
    """Lazily builds and caches a Gmail API client, refreshing the access
    token from the stored OAuth refresh token as needed. The refresh token
    itself never expires (unless revoked), so this needs no user
    interaction at runtime."""
    global _gmail_service
    if _gmail_service is not None:
        return _gmail_service

    missing = [
        name for name, val in (
            ("GOOGLE_OAUTH_CLIENT_ID", GOOGLE_OAUTH_CLIENT_ID),
            ("GOOGLE_OAUTH_CLIENT_SECRET", GOOGLE_OAUTH_CLIENT_SECRET),
            ("GOOGLE_OAUTH_REFRESH_TOKEN", GOOGLE_OAUTH_REFRESH_TOKEN),
            ("SENDER_EMAIL", SENDER_EMAIL),
        ) if not val
    ]
    if missing:
        raise RuntimeError(
            "Missing environment variable(s): " + ", ".join(missing) +
            ". See get_refresh_token.py for one-time setup."
        )

    creds = OAuthCredentials(
        token=None,
        refresh_token=GOOGLE_OAUTH_REFRESH_TOKEN,
        token_uri=GMAIL_TOKEN_URI,
        client_id=GOOGLE_OAUTH_CLIENT_ID,
        client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
        scopes=GMAIL_SCOPES,
    )
    creds.refresh(GoogleAuthRequest())  # mints a fresh access token now

    _gmail_service = build_google_service("gmail", "v1", credentials=creds)
    return _gmail_service


def send_email(to_address: str, full_name: str, phone: str, language: str = "en", company: str = ""):
    service = get_gmail_service()
    message_body = build_email_message(to_address, full_name, phone, language, company)

    try:
        service.users().messages().send(userId="me", body=message_body).execute()
    except Exception as exc:
        # Surface Gmail's own error so misconfiguration (revoked token,
        # missing scope, etc.) is easy to diagnose from the logs.
        logger.error("Gmail API error sending to %s: %s", to_address, exc)
        raise RuntimeError(f"Gmail API send failed: {exc}") from exc


# ── Flask app ────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app, resources={r"/submit": {"origins": ALLOWED_ORIGIN}})


@app.route("/", methods=["GET"])
def contact_form():
    """Serves the contact form itself, so the same Render service hosts
    both the page and the API — no separate hosting needed for mobile
    testing."""
    return app.send_static_file("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}
    full_name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    company = (data.get("company") or "").strip()[:200]
    message = (data.get("message") or "").strip()[:2000]
    language = "en"  # Form translations do not change the outgoing email.

    if not full_name:
        return jsonify(ok=False, error="Name is required."), 400
    if not email or not EMAIL_RE.match(email):
        return jsonify(ok=False, error="A valid email is required."), 400

    logger.info("Submission received: %s <%s> phone=%s", full_name, email, phone or "—")

    # Save first, independent of whether the email send succeeds — a lead
    # you have on file beats one lost to a flaky email send.
    try:
        save_submission(full_name, email, phone, company, message)
    except Exception as exc:
        logger.error("Failed to save submission for %s: %s", email, exc)

    try:
        send_email(email, full_name, phone, language, company)
    except Exception as exc:
        logger.error("Failed to send to %s: %s", email, exc)
        return jsonify(ok=False, error="Could not send the email. Please try again."), 500

    logger.info("Email sent to %s", email)
    return jsonify(ok=True)


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    # Render sets the PORT env var and expects the app to bind to it.
    # Locally this just falls back to 5000, same as before.
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
