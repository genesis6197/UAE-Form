# Email settings

All outgoing emails use the English `assets/Email_format.docx` body and English subject, regardless of the form language. The PDF attachment remains `assets/Overview.pdf`.

## CC recipients

Set `EMAIL_CC` in your hosting service environment settings. Default: `mohit@assiduus.in`.
Use comma-separated addresses for multiple recipients. Set the value to an empty string to disable CC. Duplicates and the primary recipient are omitted. Invalid addresses stop the send and produce a configuration error in the server log.

## Signature

Set `SIGNATURE_NAME`, `SIGNATURE_TITLE`, and `SIGNATURE_EMAIL` in the hosting environment. Defaults are Mohit Gadam, COO -Global Operations, and mohit@assiduusglobal.com. Existing environment overrides take precedence; update or remove old SIGNATURE_* values when deploying this signature. The name also controls the sender display name; `SENDER_EMAIL` still controls the sending mailbox.

For changes to logos, links, formatting, or the disclaimer, edit `assets/email_signature.html`. Keep the `{{signature_name}}`, `{{signature_title}}`, and `{{signature_email}}` placeholders where the corresponding values should appear.

On Render, save environment changes and restart/redeploy the service. Commit and deploy template changes. The template is read each time an email is built. No application-code edit is needed for CC or signature updates.

The retained `assets/email_translations.json` is inactive and is not loaded by the server.

## Company/brand name in the email

The form's optional "Company/Brand" field is inserted wherever `<<company>>` appears in `assets/Email_format.docx` (currently twice: "meeting the team from <<company>>" and "help <<company>> reach customers"). If the field is left blank, the email falls back to "your brand". The value is HTML-escaped before insertion.
