"""
Phone Call Scam Risk Questionnaire Assessment Engine
Evaluates caller behavior based on 10 targeted safety questions.
"""

from typing import Dict, Any, List
from config import RISK_THRESHOLDS, RISK_LEVEL_META


PHONE_QUESTIONS = [
    {
        "id": "q1",
        "question": "Did the caller ask for an OTP (One-Time Password) or verification code?",
        "question_mr": "कॉल करणाऱ्या व्यक्तीने ओटीपी (OTP) किंवा व्हेरिफिकेशन कोड विचारला का?",
        "question_hi": "क्या कॉलर ने ओटीपी (OTP) या वेरिफिकेशन कोड मांगा?",
        "weight": 30,
        "reason": "The caller asked for an OTP / security code.",
        "reason_mr": "कॉल करणाऱ्याने ओटीपी (OTP) किंवा सुरक्षा कोड विचारला.",
        "reason_hi": "कॉलर ने ओटीपी (OTP) या सुरक्षा कोड मांगा।",
        "action": "NEVER share an OTP with anyone over the phone. Legitimate banks and staff will never ask for your OTP.",
        "action_mr": "फोनवर कोणाशीही कधीही OTP शेअर करू नका. बँक अधिकारी कधीही तुमचा OTP मागत नाहीत.",
        "action_hi": "फोन पर कभी भी किसी के साथ OTP साझा न करें। बैंक कर्मचारी कभी भी आपका OTP नहीं मांगते।"
    },
    {
        "id": "q2",
        "question": "Did the caller ask for your bank account number, card number, or CVV?",
        "question_mr": "कॉल करणाऱ्याने तुमचा बँक खाते क्रमांक, डेबिट/क्रेडिट कार्ड नंबर किंवा CVV विचारला का?",
        "question_hi": "क्या कॉलर ने आपका बैंक खाता नंबर, कार्ड नंबर या CVV मांगा?",
        "weight": 30,
        "reason": "The caller asked for your banking or debit/credit card details.",
        "reason_mr": "कॉल करणाऱ्याने तुमचे बँक खाते किंवा कार्ड तपशील विचारले.",
        "reason_hi": "कॉलर ने आपके बैंक खाते या कार्ड का विवरण मांगा।",
        "action": "Do NOT share card numbers, PINs, or banking passwords. End the call immediately.",
        "action_mr": "कार्ड क्रमांक, पिन किंवा पासवर्ड शेअर करू नका. कॉल त्वरित बंद करा.",
        "action_hi": "कार्ड नंबर, पिन या पासवर्ड साझा न करें। तुरंत कॉल समाप्त करें।"
    },
    {
        "id": "q3",
        "question": "Did the caller ask you to send money, wire funds, or buy gift cards?",
        "question_mr": "कॉल करणाऱ्याने तुम्हाला पैसे पाठवण्यास, ट्रान्सफर करण्यास किंवा गिफ्ट कार्ड खरेदी करण्यास सांगितले का?",
        "question_hi": "क्या कॉलर ने आपको पैसे भेजने, ट्रांसफर करने या गिफ्ट कार्ड खरीदने के लिए कहा?",
        "weight": 25,
        "reason": "The caller demanded a payment, money transfer, or gift card purchase.",
        "reason_mr": "कॉल करणाऱ्याने पैसे पाठवण्याची किंवा गिफ्ट कार्ड खरेदी करण्याची मागणी केली.",
        "reason_hi": "कॉलर ने पैसे भेजने या गिफ्ट कार्ड खरीदने की मांग की।",
        "action": "Do NOT transfer money or purchase gift cards. Scammers frequently demand payment through non-refundable methods.",
        "action_mr": "पैसे पाठवू नका किंवा गिफ्ट कार्ड खरेदी करू नका. फसवणूक करणारे अशा मार्गांचा वापर करतात.",
        "action_hi": "पैसे ट्रांसफर न करें और न ही गिफ्ट कार्ड खरीदें। धोखेबाज ऐसे तरीकों की मांग करते हैं।"
    },
    {
        "id": "q4",
        "question": "Did the caller create urgency, rush you, or tell you not to hang up?",
        "question_mr": "कॉल करणाऱ्याने घाईगडबड केली, दबाव आणला किंवा फोन कट न करण्यास सांगितले का?",
        "question_hi": "क्या कॉलर ने जल्दबाजी की, दबाव बनाया या फोन न काटने के लिए कहा?",
        "weight": 15,
        "reason": "The caller pressured you to act immediately without checking.",
        "reason_mr": "कॉल करणाऱ्याने विचार न करता त्वरित कृती करण्यासाठी दबाव आणला.",
        "reason_hi": "कॉलर ने बिना सोचे-समझे तुरंत कदम उठाने का दबाव बनाया।",
        "action": "Take your time. Scammers create fake urgency to panic you. Hang up and verify independently.",
        "action_mr": "शांत राहा. भीती निर्माण करण्यासाठी अशी घाई केली जाते. फोन ठेवा आणि स्वतंत्रपणे खात्री करा.",
        "action_hi": "शांत रहें। घबराहट पैदा करने के लिए ऐसी जल्दबाजी की जाती है। फोन काटें और स्वतंत्र जांच करें।"
    },
    {
        "id": "q5",
        "question": "Did the caller claim to represent a bank, government department, police, or tech support?",
        "question_mr": "कॉल करणाऱ्याने बँक, सरकारी विभाग, पोलीस किंवा टेक सपोर्टचा अधिकारी असल्याचा दावा केला का?",
        "question_hi": "क्या कॉलर ने बैंक, सरकारी विभाग, पुलिस या टेक सपोर्ट प्रतिनिधि होने का दावा किया?",
        "weight": 10,
        "reason": "The caller claimed official authority (bank, police, tax, or tech support).",
        "reason_mr": "कॉल करणाऱ्याने अधिकृत संस्था (बँक, पोलीस, कर विभाग इ.) असल्याचा दावा केला.",
        "reason_hi": "कॉलर ने आधिकारिक संस्था (बैंक, पुलिस, टैक्स आदि) का प्रतिनिधि होने का दावा किया।",
        "action": "Do not trust caller ID. Contact the organization using the official customer care number listed on your bank statement.",
        "action_mr": "कॉलर आयडीवर विश्वास ठेवू नका. बँकेच्या अधिकृत कस्टमर केअर नंबरवर स्वतः संपर्क साधा.",
        "action_hi": "कॉलर आईडी पर भरोसा न करें। बैंक के आधिकारिक कस्टमर केयर नंबर पर स्वयं संपर्क करें।"
    },
    {
        "id": "q6",
        "question": "Did the caller ask you to install an app or screen-sharing tool (AnyDesk, TeamViewer, QuickSupport)?",
        "question_mr": "कॉल करणाऱ्याने कोणतेही अॅप किंवा स्क्रीन-शेअरिंग टूल (AnyDesk, TeamViewer इ.) इन्स्टॉल करण्यास सांगितले का?",
        "question_hi": "क्या कॉलर ने कोई ऐप या स्क्रीन-शेयरिंग टूल (AnyDesk, TeamViewer आदि) इंस्टॉल करने को कहा?",
        "weight": 25,
        "reason": "The caller asked you to install software or screen-sharing apps.",
        "reason_mr": "कॉल करणाऱ्याने स्क्रीन-शेअरिंग अॅप किंवा सॉफ्टवेअर डाउनलोड करण्यास सांगितले.",
        "reason_hi": "कॉलर ने स्क्रीन-शेयरिंग ऐप या सॉफ्टवेयर डाउनलोड करने को कहा।",
        "action": "NEVER install remote access or screen-sharing apps on your phone or computer at the request of an unknown caller.",
        "action_mr": "अनोळखी व्यक्तीच्या सांगण्यावरून फोन किंवा कॉम्प्युटरवर कोणतेही रिमोट अॅप इन्स्टॉल करू नका.",
        "action_hi": "अज्ञात कॉलर के कहने पर फोन या कंप्यूटर पर कोई भी रिमोट ऐप इंस्टॉल न करें।"
    },
    {
        "id": "q7",
        "question": "Did the caller ask you to click a link sent via SMS, WhatsApp, or email during the call?",
        "question_mr": "कॉल चालू असताना एसएमएस, व्हॉट्सअॅप किंवा ईमेलवरील लिंकवर क्लिक करण्यास सांगितले का?",
        "question_hi": "क्या कॉलर ने कॉल के दौरान एसएमएस, व्हाट्सएप या ईमेल पर भेजे लिंक पर क्लिक करने को कहा?",
        "weight": 20,
        "reason": "The caller instructed you to click a link while speaking on the phone.",
        "reason_mr": "कॉल चालू असताना लिंकवर क्लिक करण्यास सांगितले गेले.",
        "reason_hi": "कॉल के दौरान लिंक पर क्लिक करने का निर्देश दिया गया।",
        "action": "Do not click links sent during a phone call. These links often lead to fake phishing pages.",
        "action_mr": "फोन कॉल चालू असताना आलेल्या लिंकवर क्लिक करू नका. या बनावट लिंक्स असू शकतात.",
        "action_hi": "फोन कॉल के दौरान भेजे गए लिंक पर क्लिक न करें। ये फर्जी लिंक हो सकते हैं।"
    },
    {
        "id": "q8",
        "question": "Did the caller threaten account suspension, electricity cutoff, arrest, or legal action?",
        "question_mr": "कॉल करणाऱ्याने खाते बंद करणे, वीज खंडित करणे, अटक किंवा कायदेशीर कारवाईची धमकी दिली का?",
        "question_hi": "क्या कॉलर ने खाता बंद करने, बिजली काटने, गिरफ्तारी या कानूनी कार्रवाई की धमकी दी?",
        "weight": 25,
        "reason": "The caller used threats (arrest, service disconnection, account freezing).",
        "reason_mr": "कॉल करणाऱ्याने भीती आणि धमक्यांचा (अटक, खाते बंद) वापर केला.",
        "reason_hi": "कॉलर ने डर और धमकियों (गिरफ्तारी, खाता बंद) का इस्तेमाल किया।",
        "action": "Official authorities will never arrest you over a phone call or demand instant payment to avoid penalties.",
        "action_mr": "अधिकृत यंत्रणा फोनवर कारवाईची धमकी देऊन त्वरित पैशांची मागणी कधीही करत नाहीत.",
        "action_hi": "सरकारी एजेंसियां फोन पर गिरफ्तारी की धमकी देकर तुरंत पैसे की मांग कभी नहीं करती हैं।"
    },
    {
        "id": "q9",
        "question": "Did the caller offer an unexpected prize, lottery winnings, tax refund, or easy loan?",
        "question_mr": "कॉल करणाऱ्याने अनपेक्षित बक्षीस, लॉटरी, टॅक्स रिफंड किंवा सोप्या कर्जाची ऑफर दिली का?",
        "question_hi": "क्या कॉलर ने अप्रत्याशित इनाम, लॉटरी, टैक्स रिफंड या आसान लोन की पेशकश की?",
        "weight": 15,
        "reason": "The caller promised an unexpected cash prize, refund, or reward.",
        "reason_mr": "कॉल करणाऱ्याने रोख बक्षीस, लॉटरी किंवा रिफंडचे आमिष दाखवले.",
        "reason_hi": "कॉलर ने नकद इनाम, लॉटरी या रिफंड का लालच दिया।",
        "action": "Reject unexpected prize or refund offers. If it sounds too good to be true, it is almost certainly a scam.",
        "action_mr": "अनपेक्षित बक्षीस किंवा रिफंडच्या ऑफर्स नाकारा. हे फसवणुकीचे आमिष असू शकते.",
        "action_hi": "अप्रत्याशित इनाम या रिफंड की पेशकश को अस्वीकार करें। यह धोखाधड़ी का जाल हो सकता है।"
    },
    {
        "id": "q10",
        "question": "Did the caller ask for your ATM PIN, net banking password, or app password?",
        "question_mr": "कॉल करणाऱ्याने तुमचा एटीएम पिन (PIN), नेट बँकिंग पासवर्ड किंवा यूपीआय पासवर्ड विचारला का?",
        "question_hi": "क्या कॉलर ने आपका एटीएम पिन (PIN), नेट बैंकिंग पासवर्ड या यूपीआई पासवर्ड मांगा?",
        "weight": 30,
        "reason": "The caller asked for your secret PIN or password.",
        "reason_mr": "कॉल करणाऱ्याने तुमचा गुप्त पिन किंवा पासवर्ड विचारला.",
        "reason_hi": "कॉलर ने आपका गोपनीय पिन या पासवर्ड मांगा।",
        "action": "Your PIN and passwords are strictly confidential. No bank employee will ever ask for them.",
        "action_mr": "तुमचा पिन आणि पासवर्ड अत्यंत गोपनीय आहेत. कोणताही बँक कर्मचारी ते कधीही मागत नाही.",
        "action_hi": "आपका पिन और पासवर्ड पूरी तरह गोपनीय हैं। कोई भी बैंक कर्मचारी इसे कभी नहीं मांगता।"
    }
]


