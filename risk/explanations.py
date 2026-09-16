"""
Explanation and Recommendation Generator
Transforms technical ML outputs and matched heuristics into empathetic, plain-language guidance.
"""

from typing import List, Dict, Any


DEFAULT_SAFE_ACTIONS = {
    "en": [
        "Always verify unexpected messages through official customer support channels before taking action.",
        "Do not click on links or download attachments from unfamiliar or unexpected senders.",
        "Remember that legitimate institutions will never ask for your passwords or full PIN."
    ],
    "mr": [
        "कोणतीही कृती करण्यापूर्वी अधिकृत ग्राहक सेवा चॅनेलद्वारे अनपेक्षित संदेशांची नेहमी खात्री करा.",
        "अनोळखी किंवा संशयास्पद पाठवणाऱ्यांच्या लिंकवर क्लिक करू नका किंवा फाइल्स डाउनलोड करू नका.",
        "लक्षात ठेवा की अधिकृत बँका आणि संस्था कधीही तुमचे पासवर्ड किंवा संपूर्ण एटीएम पिन मागत नाहीत."
    ],
    "hi": [
        "कोई भी कदम उठाने से पहले हमेशा आधिकारिक ग्राहक सहायता के माध्यम से अनपेक्षित संदेशों की पुष्टि करें।",
        "अपरिचित या संदिग्ध प्रेषकों के लिंक पर क्लिक न करें और न ही फाइलें डाउनलोड करें।",
        "याद रखें कि वैध संस्थाएं और बैंक कभी भी आपके पासवर्ड या पूरा एटीएम पिन नहीं मांगते हैं।"
    ]
}

DEFAULT_SUSPICIOUS_ACTIONS = {
    "en": [
        "Do NOT click any links or download any files attached to this message.",
        "Do NOT reply, call phone numbers provided in the message, or share any personal details.",
        "If this claims to be from a service you use (bank, email, shopping), log into your account directly from your browser to check for real notifications."
    ],
    "mr": [
        "या संदेशासोबत जोडलेल्या कोणत्याही लिंकवर क्लिक करू नका किंवा फाइल डाउनलोड करू नका.",
        "उत्तर देऊ नका, संदेशात दिलेल्या क्रमांकावर कॉल करू नका किंवा कोणतीही वैयक्तिक माहिती शेअर करू नका.",
        "जर हा संदेश तुमच्या बँक किंवा सेवेचा असल्याचा दावा करत असेल, तर थेट अधिकृत वेबसाइटवर लॉगिन करून तपासा."
    ],
    "hi": [
        "इस संदेश से जुड़े किसी भी लिंक पर क्लिक न करें और न ही कोई फाइल डाउनलोड करें।",
        "उत्तर न दें, संदेश में दिए गए नंबरों पर कॉल न करें और न ही कोई व्यक्तिगत जानकारी साझा करें।",
        "यदि यह आपके बैंक या किसी सेवा से होने का दावा करता है, तो सीधे अपने ब्राउज़र से आधिकारिक वेबसाइट पर लॉगिन करें।"
    ]
}

DEFAULT_HIGH_RISK_ACTIONS = {
    "en": [
        "DO NOT click any links, open attachments, or reply to this message.",
        "DO NOT share any One-Time Password (OTP), credit card number, PIN, or bank information.",
        "Block the sender and report the message as spam or phishing in your email/messaging app.",
        "If you have already clicked a link or shared information, immediately contact your bank and change your account passwords."
    ],
    "mr": [
        "कोणत्याही लिंकवर क्लिक करू नका, फाइल उघडू नका आणि या संदेशाला उत्तर देऊ नका.",
        "कोणताही ओटीपी (OTP), क्रेडिट/डेबिट कार्ड नंबर, पिन किंवा बँक तपशील कोणाशीही शेअर करू नका.",
        "हा क्रमांक किंवा ईमेल ब्लॉक करा आणि स्पॅम/फिशिंग म्हणून तक्रार नोंदवा.",
        "जर तुम्ही आधीच माहिती शेअर केली असेल, तर त्वरित तुमच्या बँकेशी संपर्क साधा आणि पासवर्ड बदला."
    ],
    "hi": [
        "किसी भी लिंक पर क्लिक न करें, अटैचमेंट न खोलें और इस संदेश का उत्तर न दें।",
        "कोई भी वन-टाइम पासवर्ड (OTP), क्रेडिट कार्ड नंबर, पिन या बैंक विवरण साझा न करें।",
        "प्रेषक को ब्लॉक करें और अपने ऐप में संदेश को स्पैम या फ़िशिंग के रूप में रिपोर्ट करें।",
        "यदि आपने पहले ही जानकारी साझा कर दी है, तो तुरंत अपने बैंक से संपर्क करें और पासवर्ड बदलें।"
    ]
}

DEFAULT_SAFE_REASONS = {
    "en": [
        "No aggressive scam phrases or urgent payment requests detected.",
        "Standard language structure with no identified threat or credential demand."
    ],
    "mr": [
        "या मजकुरात कोणतेही आक्रमक घोटाळ्याचे शब्द किंवा तातडीने पैशांची मागणी आढळली नाही.",
        "ओळखपत्र, पासवर्ड किंवा बँक तपशील मागितल्याचा कोणताही धोका आढळला नाही."
    ],
    "hi": [
        "इस संदेश में धोखाधड़ी वाले शब्द या तत्काल भुगतान के अनुरोध नहीं पाए गए।",
        "सामान्य भाषा संरचना, जिसमें कोई धमकी या क्रेडेंशियल की मांग नहीं मिली।"
    ]
}


def build_explanation_summary(
    risk_level: str,
    reasons: List[str],
    actions: List[str],
    has_urls: bool = False,
    url_risk_level: str = "LOW",
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Constructs a clear visual explanation structure in requested language (en, mr, hi):
    - Clean deduplicated 'Why is this suspicious?' list
    - Prioritized 'What should you do?' checklist
    - Summary banner sentence
    """
    valid_lang = lang if lang in ("en", "mr", "hi") else "en"

    # Deduplicate reasons while preserving order
    unique_reasons = []
    for r in reasons:
        if r not in unique_reasons:
            unique_reasons.append(r)
            
    # If safe and no suspicious reasons found
    if not unique_reasons and risk_level == "LOW":
        unique_reasons = DEFAULT_SAFE_REASONS.get(valid_lang, DEFAULT_SAFE_REASONS["en"])
        
    # Deduplicate actions
    unique_actions = []
    for a in actions:
        if a not in unique_actions:
            unique_actions.append(a)
            
    # Add baseline safe guidance if empty
    if not unique_actions:
        if risk_level == "LOW":
            unique_actions = DEFAULT_SAFE_ACTIONS.get(valid_lang, DEFAULT_SAFE_ACTIONS["en"])
        elif risk_level == "MEDIUM":
            unique_actions = DEFAULT_SUSPICIOUS_ACTIONS.get(valid_lang, DEFAULT_SUSPICIOUS_ACTIONS["en"])
        else:
            unique_actions = DEFAULT_HIGH_RISK_ACTIONS.get(valid_lang, DEFAULT_HIGH_RISK_ACTIONS["en"])
            
    return {
        "reasons": unique_reasons,
        "actions": unique_actions
    }
