// All text shown by the form lives here. Language changes do not reset entered data.
// Examples (names, phone, email) use UAE conventions: +971 mobile numbers and
// .ae addresses. The U+2066/U+2069 pair around the phone number is an LTR
// isolate — without it the number groups reorder inside Arabic and Urdu text.
const translations = {
  ar: {
    languageLabel: 'اللغة', pageTitle: 'Assiduus Global — تواصل معنا',
    tagline: 'نساعد العلامات التجارية على البيع والتوسّع عالميًا عبر أسرع الطرق وأكثرها فعالية من حيث التكلفة.',
    headline: 'يسعدنا التعرّف عليك',
    subtext: 'شاركنا بعض التفاصيل وسيتواصل معك فريقنا خلال يوم عمل واحد.',
    firstName: 'الاسم الأول', lastName: 'اسم العائلة', email: 'البريد الإلكتروني', phone: 'رقم الهاتف', optional: '(اختياري)',
    firstNamePlaceholder: 'أحمد', lastNamePlaceholder: 'المنصوري', emailPlaceholder: 'you@company.ae',
    phonePlaceholder: 'مثال: ⁦+971 50 123 4567⁩', submit: 'إرسال', submitting: 'جارٍ الإرسال…',
    company: 'الشركة/العلامة التجارية', companyPlaceholder: 'اسم شركتك أو علامتك التجارية', message: 'الرسالة', messagePlaceholder: 'كيف يمكننا مساعدتك؟',
    privacy: 'لن نستخدم هذه البيانات إلا للرد على استفسارك.',
    successTitle: 'شكرًا لك — تم إرسال طلبك.', successBody: 'سيتواصل معك فريقنا عبر البيانات التي شاركتها.',
    requiredFirst: 'يرجى إدخال اسمك الأول.', requiredLast: 'يرجى إدخال اسم العائلة.',
    invalidEmail: 'يرجى إدخال بريد إلكتروني صالح.',
    sendError: 'تعذّر إرسال البريد الإلكتروني. يرجى المحاولة مرة أخرى.',
    genericError: 'حدث خطأ ما. يرجى المحاولة مرة أخرى.'
  },
  en: {
    languageLabel: 'Language', pageTitle: 'Assiduus Global — Get in touch',
    tagline: 'Helping brands sell and scale globally through the fastest, most cost-effective route.',
    headline: "Let's get acquainted",
    subtext: 'Share a few details and our team will follow up within one business day.',
    firstName: 'First name', lastName: 'Last name', email: 'Email', phone: 'Phone', optional: '(optional)',
    firstNamePlaceholder: 'Ahmed', lastNamePlaceholder: 'Al Mansouri', emailPlaceholder: 'you@company.ae',
    phonePlaceholder: 'e.g. +971 50 123 4567', submit: 'Submit', submitting: 'Submitting…',
    company: 'Company/Brand', companyPlaceholder: 'Your company or brand', message: 'Message', messagePlaceholder: 'How can we help?',
    privacy: "We'll only use these details to respond to your enquiry.",
    successTitle: "Thanks — it's on its way.", successBody: 'Our team will reach out using the details you shared.',
    requiredFirst: 'Please enter your first name.', requiredLast: 'Please enter your last name.',
    invalidEmail: 'Please enter a valid email address.',
    sendError: 'Could not send the email. Please try again.',
    genericError: 'Something went wrong. Please try again.'
  },
  hi: {
    languageLabel: 'भाषा', pageTitle: 'Assiduus Global — संपर्क करें',
    tagline: 'हम ब्रांड्स को सबसे तेज़ और किफ़ायती रास्ते से दुनिया भर में बिक्री और विस्तार करने में मदद करते हैं।',
    headline: 'आइए, परिचय करें',
    subtext: 'कुछ जानकारी साझा करें, हमारी टीम एक कार्यदिवस के भीतर आपसे संपर्क करेगी।',
    firstName: 'पहला नाम', lastName: 'उपनाम', email: 'ईमेल', phone: 'फ़ोन नंबर', optional: '(वैकल्पिक)',
    firstNamePlaceholder: 'आरव', lastNamePlaceholder: 'शर्मा', emailPlaceholder: 'you@company.ae',
    phonePlaceholder: 'जैसे +971 50 123 4567', submit: 'भेजें', submitting: 'भेजा जा रहा है…',
    company: 'कंपनी/ब्रांड', companyPlaceholder: 'आपकी कंपनी या ब्रांड', message: 'संदेश', messagePlaceholder: 'हम आपकी किस तरह मदद कर सकते हैं?',
    privacy: 'इन जानकारियों का उपयोग हम केवल आपकी पूछताछ का उत्तर देने के लिए करेंगे।',
    successTitle: 'धन्यवाद — आपका संदेश भेज दिया गया है।', successBody: 'आपके द्वारा दी गई जानकारी के ज़रिए हमारी टीम आपसे संपर्क करेगी।',
    requiredFirst: 'कृपया अपना पहला नाम दर्ज करें।', requiredLast: 'कृपया अपना उपनाम दर्ज करें।',
    invalidEmail: 'कृपया एक मान्य ईमेल पता दर्ज करें।',
    sendError: 'ईमेल नहीं भेजा जा सका। कृपया पुनः प्रयास करें।',
    genericError: 'कुछ गड़बड़ हो गई। कृपया पुनः प्रयास करें।'
  },
  ur: {
    languageLabel: 'زبان', pageTitle: 'Assiduus Global — رابطہ کریں',
    tagline: 'ہم برانڈز کو تیز ترین اور کم لاگت والے راستے سے دنیا بھر میں فروخت اور ترقی میں مدد دیتے ہیں۔',
    headline: 'آئیے تعارف کرتے ہیں',
    subtext: 'چند تفصیلات شیئر کریں، ہماری ٹیم ایک کاروباری دن کے اندر آپ سے رابطہ کرے گی۔',
    firstName: 'پہلا نام', lastName: 'خاندانی نام', email: 'ای میل', phone: 'فون نمبر', optional: '(اختیاری)',
    firstNamePlaceholder: 'علی', lastNamePlaceholder: 'خان', emailPlaceholder: 'you@company.ae',
    phonePlaceholder: 'مثلاً ⁦+971 50 123 4567⁩', submit: 'بھیجیں', submitting: 'بھیجا جا رہا ہے…',
    company: 'کمپنی/برانڈ', companyPlaceholder: 'آپ کی کمپنی یا برانڈ', message: 'پیغام', messagePlaceholder: 'ہم آپ کی کیا مدد کر سکتے ہیں؟',
    privacy: 'ہم یہ تفصیلات صرف آپ کے استفسار کا جواب دینے کے لیے استعمال کریں گے۔',
    successTitle: 'شکریہ — آپ کا پیغام بھیج دیا گیا ہے۔', successBody: 'ہماری ٹیم آپ کی دی گئی تفصیلات پر رابطہ کرے گی۔',
    requiredFirst: 'براہِ کرم اپنا پہلا نام درج کریں۔', requiredLast: 'براہِ کرم اپنا خاندانی نام درج کریں۔',
    invalidEmail: 'براہِ کرم درست ای میل ایڈریس درج کریں۔',
    sendError: 'ای میل نہیں بھیجی جا سکی۔ دوبارہ کوشش کریں۔',
    genericError: 'کچھ غلط ہو گیا۔ دوبارہ کوشش کریں۔'
  },
  ml: {
    languageLabel: 'ഭാഷ', pageTitle: 'Assiduus Global — ബന്ധപ്പെടുക',
    tagline: 'ഏറ്റവും വേഗമേറിയതും ചെലവു കുറഞ്ഞതുമായ വഴിയിലൂടെ ബ്രാൻഡുകൾക്ക് ആഗോളതലത്തിൽ വിൽക്കാനും വളരാനും ഞങ്ങൾ സഹായിക്കുന്നു.',
    headline: 'നമുക്ക് പരിചയപ്പെടാം',
    subtext: 'കുറച്ച് വിവരങ്ങൾ പങ്കുവയ്ക്കൂ, ഒരു പ്രവൃത്തി ദിവസത്തിനകം ഞങ്ങളുടെ ടീം ബന്ധപ്പെടും.',
    firstName: 'പേര്', lastName: 'കുടുംബപ്പേര്', email: 'ഇമെയിൽ', phone: 'ഫോൺ നമ്പർ', optional: '(നിർബന്ധമല്ല)',
    firstNamePlaceholder: 'അനീഷ്', lastNamePlaceholder: 'നായർ', emailPlaceholder: 'you@company.ae',
    phonePlaceholder: 'ഉദാ: +971 50 123 4567', submit: 'അയയ്ക്കുക', submitting: 'അയയ്ക്കുന്നു…',
    company: 'കമ്പനി/ബ്രാൻഡ്', companyPlaceholder: 'നിങ്ങളുടെ കമ്പനി അല്ലെങ്കിൽ ബ്രാൻഡ്', message: 'സന്ദേശം', messagePlaceholder: 'ഞങ്ങൾക്ക് എങ്ങനെ സഹായിക്കാനാകും?',
    privacy: 'നിങ്ങളുടെ അന്വേഷണത്തിന് മറുപടി നൽകാൻ മാത്രമേ ഈ വിവരങ്ങൾ ഉപയോഗിക്കൂ.',
    successTitle: 'നന്ദി — സന്ദേശം അയച്ചു.', successBody: 'നിങ്ങൾ നൽകിയ വിവരങ്ങൾ വഴി ഞങ്ങളുടെ ടീം ബന്ധപ്പെടും.',
    requiredFirst: 'ദയവായി നിങ്ങളുടെ പേര് നൽകുക.', requiredLast: 'ദയവായി കുടുംബപ്പേര് നൽകുക.',
    invalidEmail: 'സാധുവായ ഒരു ഇമെയിൽ വിലാസം നൽകുക.',
    sendError: 'ഇമെയിൽ അയയ്ക്കാനായില്ല. വീണ്ടും ശ്രമിക്കുക.',
    genericError: 'എന്തോ പിഴവ് സംഭവിച്ചു. വീണ്ടും ശ്രമിക്കുക.'
  }
};

