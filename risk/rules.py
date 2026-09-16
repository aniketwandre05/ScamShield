"""
Rule-Based Suspicious Indicator Detector
Detects specific high-risk patterns such as OTP requests, financial demands, fake urgency, and impersonation.
"""

import re
from typing import List, Dict, Any


# Heuristic rule patterns with severity weights and human explanations
RULES_DEFINITION = [
    {
        "id": "RULE_OTP_REQUEST",
        "category": "Credential Theft",
        "weight": 25,
        "patterns": [
            r'\b(?:share|send|provide|enter|submit|verify|input)\b.*?\b(?:otp|one[- ]time[- ]password|pin|security[- ]code|2fa[- ]code)\b',
            r'\b(?:one[- ]time[- ]password|verification[- ]code)\s+(?:is\s+required|needed|to\s+unlock)\b',
            r'\b(?:your\s+)?(?:otp|verification\s+code)\s+is\s+\d+\b',
            r'(?:ओटीपी|OTP|पासवर्ड|पिन|सुरक्षा\s*कोड|व्हेरिफिकेशन\s*कोड).*?(?:शेअर|पाठवा|द्या|सांगा|नोंदवा|करा|टाका)',
            r'(?:तुमचा\s*)?(?:ओटीपी|OTP)\s*(?:आहे|सांगा|द्या)',
            r'(?:ओटीपी|OTP|पासवर्ड|पिन|सुरक्षा\s*कोड|वेरिफिकेशन\s*कोड).*?(?:शेयर|भेजें|बताएं|दर्ज|साझा|करें|डालें)',
            r'(?:आपका\s*)?(?:ओटीपी|OTP)\s*(?:है|बताएं|दें)',
            r'\botp\s+(?:share|send|batao|bhejo|sanga|pathva|dya)\b'
        ],
        "reason": "Requests your One-Time Password (OTP), security code, or PIN.",
        "reason_mr": "तुमचा वन-टाईम पासवर्ड (OTP), सुरक्षा कोड किंवा पिन मागितला आहे.",
        "reason_hi": "आपका वन-टाइम पासवर्ड (OTP), सुरक्षा कोड या पिन मांगा गया है।",
        "action": "Never share OTPs, PINs, or verification codes with anyone, even if they claim to be from your bank.",
        "action_mr": "बँकेचे अधिकारी असल्याचे सांगत असले तरी कोणाशीही OTP, पिन किंवा सुरक्षा कोड कधीही शेअर करू नका.",
        "action_hi": "बैंक अधिकारी होने का दावा करने पर भी किसी के साथ OTP, पिन या सुरक्षा कोड कभी साझा न करें।"
    },
    {
        "id": "RULE_FINANCIAL_DEMAND",
        "category": "Financial Request",
        "weight": 25,
        "patterns": [
            r'\b(?:debit\s+card|credit\s+card|cvv|card\s+number|routing\s+number)\s+(?:number|details|is\s+required)\b',
            r'\b(?:wire\s+transfer|western\s+union|moneygram|gift\s+card|itunes\s+card|google\s+play\s+card|crypto|bitcoin|usdt)\b',
            r'\b(?:send\s+money|transfer\s+funds|unpaid\s+invoice|claim\s+fee|processing\s+fee)\b',
            r'(?:बँक\s*खाते|कार्ड\s*नंबर|डेबिट\s*कार्ड|क्रेडिट\s*कार्ड|सीव्हीव्ही|CVV|पैसे\s*पाठवा|पैसे\s*ट्रान्सफर|गिफ्ट\s*कार्ड|फी\s*भरा|शुल्क|पॅन\s*कार्ड|खाते\s*क्रमांक)',
            r'(?:पैसे\s*(?:पाठवा|द्या|भरा)|ट्रान्सफर\s*करा)',
            r'(?:बैंक\s*खाता|कार्ड\s*नंबर|डेबिट\s*कार्ड|क्रेडिट\s*कार्ड|सीवीवी|CVV|पैसे\s*भेजें|पैसे\s*ट्रांसफर|गिफ्ट\s*कार्ड|शुल्क\s*भुगतान|पैन\s*कार्ड|खाता\s*संख्या)',
            r'(?:पैसे\s*(?:भेजें|दें|डालें)|ट्रांसफर\s*करें)',
            r'\b(?:paise\s+(?:bhejo|transfer|pathva|dya)|bank\s+khata|bank\s+khate|gift\s+card)\b'
        ],
        "reason": "Asks for bank details, card numbers, or payments via wire transfer / gift cards.",
        "reason_mr": "बँक खात्याचे तपशील, कार्ड नंबर किंवा ट्रान्सफर/गिफ्ट कार्डद्वारे पैशांची मागणी केली आहे.",
        "reason_hi": "बैंक खाते का विवरण, कार्ड नंबर या ट्रांसफर/गिफ्ट कार्ड के माध्यम से भुगतान मांगा गया है।",
        "action": "Do not make payments or provide banking credentials. Banks and legitimate agencies never demand payment via gift cards or wire transfers.",
        "action_mr": "कोणतेही पैसे पाठवू नका किंवा बँक तपशील देऊ नका. अधिकृत संस्था कधीही गिफ्ट कार्ड किंवा संशयास्पद ट्रान्सफर मागत नाहीत.",
        "action_hi": "कोई भुगतान न करें और न ही बैंक विवरण दें। बैंक या एजेंसियां कभी भी गिफ्ट कार्ड या अज्ञात ट्रांसफर द्वारा पैसे नहीं मांगती हैं।"
    },
    {
        "id": "RULE_URGENCY_THREAT",
        "category": "High Pressure / Urgency",
        "weight": 20,
        "patterns": [
            r'\b(?:urgent|immediately|within\s+\d+\s+(?:hours?|mins?|minutes?))\s*[:!]?',
            r'\b(?:account|card|access)\s+(?:has\s+been\s+)?(?:suspended|blocked|locked|terminated|closed)\b',
            r'\b(?:legal\s+action|law\s+enforcement|arrest\s+warrant|police\s+case|court\s+notice)\b',
            r'\b(?:final\s+warning|last\s+notice|immediate\s+action\s+required)\b',
            r'(?:तातडीने|त्वरित|ताबडतोब|तासांत|खाते\s*(?:ब्लॉक|बंद|निलंबित)|अटक|पोलीस\s*कारवाई|कायदेशीर\s*कारवाई|शेवटची\s*नोटीस|अंतिम\s*इशारा|वीज\s*(?:खंडित|बंद|कट)|कनेक्शन\s*बंद)',
            r'(?:तुरंत|तत्काल|घंटों\s*में|खाता\s*(?:ब्लॉक|बंद|निलंबित)|गिरफ्तारी|पुलिस\s*कार्रवाई|कानूनी\s*कार्रवाई|अंतिम\s*चेतावनी|बिजली\s*(?:कट|बंद)|कनेक्शन\s*काटा)',
            r'\b(?:turant|tatkal|khata\s+block|account\s+band|bijli\s+kat|police\s+case)\b'
        ],
        "reason": "Creates artificial urgency or threatens account closure / legal consequences.",
        "reason_mr": "तातडीने कारवाई करण्यासाठी दबाव आणला आहे किंवा खाते बंद करण्याची / कारवाईची धमकी दिली आहे.",
        "reason_hi": "तुरंत कार्रवाई करने का दबाव बनाया गया है या खाता बंद/कानूनी कार्रवाई की धमकी दी गई है।",
        "action": "Stay calm. Scammers use artificial panic to force quick decisions. Legitimate companies give reasonable time to resolve issues.",
        "action_mr": "शांत राहा. घाईगडबडीत निर्णय घेण्यासाठी अशी भीती दाखवली जाते. अधिकृत कंपन्या समस्या सोडवण्यासाठी वेळ देतात.",
        "action_hi": "शांत रहें। जल्दबाजी में गलत कदम उठाने के लिए ऐसा डर दिखाया जाता है। वैध कंपनियां उचित समय देती हैं।"
    },
    {
        "id": "RULE_PRIZE_REWARD",
        "category": "Unrealistic Reward",
        "weight": 20,
        "patterns": [
            r'\b(?:congratulations|congrats)\b.*?\b(?:won|winner|lottery|prize|reward)\b',
            r'\b(?:you\s+have\s+been\s+selected\s+to\s+receive|claim\s+your\s+(?:prize|reward|gift|bonus))\b',
            r'\b(?:unclaimed\s+funds|inheritance\s+of|\$\d+,\d+\s+cash\s+prize)\b',
            r'(?:अभिनंदन|तुम्ही\s*जिंकले|लॉटरी|बक्षीस|इनाम|कॅश\s*प्राईझ|बोनस|विजेते|दावा\s*करा)',
            r'(?:बधाई|आपने\s*जीता|लॉटरी|इनाम|पुरस्कार|कैश\s*प्राइज|बोनस|विजेता|दावा\s*करें)',
            r'\b(?:badhai|abhinandan|lottery\s+lagi|prize\s+mila|jeeta|jinkle)\b'
        ],
        "reason": "Offers unexpected prizes, lottery winnings, or free money.",
        "reason_mr": "अनपेक्षित बक्षीस, लॉटरी किंवा मोफत पैशांचे आमिष दाखवले आहे.",
        "reason_hi": "अप्रत्याशित इनाम, लॉटरी या मुफ्त पैसों का लालच दिया गया है।",
        "action": "If you didn't enter a contest, you didn't win. Never pay fees or share personal details to claim a 'prize'.",
        "action_mr": "कोणत्याही स्पर्धेत भाग न घेता बक्षीस मिळत नाही. बक्षीसासाठी कोणतेही शुल्क भरू नका किंवा माहिती देऊ नका.",
        "action_hi": "बिना किसी प्रतियोगिता के इनाम नहीं मिलता। इनाम के नाम पर कभी भी शुल्क न दें और न ही जानकारी साझा करें।"
    },
    {
        "id": "RULE_IMPERSONATION",
        "category": "Brand Impersonation",
        "weight": 15,
        "patterns": [
            r'\b(?:irs|customs|social\s+security\s+administration|tax\s+department)\b',
            r'\b(?:amazon\s+security|paypal\s+security|apple\s+support|microsoft\s+support|netflix\s+billing)\b.*?\b(?:alert|urgent|verify|locked|suspend)\b',
            r'\b(?:kyc\s+update\s+required|pan\s+card\s+blocked|account\s+verification\s+team)\b',
            r'(?:केवायसी\s*(?:अपडेट|निलंबित|व्हेरिफिकेशन)|KYC\s*अपडेट|पॅन\s*कार्ड\s*(?:ब्लॉक|लिंक)|बँक\s*अधिकारी|ग्राहक\s*सेवा|विद्युत\s*विभाग|महावितरण|इन्कम\s*टॅक्स)',
            r'(?:केवाईसी\s*(?:अपडेट|निलंबित|सत्यापन)|KYC\s*अपडेट|पैन\s*कार्ड\s*(?:ब्लॉक|लिंक)|बैंक\s*अधिकारी|कस्टमर\s*केयर|बिजली\s*विभाग|आयकर\s*विभाग|इनकम\s*टैक्स)',
            r'\b(?:kyc\s+update|pan\s+card\s+block|bijli\s+bill|bank\s+officer)\b'
        ],
        "reason": "Claims to be from a well-known institution, government body, or tech support.",
        "reason_mr": "प्रसिद्ध संस्था, बँक, सरकारी विभाग किंवा विद्युत मंडळाचे असल्याचा बनावट दावा केला आहे.",
        "reason_hi": "किसी प्रसिद्ध संस्था, बैंक, सरकारी विभाग या बिजली बोर्ड का होने का फर्जी दावा किया गया है।",
        "action": "Verify directly by visiting the organization's official website or calling the customer service number on your actual physical card/bill.",
        "action_mr": "संस्थेच्या अधिकृत वेबसाइटला भेट देऊन किंवा अधिकृत बिल/पासबुकवरील क्रमांकावर संपर्क साधून थेट खात्री करा.",
        "action_hi": "संस्था की आधिकारिक वेबसाइट पर जाकर या अपने बिल/पासबुक पर दिए गए नंबर पर कॉल करके सीधे पुष्टि करें।"
    },
    {
        "id": "RULE_SUSPICIOUS_LINK",
        "category": "Link Risk",
        "weight": 15,
        "patterns": [
            r'https?://(?:bit\.ly|tinyurl\.com|t\.co|cutt\.ly|is\.gd|tiny\.cc)/[a-zA-Z0-9_-]+',
            r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?(?:/[^\s]*)?',
            r'\b(?:click\s+here\s+to\s+verify|tap\s+here\s+to\s+unlock)\b',
            r'(?:येथे\s*क्लिक\s*करा|लिंकवर\s*क्लिक\s*करा|खाते\s*(?:सुरू|अनलॉक)\s*करण्यासाठी\s*क्लिक\s*करा)',
            r'(?:यहाँ\s*क्लिक\s*करें|लिंक\s*पर\s*क्लिक\s*करें|खाता\s*(?:चालू|अनलॉक)\s*करने\s*के\s*लिए\s*क्लिक\s*करें)',
            r'\b(?:click\s+kare|click\s+kara|link\s+khol|link\s+open)\b'
        ],
        "reason": "Contains a shortened link or urges you to click an unverified address.",
        "reason_mr": "शॉर्ट लिंक समाविष्ट आहे किंवा असत्यापित लिंकवर क्लिक करण्याचा आग्रह केला आहे.",
        "reason_hi": "शॉर्ट लिंक शामिल है या किसी असत्यापित लिंक पर क्लिक करने का दबाव दिया गया है।",
        "action": "Do not click on links sent in unsolicited messages. Type the official website address directly in your browser.",
        "action_mr": "अनोळखी संदेशांमधील कोणत्याही लिंकवर क्लिक करू नका. अधिकृत वेबसाइटचा पत्ता थेट ब्राउझरमध्ये टाईप करा.",
        "action_hi": "अज्ञात संदेशों में भेजे गए किसी भी लिंक पर क्लिक न करें। ब्राउज़र में सीधे आधिकारिक पता टाइप करें।"
    }
]

