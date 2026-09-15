"""
ScamShield Multi-Language Localization Module
Provides comprehensive translations for English (en), Marathi (mr), and Hindi (hi).
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

        # Home Page
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

        # Common Tabs & Upload
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

        # Results Page
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

        # Risk Labels
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

        # Home Page
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

        # Common Tabs & Upload
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
        "sms_placeholder": "उदाहरण: URGENT: तुमचे बँक खाते ब्लॉक केले आहे. अनलॉक करण्यासाठी http://bit.ly/verify वर क्लिक करा...",
        "sms_btn": "🔍 संदेश आताच तपासा",
        "sms_scan_btn": "🔍 स्क्रीनशॉट स्कॅन करा",

        # Email Page
        "email_header_title": "ईमेल मजकूर तपासा",
        "email_header_desc": "फिशिंग आणि फसवणूक ओळखण्यासाठी ईमेल तपशील पेस्ट करा किंवा स्क्रीनशॉट अपलोड करा.",
        "email_sender_label": "पाठवणाऱ्याचा ईमेल पत्ता (पर्यायी):",
        "email_sender_placeholder": "उदाहरण: support@service-security-alert.com",
        "email_subject_label": "ईमेल विषय (Subject):",
        "email_subject_placeholder": "उदाहरण: Important: Security Notice Regarding Your Account",
        "email_body_label": "ईमेल मजकूर (Body):",
        "email_body_placeholder": "ईमेलचा संपूर्ण मजकूर येथे पेस्ट करा...",
        "email_btn": "🔍 ईमेल आताच तपासा",
        "email_scan_btn": "🔍 ईमेल स्क्रीनशॉट स्कॅन करा",

        # URL Page
        "url_header_title": "वेबसाइट लिंक (URL) तपासा",
        "url_header_desc": "क्लिक करण्यापूर्वी लिंक सुरक्षित आहे की धोकादायक ते तपासा.",
        "url_label": "येथे वेबसाइट लिंक (URL) पेस्ट करा:",
        "url_placeholder": "उदाहरण: https://example.com/login किंवा http://192.168.1.1/claim",
        "url_help": "स्कॅमशील्ड धोकादायक वेबसाइटवर न जाता लिंकची सुरक्षितपणे तपासणी करते.",
        "url_btn": "🔍 लिंक सुरक्षितता तपासा",
        "url_scan_btn": "🔍 लिंक स्क्रीनशॉट स्कॅन करा",

        # Phone Page
        "phone_header_title": "संशयास्पद फोन कॉल तपासा",
        "phone_header_desc": "कॉल करणाऱ्याने काय विचारले याबद्दल १० सोप्या प्रश्नांची उत्तरे द्या.",
        "phone_yes": "होय (YES)",
        "phone_no": "नाही (NO)",
        "phone_btn": "🔍 कॉल जोखीम मोजा",

        # Results Page
        "result_title": "स्कॅमशील्ड तपासणी निकाल",
        "content_checked": "तपासलेला प्रकार:",
        "ocr_extracted_badge": "स्क्रीनशॉट ओसीआर द्वारे वाचले गेले",
        "risk_score_label": "अंदाजित जोखीम गुण (Risk Score)",
        "why_heading": "🔍 हा निकाल का देण्यात आला?",
        "what_heading": "🛡️ आता तुम्ही काय करावे?",
        "btn_check_another": "🔄 दुसरी तपासणी करा",
        "btn_view_history": "📋 तपासणी इतिहास पहा",
        "snippet_label": "तपासलेला मजकूर सारांश:",
        "sms_display_type": "एसएमएस / व्हॉट्सअॅप संदेश",
        "email_display_type": "ईमेल संदेश",
        "url_display_type": "वेबसाइट लिंक (URL)",
        "phone_display_type": "फोन कॉल मूल्यमापन",

        # Risk Labels
        "risk_safe": "सुरक्षित वाटत आहे (Safe)",
        "risk_medium": "संशयास्पद (मध्यम जोखीम)",
        "risk_high": "संभाव्य फसवणूक (धोकादायक)",
        "risk_safe_summary": "या मजकुरात फसवणुकीचे कोणतेही त्वरित चिन्ह आढळले नाही, तरीही नेहमी सावध राहा.",
        "risk_medium_summary": "या मजकुरात काही संशयास्पद गोष्टी आढळल्या आहेत. काळजीपूर्वक व्यवहार करा.",
        "risk_high_summary": "फसवणूक किंवा फिशिंगची दाट शक्यता आहे. कोणतीही माहिती देऊ नका किंवा लिंकवर क्लिक करू नका.",

        # History Page
        "history_title": "अलीकडील तपासणी इतिहास",
        "history_desc": "केवळ तुमच्या सध्याच्या सत्रात सेव्ह केले आहे. कोणतीही खाजगी माहिती कायमस्वरूपी साठवली जात नाही.",
        "history_clear_btn": "🗑️ इतिहास साफ करा",
        "history_empty_title": "अद्याप कोणतीही तपासणी केलेली नाही",
        "history_empty_desc": "इतिहास पाहण्यासाठी एसएमएस, ईमेल, लिंक किंवा फोन कॉल तपासा.",
        "history_go_home": "मुख्यपृष्ठावर जा",

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

        # Home Page
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

        # Common Tabs & Upload
        "tab_paste_text": "✏️ संदेश पेस्ट करें",
        "tab_upload_screenshot": "📷 स्क्रीनशॉट अपलोड करें",
        "tab_paste_email": "✏️ ईमेल विवरण पेस्ट करें",
        "tab_upload_email_screenshot": "📷 ईमेल स्क्रीनशॉट अपलोड करें",
        "tab_paste_url": "✏️ लिंक पेस्ट करें",
        "tab_upload_url_screenshot": "📷 लिंक स्क्रीनशॉट अपलोड करें",
        "upload_drag_drop": "स्क्रीनशॉट यहां क्लिक करें या ड्रैग करें",
        "upload_formats": "PNG, JPG, JPEG, WEBP समर्थित (अधिकतम 16 MB)",
        "upload_remove": "✕ हटाएं",
        "try_example": "उदाहरण आज़माएं:",

        # SMS Page
        "sms_header_title": "एसएमएस या व्हाट्सएप संदेश जांचें",
        "sms_header_desc": "धोखाधड़ी जांचने के लिए संदेश पेस्ट करें या स्क्रीनशॉट अपलोड करें।",
        "sms_label": "संदेश यहां पेस्ट करें:",
        "sms_placeholder": "उदाहरण: URGENT: आपका बैंक खाता ब्लॉक कर दिया गया है। अनलॉक करने के लिए http://bit.ly/verify पर क्लिक करें...",
        "sms_btn": "🔍 संदेश अभी जांचें",
        "sms_scan_btn": "🔍 स्क्रीनशॉट स्कैन करें",

        # Email Page
        "email_header_title": "ईमेल सामग्री जांचें",
        "email_header_desc": "फ़िशिंग और धोखाधड़ी पकड़ने के लिए ईमेल विवरण पेस्ट करें या स्क्रीनशॉट अपलोड करें।",
        "email_sender_label": "भेजने वाले का ईमेल पता (वैकल्पिक):",
        "email_sender_placeholder": "उदाहरण: support@service-security-alert.com",
        "email_subject_label": "ईमेल विषय (Subject):",
        "email_subject_placeholder": "उदाहरण: Important: Security Notice Regarding Your Account",
        "email_body_label": "ईमेल मुख्य भाग (Body):",
        "email_body_placeholder": "ईमेल का पूरा विवरण यहां पेस्ट करें...",
        "email_btn": "🔍 ईमेल अभी जांचें",
        "email_scan_btn": "🔍 ईमेल स्क्रीनशॉट स्कैन करें",

        # URL Page
        "url_header_title": "वेबसाइट लिंक (URL) जांचें",
        "url_header_desc": "क्लिक करने से पहले जांचें कि लिंक सुरक्षित है या दुर्भावनापूर्ण।",
        "url_label": "वेबसाइट लिंक (URL) यहां पेस्ट करें:",
        "url_placeholder": "उदाहरण: https://example.com/login या http://192.168.1.1/claim",
        "url_help": "स्कैमशील्ड दुर्भावनापूर्ण वेबसाइटों पर जाए बिना लिंक की सुरक्षित जांच करता है।",
        "url_btn": "🔍 लिंक सुरक्षा जांचें",
        "url_scan_btn": "🔍 लिंक स्क्रीनशॉट स्कैन करें",

        # Phone Page
        "phone_header_title": "संदिग्ध फोन कॉल की जांच करें",
        "phone_header_desc": "कॉलर ने आपसे क्या कहा, इसके बारे में 10 सरल प्रश्नों के उत्तर दें।",
        "phone_yes": "हाँ (YES)",
        "phone_no": "नहीं (NO)",
        "phone_btn": "🔍 कॉल जोखिम की गणना करें",

        # Results Page
        "result_title": "स्कैमशील्ड मूल्यांकन परिणाम",
        "content_checked": "जांचा गया प्रकार:",
        "ocr_extracted_badge": "स्क्रीनशॉट ओसीआर द्वारा निकाला गया",
        "risk_score_label": "अनुमानित जोखिम स्कोर (Risk Score)",
        "why_heading": "🔍 हमने यह स्कोर क्यों दिया?",
        "what_heading": "🛡️ अब आपको क्या करना चाहिए?",
        "btn_check_another": "🔄 दूसरा आइटम जांचें",
        "btn_view_history": "📋 स्कैन इतिहास देखें",
        "snippet_label": "विश्लेषण किया गया विवरण:",
        "sms_display_type": "एसएमएस / व्हाट्सएप संदेश",
        "email_display_type": "ईमेल संदेश",
        "url_display_type": "वेबसाइट लिंक (URL)",
        "phone_display_type": "फोन कॉल मूल्यांकन",

        # Risk Labels
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

        # Footer & Disclaimer
        "footer_disclaimer": "🔒 गोपनीयता और सुरक्षा सूचना: स्कैमशील्ड आपके निर्णय में सहायता के लिए अनुमानित जोखिम मूल्यांकन प्रदान करता है। संवेदनशील पासवर्ड या बैंकिंग विवरण अपलोड करने से बचें।",
        "footer_copy": "© 2026 स्कैमशील्ड • मशीन लर्निंग लैब प्रोजेक्ट • सरलता और सुगमता के लिए निर्मित"
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """Retrieves localized text string with fallback to English."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