// Scripts that read right to left.
const rtlLanguages = ['ar', 'ur'];
// Browser codes that should land on one of the languages above.
const languageAliases = { ps: 'ur', ckb: 'ar', fa: 'ar', mr: 'hi', ne: 'hi' };

const languageSelect = document.getElementById('languageSelect');
let currentLanguage = 'en';

function t(key) {
  return translations[currentLanguage][key] || translations.en[key] || key;
}

function setLanguage(language) {
  currentLanguage = translations[language] ? language : 'en';
  languageSelect.value = currentLanguage;
  document.documentElement.lang = currentLanguage;
  document.documentElement.dir = rtlLanguages.indexOf(currentLanguage) > -1 ? 'rtl' : 'ltr';
  document.title = t('pageTitle');
  document.querySelectorAll('[data-i18n]').forEach(function(element) {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(function(element) {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  languageSelect.setAttribute('aria-label', t('languageLabel'));
  const button = document.getElementById('ctaBtn');
  if (button) button.textContent = t(document.getElementById('leadForm').classList.contains('busy') ? 'submitting' : 'submit');
  const error = document.getElementById('formError');
  if (error && error.dataset.errorKey) error.textContent = t(error.dataset.errorKey);
  try { localStorage.setItem('formLanguage', currentLanguage); } catch (_) {}
}

let savedLanguage;
try { savedLanguage = localStorage.getItem('formLanguage'); } catch (_) {}
const rawBrowserLanguage = (navigator.language || '').toLowerCase();
const browserLanguage = languageAliases[rawBrowserLanguage] || languageAliases[rawBrowserLanguage.split('-')[0]] || rawBrowserLanguage.split('-')[0];
setLanguage(savedLanguage || (translations[browserLanguage] ? browserLanguage : 'en'));
languageSelect.addEventListener('change', function() { setLanguage(this.value); });