# Compile patterns for performance
COMPILED_RULES = []
for r in RULES_DEFINITION:
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in r["patterns"]]
    COMPILED_RULES.append({
        "id": r["id"],
        "category": r["category"],
        "weight": r["weight"],
        "patterns": compiled_patterns,
        "reason": r["reason"],
        "reason_mr": r.get("reason_mr", r["reason"]),
        "reason_hi": r.get("reason_hi", r["reason"]),
        "action": r["action"],
        "action_mr": r.get("action_mr", r["action"]),
        "action_hi": r.get("action_hi", r["action"])
    })


def evaluate_rules(text: str, lang: str = "en") -> Dict[str, Any]:
    """
    Evaluates text against heuristic scam patterns in English, Marathi, Hindi, and Hinglish/Marathlish.
    Returns matched rules, cumulative rule score, reasons, and actions in the requested language.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "matched_rules": [],
            "rule_score": 0,
            "reasons": [],
            "actions": []
        }

    matched = []
    reasons = []
    actions = []
    total_weight = 0

    for rule in COMPILED_RULES:
        for pattern in rule["patterns"]:
            if pattern.search(text):
                matched.append(rule["id"])
                
                # Pick localized reason and action
                if lang == "mr":
                    reasons.append(rule["reason_mr"])
                    actions.append(rule["action_mr"])
                elif lang == "hi":
                    reasons.append(rule["reason_hi"])
                    actions.append(rule["action_hi"])
                else:
                    reasons.append(rule["reason"])
                    actions.append(rule["action"])
                    
                total_weight += rule["weight"]
                break  # Don't double count same rule

    # Cap rule score to 100
    rule_score = min(100, total_weight)

    return {
        "matched_rules": matched,
        "rule_score": rule_score,
        "reasons": reasons,
        "actions": actions
    }
