"""
ScamShield Multi-Language Localization Module
Provides comprehensive translations for English (en), Marathi (mr), and Hindi (hi).
Includes full HCI checklist localizations for Usability, Accessibility, Feedback,
Reporting, and Learning.
"""

TRANSLATIONS = {
    "en": {
        # Brand & Nav
        "brand_title": "SCAMSHIELD",
        "brand_subtitle": "AI Scam Detection & Risk Assessment",
        "nav_home": "Home",
        "nav_sms": "SMS",
        "nav_email": "Email",
        "nav_url": "URL",
        "nav_phone": "Phone",
        "nav_history": "History",
        "nav_learn": "Learn",
        "nav_report": "Report Scam",
        "skip_to_content": "Skip to main content",

        # Theming & Accessibility Controls
        "theme_toggle": "Toggle Dark / Light Mode",
        "theme_dark": "🌙 Dark",
        "theme_light": "☀️ Light",
        "a11y_dyslexia": "🔤 Dyslexia Font",
        "a11y_contrast": "👁️ High Contrast",

        # Home Page & Onboarding
        "hero_title": "What would you like to check today?",
        "hero_subtitle": "Check suspicious messages, emails, links, and phone calls before you act or click.",
        "card_sms_title": "CHECK SMS",
        "card_sms_desc": "Check a suspicious SMS or WhatsApp message.",
        "card_sms_btn": "Check Message →",
        "card_email_title": "CHECK EMAIL",
        "card_email_desc": "Check an email for suspicious or phishing content.",
        "card_email_btn": "Check Email →",
        "card_url_title": "CHECK URL",
        "card_url_desc": "Check whether a website link appears suspicious.",
        "card_url_btn": "Check Link →",
        "card_phone_title": "CHECK PHONE CALL",
        "card_phone_desc": "Answer a few questions about a suspicious call.",
        "card_phone_btn": "Start Questions →",
        "onboarding_title": "🛡️ New to ScamShield? Quick 3-Step Guide",
        "onboarding_step1": "1. Choose what to check (SMS, Email, URL, or Phone Call).",
        "onboarding_step2": "2. Paste the message text or drop a screenshot.",
        "onboarding_step3": "3. View instant risk evaluation and a clear checklist of what to do.",
        "onboarding_dismiss": "Got it, thanks! ✕",

        # Form Controls & Privacy Banner
        "privacy_tip_title": "Privacy Guard",
        "privacy_tip_desc": "Never paste active OTPs, passwords, or complete credit cards. ScamShield automatically masks sensitive numbers for your safety.",
        "btn_paste": "Paste",
        "btn_clear": "Clear",
        "tab_paste_text": "✏️ Paste Message Text",
        "tab_upload_screenshot": "📷 Upload Screenshot",
        "tab_paste_email": "✏️ Paste Email Details",
        "tab_upload_email_screenshot": "📷 Upload Email Screenshot",
        "tab_paste_url": "✏️ Paste URL Link",
        "tab_upload_url_screenshot": "📷 Upload URL Screenshot",
        "upload_drag_drop": "Click or Drag & Drop Screenshot Here",
        "upload_formats": "Supports PNG, JPG, JPEG, WEBP (Max 16 MB)",
        "upload_remove": "✕ Remove",
        "try_example": "Try an Example:",

        # SMS Page
        "sms_header_title": "Check SMS or WhatsApp Message",
        "sms_header_desc": "Paste the message text or upload a screenshot to check for scams.",
        "sms_label": "Paste the message here:",
        "sms_placeholder": "Example: URGENT: Your bank account is locked. Click http://bit.ly/verify to unlock...",
        "sms_btn": "🔍 Check Message Now",
        "sms_scan_btn": "🔍 Scan Screenshot",

        # Email Page
        "email_header_title": "Check Email Content",
        "email_header_desc": "Paste email details or upload a screenshot to detect phishing and scam attempts.",
        "email_sender_label": "Sender Email Address (Optional):",
        "email_sender_placeholder": "Example: support@service-security-alert.com",
        "email_subject_label": "Email Subject Line:",
        "email_subject_placeholder": "Example: Important: Security Notice Regarding Your Account",
        "email_body_label": "Email Body / Message Text:",
        "email_body_placeholder": "Paste the text of the email here...",
        "email_btn": "🔍 Check Email Now",
        "email_scan_btn": "🔍 Scan Email Screenshot",

        # URL Page
        "url_header_title": "Check Website Link (URL)",
        "url_header_desc": "Paste a website link or upload a screenshot to inspect if it is safe or malicious.",
        "url_label": "Paste the website link (URL) here:",
        "url_placeholder": "Example: https://example.com/login or http://192.168.1.1/claim",
        "url_help": "ScamShield safely inspects the link structure without visiting malicious websites.",
        "url_btn": "🔍 Check Link Safety",
        "url_scan_btn": "🔍 Scan Link Screenshot",

        # Phone Page
        "phone_header_title": "Check a Suspicious Phone Call",
        "phone_header_desc": "Answer these 10 simple questions about what the caller asked you to do.",
        "phone_yes": "YES",
        "phone_no": "NO",
        "phone_btn": "🔍 Calculate Call Scam Risk",

        # Results Page & Explainability
        "result_title": "ScamShield Assessment Result",
        "content_checked": "Content Checked:",
        "ocr_extracted_badge": "Extracted via OCR Screenshot Scanner",
        "risk_score_label": "Estimated Risk Score",
        "why_heading": "🔍 Why Did We Give This Score?",
        "what_heading": "🛡️ What Should You Do Now?",
        "btn_check_another": "🔄 Check Another Item",
        "btn_view_history": "📋 View Scan History",
        "snippet_label": "Analyzed Content Snippet:",
        "sms_display_type": "SMS / WhatsApp Message",
        "email_display_type": "Email Message",
        "url_display_type": "Website Link (URL)",
        "phone_display_type": "Phone Call Assessment",
        "btn_read_aloud": "🔊 Read Aloud",
        "btn_stop_audio": "⏹️ Stop Audio",
        "btn_copy_summary": "📋 Copy Summary",
        "btn_share_warning": "📤 Share Warning",
        "toast_copied": "Summary copied to clipboard!",
        "feedback_title": "Was this assessment helpful?",
        "feedback_yes": "👍 Yes, helpful",
        "feedback_no": "👎 Report incorrect",
        "feedback_thanks": "Thank you for helping improve ScamShield!",
        "disclaimer_result": "Disclaimer: ScamShield uses automated heuristic rules and machine learning models to detect fraud indicators. Always verify directly with official institution channels before taking financial action.",

        # Analyzing Loading Overlay
        "analyzing_title": "Analyzing Content for Fraud Markers...",
        "analyzing_subtitle": "Inspecting text patterns, urgency signals, and security risks...",

        # Risk Labels & Summaries
        "risk_safe": "Potentially Safe",
        "risk_medium": "Suspicious (Medium Risk)",
        "risk_high": "Potential Scam (High Risk)",
        "risk_safe_summary": "This content shows no immediate signs of scam activity, but always remain vigilant.",
        "risk_medium_summary": "This content exhibits some suspicious indicators. Proceed with caution.",
        "risk_high_summary": "High likelihood of scam or phishing attempt. Do not share information or click links.",

        # History Page
        "history_title": "Recent Scan History",
        "history_desc": "Saved locally in your active session. No sensitive data is permanently stored.",
        "history_clear_btn": "🗑️ Clear History",
        "history_empty_title": "No Scans Performed Yet",
        "history_empty_desc": "Check an SMS, Email, URL, or Phone call to see results here.",
        "history_go_home": "Go to Home",
        "history_search_placeholder": "Search history by keyword...",
        "history_filter_all": "All Risk Levels",
        "history_filter_high": "High Risk",
        "history_filter_medium": "Medium Risk",
        "history_filter_safe": "Safe",
        "history_export_csv": "📥 Export CSV",
        "history_print": "🖨️ Print / Save Report",

        # Learn Page
        "learn_header_title": "Scam Awareness & Learning Center",
        "learn_header_desc": "Learn how scammers manipulate victims, spot warning red flags, and test your knowledge.",
        "learn_patterns_title": "Common Scam Tactics & Red Flags",
        "learn_quiz_title": "Test Your Scam Detection Instincts",
        "learn_faq_title": "Frequently Asked Questions (FAQ)",

        # Report Page
        "report_header_title": "Report a Scam & Official Helplines",
        "report_header_desc": "Emergency helplines and quick incident submission to safeguard your community.",
        "helpline_title": "National Cybercrime Helplines (India)",
        "helpline_1930_desc": "Dial 1930 immediately if you suffered financial fraud within the last 24 hours to freeze transferred money.",
        "portal_desc": "Official Cyber Crime Portal: cybercrime.gov.in (Ministry of Home Affairs, India)",
        "report_form_title": "Submit a Community Scam Report",
        "report_form_type": "Scam Channel / Type:",
        "report_form_details": "Details / Message Text:",
        "report_form_submit": "🚨 Submit Threat Report",
        "report_form_success": "Your incident report has been submitted to assist threat awareness. Thank you for protecting the community!",

        # Error Page
        "error_default_title": "Page Not Found",
        "error_default_message": "The page you requested could not be found.",
        "error_try_again": "Try Again",
        "error_back_home": "Back to Home",

        # Footer & Disclaimer
        "footer_disclaimer": "🔒 Privacy & Safety Notice: ScamShield provides an estimated risk assessment to assist your decision-making and is not a guaranteed security verdict. Avoid uploading sensitive passwords or banking credentials.",
        "footer_copy": "© 2026 ScamShield • Machine Learning Lab Project • Built for Simplicity and Accessibility"
    },

    "mr": {
        # Brand & Nav
        "brand_title": "स्कॅमशील्ड",
        "brand_subtitle": "एआय आधारित फसवणूक ओळख आणि जोखीम मूल्यमापन",
        "nav_home": "मुख्यपृष्ठ",
        "nav_sms": "एसएमएस",
        "nav_email": "ईमेल",
        "nav_url": "वेब लिंक",
        "nav_phone": "फोन कॉल",
        "nav_history": "इतिहास",
        "nav_learn": "माहिती व शिक्षण",
        "nav_report": "तक्रार नोंदवा",
        "skip_to_content": "मुख्य मजकुराकडे थेट जा",

        # Theming & Accessibility Controls
        "theme_toggle": "डार्क / लाइट मोड बदला",
        "theme_dark": "🌙 डार्क",
        "theme_light": "☀️ लाइट",
        "a11y_dyslexia": "🔤 डिस्लेक्सिया फॉन्ट",
        "a11y_contrast": "👁️ हाय कॉन्ट्रास्ट",

        # Home Page & Onboarding
        "hero_title": "आज आपण काय तपासू इच्छिता?",
        "hero_subtitle": "कोणतीही कृती किंवा क्लिक करण्यापूर्वी संशयास्पद संदेश, ईमेल, लिंक्स आणि फोन कॉल्स तपासा.",
        "card_sms_title": "एसएमएस तपासा",
        "card_sms_desc": "संशयास्पद एसएमएस किंवा व्हॉट्सअॅप मेसेज तपासा.",
        "card_sms_btn": "संदेश तपासा →",
        "card_email_title": "ईमेल तपासा",
        "card_email_desc": "संशयास्पद किंवा फिशिंग ईमेल तपासा.",
        "card_email_btn": "ईमेल तपासा →",
        "card_url_title": "वेब लिंक तपासा",
        "card_url_desc": "वेबसाइट लिंक सुरक्षित आहे की संशयास्पद ते तपासा.",
        "card_url_btn": "लिंक तपासा →",
        "card_phone_title": "फोन कॉल तपासा",
        "card_phone_desc": "संशयास्पद कॉलबाबत काही सोप्या प्रश्नांची उत्तरे द्या.",
        "card_phone_btn": "प्रश्न सुरू करा →",
        "onboarding_title": "🛡️ स्कॅमशील्डवर नवीन आहात? ३ सोप्या पायऱ्या",
        "onboarding_step1": "१. तपासणीचा प्रकार निवडा (एसएमएस, ईमेल, वेब लिंक किंवा फोन कॉल).",
        "onboarding_step2": "२. मजकूर पेस्ट करा किंवा स्क्रीनशॉट अपलोड करा.",
        "onboarding_step3": "३. त्वरित धोका गुण आणि पुढील सुरक्षितता पावलांची यादी पहा.",
        "onboarding_dismiss": "समजले, धन्यवाद! ✕",

        # Form Controls & Privacy Banner
        "privacy_tip_title": "गोपनीयता सुरक्षा",
        "privacy_tip_desc": "सक्रिय ओटीपी, पासवर्ड किंवा संपूर्ण कार्ड तपशील कधीही पेस्ट करू नका. आपल्या संरक्षणासाठी स्कॅमशील्ड आपोआप संवेदनशील नंबर मास्क करते.",
        "btn_paste": "पेस्ट करा",
        "btn_clear": "साफ करा",
        "tab_paste_text": "✏️ संदेश मजकूर पेस्ट करा",
        "tab_upload_screenshot": "📷 स्क्रीनशॉट अपलोड करा",
        "tab_paste_email": "✏️ ईमेल तपशील पेस्ट करा",
        "tab_upload_email_screenshot": "📷 ईमेल स्क्रीनशॉट अपलोड करा",
        "tab_paste_url": "✏️ वेब लिंक पेस्ट करा",
        "tab_upload_url_screenshot": "📷 लिंक स्क्रीनशॉट अपलोड करा",
        "upload_drag_drop": "येथे स्क्रीनशॉट क्लिक करा किंवा ड्रॅग करा",
        "upload_formats": "PNG, JPG, JPEG, WEBP समर्थित (कमाल १६ MB)",
        "upload_remove": "✕ काढा",
        "try_example": "उदाहरणे वापरून पहा:",

        # SMS Page
        "sms_header_title": "एसएमएस किंवा व्हॉट्सअॅप संदेश तपासा",
        "sms_header_desc": "फसवणूक तपासण्यासाठी संदेश पेस्ट करा किंवा स्क्रीनशॉट अपलोड करा.",
        "sms_label": "येथे संदेश पेस्ट करा:",
        "sms_placeholder": "उदा: URGENT: तुमचे बँक खाते ब्लॉक केले आहे. अनलॉक करण्यासाठी येथे क्लिक करा http://bit.ly/verify...",
        "sms_btn": "🔍 संदेश आता तपासा",
        "sms_scan_btn": "🔍 स्क्रीनशॉट स्कॅन करा",

        # Email Page
        "email_header_title": "ईमेल सामग्री तपासा",
        "email_header_desc": "फिशिंग आणि फसवणूक ओळखण्यासाठी ईमेल तपशील पेस्ट करा किंवा स्क्रीनशॉट अपलोड करा.",
        "email_sender_label": "प्रेषक ईमेल पत्ता (पर्यायी):",
        "email_sender_placeholder": "उदा: support@service-security-alert.com",
        "email_subject_label": "ईमेल विषय (Subject):",
        "email_subject_placeholder": "उदा: Important: Security Notice Regarding Your Account",
        "email_body_label": "ईमेल मुख्य मजकूर:",
        "email_body_placeholder": "ईमेलमधील मजकूर येथे पेस्ट करा...",
        "email_btn": "🔍 ईमेल आता तपासा",
        "email_scan_btn": "🔍 स्क्रीनशॉट स्कॅन करा",

        # URL Page
        "url_header_title": "वेबसाइट लिंक (URL) तपासा",
        "url_header_desc": "वेबसाईट लिंक सुरक्षित आहे की धोकादायक ते तपासण्यासाठी लिंक पेस्ट करा किंवा स्क्रीनशॉट अपलोड करा.",
        "url_label": "वेबसाइट लिंक (URL) येथे पेस्ट करा:",
        "url_placeholder": "उदा: https://example.com/login किंवा http://192.168.1.1/claim",
        "url_help": "स्कॅमशील्ड दुर्भावनापूर्ण वेबसाइट्सना भेट न देता लिंकची सुरक्षितता तपासते.",
        "url_btn": "🔍 लिंक सुरक्षितता तपासा",
        "url_scan_btn": "🔍 स्क्रीनशॉट स्कॅन करा",

        # Phone Page
        "phone_header_title": "संशयास्पद फोन कॉल तपासा",
        "phone_header_desc": "कॉल करणाऱ्या व्यक्तीने काय सांगितले याविषयी या १० सोप्या प्रश्नांची उत्तरे द्या.",
        "phone_yes": "होय (YES)",
        "phone_no": "नाही (NO)",
        "phone_btn": "🔍 कॉलचा धोका गुण मोजा",

        # Results Page & Explainability
        "result_title": "स्कॅमशील्ड मूल्यांकन निकाल",
        "content_checked": "तपासलेला प्रकार:",
        "ocr_extracted_badge": "स्क्रीनशॉट स्कॅनरद्वारे काढलेला मजकूर",
        "risk_score_label": "अंदाजित धोका गुण (Risk Score)",
        "why_heading": "🔍 आम्ही हा गुण का दिला?",
        "what_heading": "🛡️ आता तुम्ही काय करावे?",
        "btn_check_another": "🔄 दुसरी तपासणी करा",
        "btn_view_history": "📋 तपासणी इतिहास पहा",
        "snippet_label": "तपासलेला मजकूर सारांश:",
        "sms_display_type": "एसएमएस / व्हॉट्सअॅप संदेश",
        "email_display_type": "ईमेल संदेश",
        "url_display_type": "वेबसाइट लिंक (URL)",
        "phone_display_type": "फोन कॉल मूल्यांकन",
        "btn_read_aloud": "🔊 निकाल ऐका",
        "btn_stop_audio": "⏹️ आवाज थांबवा",
        "btn_copy_summary": "📋 सारांश कॉपी करा",
        "btn_share_warning": "📤 इशारा शेअर करा",
        "toast_copied": "निकाल सारांश क्लिपबोर्डवर कॉपी केला!",
        "feedback_title": "हे मूल्यमापन उपयुक्त ठरले का?",
        "feedback_yes": "👍 होय, उपयुक्त",
        "feedback_no": "👎 चुकीचे नोंदवा",
        "feedback_thanks": "स्कॅमशील्ड सुधारण्यात मदत केल्याबद्दल धन्यवाद!",
        "disclaimer_result": "सूचना: स्कॅमशील्ड स्वयंचलित विश्लेषणावर आधारित जोखीम दर्शवते. कोणतीही आर्थिक कृती करण्यापूर्वी नेहमी अधिकृत बँकेशी संपर्क साधा.",

        # Analyzing Loading Overlay
        "analyzing_title": "फसवणुकीच्या संकेतांची तपासणी चालू आहे...",
        "analyzing_subtitle": "मजकूर, तात्काळ भाषेचे धोके आणि सुरक्षा विश्लेषणाचे काम सुरू आहे...",

        # Risk Labels & Summaries
        "risk_safe": "संभाव्य सुरक्षित (Safe)",
        "risk_medium": "संशयास्पद (मध्यम धोका)",
        "risk_high": "संभाव्य फसवणूक (उच्च धोका)",
        "risk_safe_summary": "या मजकुरात फसवणुकीचे कोणतेही थेट संकेत आढळले नाहीत, तरीही नेहमी सतर्क राहा.",
        "risk_medium_summary": "या मजकुरात काही संशयास्पद बाबी आढळल्या आहेत. काळजीपूर्वक व्यवहार करा.",
        "risk_high_summary": "फसवणूक किंवा फिशिंगची दाट शक्यता आहे. कोणतीही माहिती शेअर करू नका आणि लिंकवर क्लिक करू नका.",

        # History Page
        "history_title": "मागील तपासणी इतिहास",
        "history_desc": "केवळ तुमच्या चालू सत्रामध्ये सुरक्षित. कोणताही संवेदनशील डेटा कायमस्वरूपी साठवला जात नाही.",
        "history_clear_btn": "🗑️ इतिहास साफ करा",
        "history_empty_title": "अद्याप कोणतीही तपासणी केलेली नाही",
        "history_empty_desc": "इतिहास पाहण्यासाठी एसएमएस, ईमेल, लिंक किंवा फोन कॉल तपासा.",
        "history_go_home": "मुख्यपृष्ठावर जा",
        "history_search_placeholder": "कीवर्डद्वारे मागील स्कॅन शोधा...",
        "history_filter_all": "सर्व जोखीम पातळी",
        "history_filter_high": "उच्च धोका",
        "history_filter_medium": "मध्यम धोका",
        "history_filter_safe": "सुरक्षित",
        "history_export_csv": "📥 CSV डाउनलोड",
        "history_print": "🖨️ अहवाल प्रिंट करा",

        # Learn Page
        "learn_header_title": "फसवणूक जागृती आणि शिक्षण केंद्र",
        "learn_header_desc": "सायबर गुन्हेगारांच्या युक्त्या ओळखा, सावधगिरी बाळगा आणि सुरक्षित राहण्याचे नियम शिका.",
        "learn_patterns_title": "सामान्य फसवणुकीचे प्रकार आणि धोक्याचे इशारे",
        "learn_quiz_title": "तुमची फसवणूक ओळखण्याची क्षमता तपासा",
        "learn_faq_title": "वारंवार विचारले जाणारे प्रश्न (FAQ)",

        # Report Page
        "report_header_title": "सायबर फसवणुकीची तक्रार आणि अधिकृत हेल्पलाईन",
        "report_header_desc": "तातडीच्या मदतीसाठी संपर्क क्रमांक आणि सायबर गुन्हे नोंदणी मार्गदर्शन.",
        "helpline_title": "राष्ट्रीय सायबर गुन्हा हेल्पलाईन (भारत)",
        "helpline_1930_desc": "गेल्या २४ तासांत आर्थिक फसवणूक झाली असल्यास तत्काळ पैसे गोठवण्यासाठी १९३० वर त्वरित कॉल करा.",
        "portal_desc": "अधिकृत राष्ट्रीय सायबर गुन्हा तक्रार पोर्टल: cybercrime.gov.in (गृह मंत्रालय, भारत सरकार)",
        "report_form_title": "समुदाय सुरक्षा इशारा नोंदवा",
        "report_form_type": "फसवणुकीचा प्रकार:",
        "report_form_details": "तपशील / संदेश मजकूर:",
        "report_form_submit": "🚨 तक्रार सादर करा",
        "report_form_success": "इतरांचे संरक्षण करण्यासाठी तुमची तक्रार नोंदवली गेली आहे. सहकार्याबद्दल धन्यवाद!",

        # Error Page
        "error_default_title": "पृष्ठ आढळले नाही",
        "error_default_message": "तुम्ही विनंती केलेले पृष्ठ सापडले नाही.",
        "error_try_again": "पुन्हा प्रयत्न करा",
        "error_back_home": "मुख्य पृष्ठावर परत जा",

        # Footer & Disclaimer
        "footer_disclaimer": "🔒 गोपनीयता आणि सुरक्षितता सूचना: स्कॅमशील्ड तुमच्या निर्णयाला मदत करण्यासाठी अंदाजित जोखीम मूल्यमापन देते. संवेदनशील पासवर्ड किंवा बँक तपशील अपलोड करणे टाळा.",
        "footer_copy": "© २०२६ स्कॅमशील्ड • मशीन लर्निंग लॅब प्रकल्प • साधेपणा आणि सहजतेसाठी डिझाइन केलेले"
    },

    "hi": {
        # Brand & Nav
        "brand_title": "स्कैमशील्ड",
        "brand_subtitle": "एआई आधारित धोखाधड़ी पहचान एवं जोखिम मूल्यांकन",
        "nav_home": "होम",
        "nav_sms": "एसएमएस",
        "nav_email": "ईमेल",
        "nav_url": "वेब लिंक",
        "nav_phone": "फोन कॉल",
        "nav_history": "इतिहास",
        "nav_learn": "सीखें व जागरूकता",
        "nav_report": "रिपोर्ट करें",
        "skip_to_content": "सीधे मुख्य सामग्री पर जाएं",

        # Theming & Accessibility Controls
        "theme_toggle": "डार्क / लाइट मोड बदलें",
        "theme_dark": "🌙 डार्क",
        "theme_light": "☀️ लाइट",
        "a11y_dyslexia": "🔤 डिस्लेक्सिया फ़ॉन्ट",
        "a11y_contrast": "👁️ हाई कंट्रास्ट",

        # Home Page & Onboarding
        "hero_title": "आज आप क्या जांचना चाहते हैं?",
        "hero_subtitle": "कोई भी कदम उठाने या क्लिक करने से पहले संदिग्ध संदेश, ईमेल, लिंक और फोन कॉल की जांच करें।",
        "card_sms_title": "एसएमएस जांचें",
        "card_sms_desc": "संदिग्ध एसएमएस या व्हाट्सएप संदेश की जांच करें।",
        "card_sms_btn": "संदेश जांचें →",
        "card_email_title": "ईमेल जांचें",
        "card_email_desc": "संदिग्ध या फ़िशिंग ईमेल सामग्री की जांच करें।",
        "card_email_btn": "ईमेल जांचें →",
        "card_url_title": "वेब लिंक जांचें",
        "card_url_desc": "जांचें कि वेबसाइट लिंक सुरक्षित है या संदिग्ध।",
        "card_url_btn": "लिंक जांचें →",
        "card_phone_title": "फोन कॉल जांचें",
        "card_phone_desc": "संदिग्ध कॉल के बारे में कुछ सरल प्रश्नों के उत्तर दें।",
        "card_phone_btn": "प्रश्न शुरू करें →",
        "onboarding_title": "🛡️ स्कैमशील्ड पर नए हैं? ३ आसान कदम",
        "onboarding_step1": "१. जांच का प्रकार चुनें (एसएमएस, ईमेल, वेब लिंक या फोन कॉल)।",
        "onboarding_step2": "२. संदेश टेक्स्ट पेस्ट करें या स्क्रीनशॉट डालें।",
        "onboarding_step3": "३. तुरंत जोखिम स्कोर और सुरक्षा उपाय सूची प्राप्त करें।",
        "onboarding_dismiss": "समझ गया, धन्यवाद! ✕",

        # Form Controls & Privacy Banner
        "privacy_tip_title": "गोपनीयता सुरक्षा",
        "privacy_tip_desc": "सक्रिय ओटीपी, पासवर्ड या पूरा कार्ड विवरण कभी पेस्ट न करें। आपकी सुरक्षा के लिए स्कैमशील्ड संवेदनशील नंबरों को स्वतः मास्क करता है।",
        "btn_paste": "पेस्ट करें",
        "btn_clear": "साफ़ करें",
        "tab_paste_text": "✏️ संदेश टेक्स्ट पेस्ट करें",
        "tab_upload_screenshot": "📷 स्क्रीनशॉट अपलोड करें",
        "tab_paste_email": "✏️ ईमेल विवरण पेस्ट करें",
        "tab_upload_email_screenshot": "📷 ईमेल स्क्रीनशॉट अपलोड करें",
        "tab_paste_url": "✏️ वेब लिंक पेस्ट करें",
        "tab_upload_url_screenshot": "📷 लिंक स्क्रीनशॉट अपलोड करें",
        "upload_drag_drop": "स्क्रीनशॉट यहां क्लिक करें या ड्रैग करें",
        "upload_formats": "PNG, JPG, JPEG, WEBP समर्थित (अधिकतम १६ MB)",
        "upload_remove": "✕ हटाएं",
        "try_example": "उदाहरण आज़माएं:",

        # SMS Page
        "sms_header_title": "एसएमएस या व्हाट्सएप संदेश जांचें",
        "sms_header_desc": "धोखाधड़ी जांचने के लिए संदेश टेक्स्ट पेस्ट करें या स्क्रीनशॉट अपलोड करें।",
        "sms_label": "यहां संदेश पेस्ट करें:",
        "sms_placeholder": "उदा: URGENT: आपका बैंक खाता ब्लॉक कर दिया गया है। अनलॉक करने के लिए http://bit.ly/verify पर क्लिक करें...",
        "sms_btn": "🔍 संदेश अभी जांचें",
        "sms_scan_btn": "🔍 स्क्रीनशॉट स्कैन करें",

        # Email Page
        "email_header_title": "ईमेल सामग्री जांचें",
        "email_header_desc": "फ़िशिंग और धोखाधड़ी का पता लगाने के लिए ईमेल विवरण पेस्ट करें या स्क्रीनशॉट अपलोड करें।",
        "email_sender_label": "प्रेषक का ईमेल पता (वैकल्पिक):",
        "email_sender_placeholder": "उदा: support@service-security-alert.com",
        "email_subject_label": "ईमेल विषय (Subject):",
        "email_subject_placeholder": "उदा: Important: Security Notice Regarding Your Account",
        "email_body_label": "ईमेल मुख्य संदेश टेक्स्ट:",
        "email_body_placeholder": "ईमेल का टेक्स्ट यहां पेस्ट करें...",
        "email_btn": "🔍 ईमेल अभी जांचें",
        "email_scan_btn": "🔍 स्क्रीनशॉट स्कैन करें",

        # URL Page
        "url_header_title": "वेबसाइट लिंक (URL) जांचें",
        "url_header_desc": "वेबसाइट लिंक सुरक्षित है या दुर्भावनापूर्ण, यह जांचने के लिए लिंक पेस्ट करें या स्क्रीनशॉट अपलोड करें।",
        "url_label": "वेबसाइट लिंक (URL) यहां पेस्ट करें:",
        "url_placeholder": "उदा: https://example.com/login या http://192.168.1.1/claim",
        "url_help": "स्कैमशील्ड दुर्भावनापूर्ण वेबसाइटों पर जाए बिना लिंक की सुरक्षा की सुरक्षित रूप से जांच करता है।",
        "url_btn": "🔍 लिंक सुरक्षा जांचें",
        "url_scan_btn": "🔍 स्क्रीनशॉट स्कैन करें",

        # Phone Page
        "phone_header_title": "संदिग्ध फोन कॉल की जांच करें",
        "phone_header_desc": "कॉलर ने आपसे क्या करने को कहा, इस बारे में इन १० सरल प्रश्नों के उत्तर दें।",
        "phone_yes": "हाँ (YES)",
        "phone_no": "नहीं (NO)",
        "phone_btn": "🔍 कॉल जोखिम की गणना करें",

        # Results Page & Explainability
        "result_title": "स्कैमशील्ड मूल्यांकन परिणाम",
        "content_checked": "जांची गई सामग्री:",
        "ocr_extracted_badge": "स्क्रीनशॉट स्कैनर द्वारा निकाला गया टेक्स्ट",
        "risk_score_label": "अनुमानित जोखिम स्कोर (Risk Score)",
        "why_heading": "🔍 हमने यह स्कोर क्यों दिया?",
        "what_heading": "🛡️ अब आपको क्या करना चाहिए?",
        "btn_check_another": "🔄 दूसरी जांच करें",
        "btn_view_history": "📋 स्कैन इतिहास देखें",
        "snippet_label": "विश्लेषित सामग्री सारांश:",
        "sms_display_type": "एसएमएस / व्हाट्सएप संदेश",
        "email_display_type": "ईमेल संदेश",
        "url_display_type": "वेबसाइट लिंक (URL)",
        "phone_display_type": "फोन कॉल मूल्यांकन",
        "btn_read_aloud": "🔊 परिणाम सुनें",
        "btn_stop_audio": "⏹️ ऑडियो रोकें",
        "btn_copy_summary": "📋 सारांश कॉपी करें",
        "btn_share_warning": "📤 चेतावनी साझा करें",
        "toast_copied": "परिणाम सारांश क्लिपबोर्ड पर कॉपी किया गया!",
        "feedback_title": "क्या यह मूल्यांकन मददगार रहा?",
        "feedback_yes": "👍 हाँ, मददगार",
        "feedback_no": "👎 गलत रिपोर्ट करें",
        "feedback_thanks": "स्कैमशील्ड को बेहतर बनाने में मदद के लिए धन्यवाद!",
        "disclaimer_result": "अस्वीकरण: स्कैमशील्ड धोखाधड़ी के संकेतों का पता लगाने के लिए स्वचालित नियमों और मशीन लर्निंग का उपयोग करता है। वित्तीय कदम उठाने से पहले हमेशा बैंक से सीधे पुष्टि करें।",

        # Analyzing Loading Overlay
        "analyzing_title": "धोखाधड़ी के संकेतों का विश्लेषण जारी है...",
        "analyzing_subtitle": "टेक्स्ट पैटर्न, तात्कालिकता के संकेत और सुरक्षा जोखिमों की जांच की जा रही है...",

        # Risk Labels & Summaries
        "risk_safe": "संभावित रूप से सुरक्षित (Safe)",
        "risk_medium": "संदिग्ध (मध्यम जोखिम)",
        "risk_high": "संभावित धोखाधड़ी (उच्च जोखिम)",
        "risk_safe_summary": "इस सामग्री में तत्काल धोखाधड़ी का कोई संकेत नहीं मिला है, लेकिन हमेशा सतर्क रहें।",
        "risk_medium_summary": "इस सामग्री में कुछ संदिग्ध संकेत मिले हैं। सावधानी बरतें।",
        "risk_high_summary": "धोखाधड़ी या फ़िशिंग की अत्यधिक संभावना है। कोई भी जानकारी साझा न करें और लिंक पर क्लिक न करें।",

        # History Page
        "history_title": "हालिया स्कैन इतिहास",
        "history_desc": "केवल आपके वर्तमान सत्र में सुरक्षित है। कोई संवेदनशील डेटा स्थायी रूप से संग्रहीत नहीं होता है।",
        "history_clear_btn": "🗑️ इतिहास साफ़ करें",
        "history_empty_title": "अभी तक कोई स्कैन नहीं किया गया",
        "history_empty_desc": "परिणाम देखने के लिए एसएमएस, ईमेल, लिंक या फोन कॉल की जांच करें।",
        "history_go_home": "होम पर जाएं",
        "history_search_placeholder": "कीवर्ड द्वारा पिछले स्कैन खोजें...",
        "history_filter_all": "सभी जोखिम स्तर",
        "history_filter_high": "उच्च जोखिम",
        "history_filter_medium": "मध्यम जोखिम",
        "history_filter_safe": "सुरक्षित",
        "history_export_csv": "📥 CSV डाउनलोड",
        "history_print": "🖨️ रिपोर्ट प्रिंट करें",

        # Learn Page
        "learn_header_title": "धोखाधड़ी जागरूकता और शिक्षा केंद्र",
        "learn_header_desc": "धोखेबाजों की तकनीकों को पहचानना सीखें, चेतावनियों को समझें और सुरक्षित रहने के नियम जानें।",
        "learn_patterns_title": "सामान्य धोखाधड़ी के तरीके और खतरे के संकेत",
        "learn_quiz_title": "अपनी धोखाधड़ी पहचान क्षमता की जांच करें",
        "learn_faq_title": "अक्सर पूछे जाने वाले प्रश्न (FAQ)",

        # Report Page
        "report_header_title": "धोखाधड़ी की रिपोर्ट और आधिकारिक हेल्पलाइन",
        "report_header_desc": "त्वरित आपातकालीन हेल्पलाइन नंबर और घटना रिपोर्टिंग गाइड।",
        "helpline_title": "राष्ट्रीय साइबर अपराध हेल्पलाइन (भारत)",
        "helpline_1930_desc": "यदि पिछले २४ घंटों में वित्तीय धोखाधड़ी हुई है, तो स्थानांतरित धन रोकने के लिए तुरंत १९३० पर कॉल करें।",
        "portal_desc": "आधिकारिक राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल: cybercrime.gov.in (गृह मंत्रालय, भारत सरकार)",
        "report_form_title": "समुदाय सुरक्षा चेतावनी दर्ज करें",
        "report_form_type": "धोखाधड़ी का प्रकार:",
        "report_form_details": "विवरण / संदेश टेक्स्ट:",
        "report_form_submit": "🚨 रिपोर्ट दर्ज करें",
        "report_form_success": "दूसरों की सुरक्षा में मदद के लिए आपकी रिपोर्ट दर्ज कर ली गई है। धन्यवाद!",

        # Error Page
        "error_default_title": "पृष्ठ नहीं मिला",
        "error_default_message": "आपके द्वारा अनुरोधित पृष्ठ नहीं मिल सका।",
        "error_try_again": "पुनः प्रयास करें",
        "error_back_home": "होम पेज पर वापस जाएं",

        # Footer & Disclaimer
        "footer_disclaimer": "🔒 गोपनीयता और सुरक्षा सूचना: स्कैमशील्ड आपके निर्णय में सहायता के लिए अनुमानित जोखिम मूल्यांकन प्रदान करता है। संवेदनशील पासवर्ड या बैंकिंग विवरण अपलोड करने से बचें।",
        "footer_copy": "© 2026 स्कैमशील्ड • मशीन लर्निंग लैब प्रोजेक्ट • सरलता और सुगमता के लिए निर्मित"
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """Retrieves localized text string with fallback to English."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