def get_localized_phone_questions(lang: str = "en") -> List[Dict[str, Any]]:
    """Returns question list with question text localized for given language."""
    localized = []
    for q in PHONE_QUESTIONS:
        item = dict(q)
        if lang == "mr":
            item["question"] = q.get("question_mr", q["question"])
        elif lang == "hi":
            item["question"] = q.get("question_hi", q["question"])
        else:
            item["question"] = q["question"]
        localized.append(item)
    return localized


def assess_phone_call_risk(answers: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
    """
    Computes risk score, risk level, reasons, and safety recommendations based on answers.
    answers: dict where keys are question IDs ('q1', 'q2', ...) and values are 'yes'/'no' or boolean.
    """
    total_score = 0
    reasons = []
    actions = []
    matched_questions = []

    for item in PHONE_QUESTIONS:
        qid = item["id"]
        val = answers.get(qid, "")
        is_yes = False
        if isinstance(val, bool):
            is_yes = val
        elif isinstance(val, str):
            is_yes = val.lower().strip() in ("yes", "y", "1", "true")
        elif isinstance(val, (int, float)):
            is_yes = bool(val)

        if is_yes:
            total_score += item["weight"]
            if lang == "mr":
                reasons.append(item.get("reason_mr", item["reason"]))
                actions.append(item.get("action_mr", item["action"]))
            elif lang == "hi":
                reasons.append(item.get("reason_hi", item["reason"]))
                actions.append(item.get("action_hi", item["action"]))
            else:
                reasons.append(item["reason"])
                actions.append(item["action"])
            matched_questions.append(qid)

    # Risk Score capped at 100
    risk_score = min(100, total_score)

    # Determine Risk Level
    if risk_score <= RISK_THRESHOLDS["LOW_MAX"]:
        risk_level = "LOW"
    elif risk_score <= RISK_THRESHOLDS["MEDIUM_MAX"]:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    meta = RISK_LEVEL_META[risk_level]

    if not reasons:
        if lang == "mr":
            reasons = [
                "या कॉलमध्ये कोणताही संशयास्पद दबाव किंवा खाजगी माहितीची मागणी आढळली नाही.",
                "कॉल करणाऱ्याने ओटीपी, पासवर्ड किंवा पैशांची मागणी केली नाही."
            ]
            actions = [
                "नेहमी सतर्क राहा. कॉलर कितीही नम्र बोलत असला तरी गोपनीय माहिती देऊ नका.",
                "संशय आल्यास फोन ठेवा आणि अधिकृत क्रमांकावर खात्री करा."
            ]
        elif lang == "hi":
            reasons = [
                "इस कॉल में कोई संदिग्ध दबाव या गोपनीय जानकारी की मांग नहीं पाई गई।",
                "कॉलर ने ओटीपी, पासवर्ड या पैसों की मांग नहीं की।"
            ]
            actions = [
                "हमेशा सतर्क रहें। कॉलर कितना भी विनम्र हो, गोपनीय विवरण साझा न करें।",
                "संदेह होने पर फोन काटें और आधिकारिक नंबर पर पुष्टि करें।"
            ]
        else:
            reasons = [
                "No high-pressure tactics or confidential information requests reported for this call.",
                "The caller did not request OTPs, passwords, or immediate financial transactions."
            ]
            actions = [
                "Always stay alert. Even if a caller seems polite, never share passwords or banking credentials.",
                "If in doubt, hang up and call the organization's verified phone number."
            ]

    # Localized label and summary
    from translations import get_text
    risk_label = get_text(f"risk_{risk_level.lower()}", lang)
    summary = get_text(f"risk_{risk_level.lower()}_summary", lang)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "badge_class": meta["badge_class"],
        "color": meta["color"],
        "icon": meta["icon"],
        "summary": summary,
        "reasons": reasons,
        "actions": actions,
        "matched_count": len(matched_questions),
        "total_questions": len(PHONE_QUESTIONS)
    }
