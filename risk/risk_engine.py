"""
Unified Hybrid Risk Assessment Engine
Combines specialized machine learning models (Text & URL) with rule-based heuristics to compute
an Estimated Risk Score (0-100), Risk Level, transparent reasoning, and actionable safety steps.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RISK_THRESHOLDS, RISK_LEVEL_META
from ml.prediction import sms_predictor, email_predictor, url_predictor
from ml.preprocessing import extract_urls
from risk.rules import evaluate_rules
from risk.explanations import build_explanation_summary


TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "wikipedia.org", "github.com", "microsoft.com",
    "apple.com", "netflix.com", "amazon.com", "usps.com", "ups.com", "fedex.com",
    "chase.com", "paypal.com"
}


def is_domain_trusted(url: str) -> bool:
    """Checks if a URL belongs to a verified legitimate domain."""
    try:
        parse_target = url if url.startswith(("http://", "https://")) else "https://" + url
        parsed = urlparse(parse_target)
        host = (parsed.hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host in TRUSTED_DOMAINS
    except Exception:
        return False


RISK_MESSAGES = {
    "ip_reason": {
        "en": "The link uses a raw IP address instead of a recognized domain name.",
        "mr": "हा लिंक अधिकृत डोमेन नावाऐवजी थेट आयपी (IP) ॲड्रेस वापरत आहे.",
        "hi": "यह लिंक किसी मान्यता प्राप्त डोमेन के बजाय सीधे आईपी (IP) एड्रेस का उपयोग करता है।"
    },
    "ip_action": {
        "en": "Never enter passwords or personal details on websites using raw IP addresses.",
        "mr": "थेट आयपी ॲड्रेस वापरणाऱ्या वेबसाइटवर कधीही पासवर्ड किंवा वैयक्तिक माहिती टाकू नका.",
        "hi": "सीधे आईपी एड्रेस वाली वेबसाइटों पर कभी भी पासवर्ड या व्यक्तिगत विवरण दर्ज न करें।"
    },
    "shortened_reason": {
        "en": "The link uses a URL shortener service which hides the true destination.",
        "mr": "हा लिंक मूळ वेबसाइट लपवण्यासाठी शॉर्ट यूआरएल सेवेचा वापर करतो.",
        "hi": "यह लिंक असली वेबसाइट को छिपाने के लिए यूआरएल शॉर्टनर सेवा का उपयोग करता है।"
    },
    "shortened_action": {
        "en": "Be cautious with shortened links; expand them before clicking.",
        "mr": "शॉर्ट लिंक्सबाबत सावध राहा; क्लिक करण्यापूर्वी त्यांची खात्री करा.",
        "hi": "शॉर्ट किए गए लिंक से सावधान रहें; क्लिक करने से पहले उनकी जांच करें।"
    },
    "subdomain_reason": {
        "en": "Excessive subdomains detected ({count} levels), often used in phishing.",
        "mr": "अनेक सबडोमेन आढळले ({count} स्तर), जे फिशिंगसाठी मोठ्या प्रमाणावर वापरले जातात.",
        "hi": "अत्यधिक सबडोमेन पाए गए ({count} स्तर), जो अक्सर फ़िशिंग में उपयोग किए जाते हैं।"
    },
    "no_https_reason": {
        "en": "The link does not use secure HTTPS encryption (http://).",
        "mr": "हा लिंक सुरक्षित HTTPS एन्क्रिप्शन वापरत नाही (http://).",
        "hi": "यह लिंक सुरक्षित HTTPS एन्क्रिप्शन का उपयोग नहीं करता है (http://)।"
    },
    "banking_kw_reason": {
        "en": "Contains security/banking keywords ({count} detected) in an unverified link.",
        "mr": "असत्यापित लिंकमध्ये बँक/सुरक्षा संबंधित शब्द ({count} आढळले) आहेत.",
        "hi": "असत्यापित लिंक में सुरक्षा/बैंकिंग संबंधित शब्द ({count} पाए गए) शामिल हैं।"
    },
    "url_ml_scam_reason": {
        "en": "Machine learning URL classifier detected structural patterns consistent with phishing or malicious sites.",
        "mr": "मशीन लर्निंग मॉडेलने या लिंकमध्ये फिशिंग किंवा धोकादायक वेबसाइटसारखी रचना ओळखली आहे.",
        "hi": "मशीन लर्निंग मॉडल ने इस लिंक में फ़िशिंग या दुर्भावनापूर्ण वेबसाइट जैसी संरचना की पहचान की है।"
    },
    "url_ml_scam_action": {
        "en": "Do not open this website in your browser.",
        "mr": "ही वेबसाइट तुमच्या ब्राउझरमध्ये उघडू नका.",
        "hi": "इस वेबसाइट को अपने ब्राउज़र में न खोलें।"
    },
    "embedded_url_scam_reason": {
        "en": "Embedded link within the message was classified as high risk by our URL security model.",
        "mr": "संदेशातील लिंक आमच्या सुरक्षा मॉडेलद्वारे अत्यंत धोकादायक आढळली आहे.",
        "hi": "संदेश में दिया गया लिंक हमारे सुरक्षा मॉडल द्वारा उच्च जोखिम वाला पाया गया है।"
    },
    "embedded_url_scam_action": {
        "en": "Do not click or tap the link in the message.",
        "mr": "संदेशातील कोणत्याही लिंकवर क्लिक करू नका.",
        "hi": "संदेश में दिए गए लिंक पर क्लिक न करें।"
    },
    "text_ml_scam_reason": {
        "en": "Machine learning text model identified spam/scam wording patterns.",
        "mr": "मशीन लर्निंग मॉडेलने या संदेशात फसवणुकीची भाषा आणि पद्धती ओळखल्या आहेत.",
        "hi": "मशीन लर्निंग मॉडल ने इस संदेश में धोखाधड़ी की भाषा और पैटर्न की पहचान की है।"
    },
    "sender_mismatch_reason": {
        "en": "Sender address '{sender}' does not match official service domain.",
        "mr": "पाठवणाऱ्याचा पत्ता '{sender}' अधिकृत सेवेच्या डोमेनशी जुळत नाही.",
        "hi": "भेजने वाले का पता '{sender}' आधिकारिक सेवा के डोमेन से मेल नहीं खाता है।"
    },
    "sender_mismatch_action": {
        "en": "Check the sender email address carefully. Impersonators often use free or misnamed email accounts.",
        "mr": "पाठवणाऱ्याचा ईमेल काळजीपूर्वक तपासा. तोतया व्यक्ती अनेकदा मोफत किंवा बनावट ईमेल खाती वापरतात.",
        "hi": "भेजने वाले का ईमेल ध्यान से जांचें। धोखेबाज अक्सर मुफ्त या फर्जी ईमेल खातों का उपयोग करते हैं।"
    },
    "email_embedded_url_reason": {
        "en": "Links inside this email were flagged as suspicious by our URL security classifier.",
        "mr": "या ईमेलमधील लिंक्स आमच्या सुरक्षा तपासणीत संशयास्पद आढळल्या आहेत.",
        "hi": "इस ईमेल में दिए गए लिंक हमारी सुरक्षा जांच में संदिग्ध पाए गए हैं।"
    },
    "email_embedded_url_action": {
        "en": "Do not click any buttons or links in this email.",
        "mr": "या ईमेलमधील कोणत्याही बटणावर किंवा लिंकवर क्लिक करू नका.",
        "hi": "इस ईमेल के किसी भी बटन या लिंक पर क्लिक न करें।"
    },
    "email_ml_phishing_reason": {
        "en": "Machine learning email classifier identified phishing intent in email content.",
        "mr": "मशीन लर्निंग ईमेल मॉडेलने या मजकुरात फिशिंगचा हेतू ओळखला आहे.",
        "hi": "मशीन लर्निंग ईमेल मॉडल ने इस सामग्री में फ़िशिंग के इरादे की पहचान की है।"
    }
}


def _get_msg(key: str, lang: str = "en", **kwargs) -> str:
    """Helper to retrieve localized risk explanation string."""
    msg_dict = RISK_MESSAGES.get(key, {})
    template = msg_dict.get(lang, msg_dict.get("en", ""))
    if kwargs:
        return template.format(**kwargs)
    return template


def compute_hybrid_risk(
    content_type: str,
    text: str = "",
    subject: str = "",
    body: str = "",
    sender: str = "",
    url: str = "",
    override_urls: Optional[List[str]] = None,
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Main risk assessment entry point for SMS, Email, URL, or Screenshot inputs.
    Supports multi-language explanations for 'en', 'mr', and 'hi'.
    """
    valid_lang = lang if lang in ("en", "mr", "hi") else "en"
    reasons = []
    actions = []
    ml_results = {}
    
    # =========================================================================
    # 1. Evaluate Single URL module directly
    # =========================================================================
    if content_type == "url":
        target_url = url.strip()
        
        # If target_url contains surrounding text (from screenshot OCR), extract clean URL
        if ' ' in target_url or '\n' in target_url:
            found_urls = extract_urls(target_url)
            if found_urls:
                target_url = found_urls[0]
            else:
                for word in target_url.split():
                    w_clean = word.strip('.,!?:;)"\'>]}')
                    if '.' in w_clean and len(w_clean) > 4:
                        target_url = w_clean
                        break
                        
        url_pred = url_predictor.predict(target_url)
        ml_results["url"] = url_pred
        
        # Rule evaluation on clean URL
        rule_eval = evaluate_rules(target_url, lang=valid_lang)
        feats = url_pred.get("features", {})
        
        # Check if URL belongs to a trusted verified domain
        trusted = is_domain_trusted(target_url)
        has_ip = bool(feats.get("has_ip_address"))
        is_short = bool(feats.get("is_shortened"))
        
        if trusted and not has_ip and not is_short:
            raw_score = 5
        elif url_pred.get("available", False):
            ml_prob = url_pred["probability"]
            if ml_prob < 0.20 and rule_eval["rule_score"] == 0:
                raw_score = ml_prob * 25.0
            elif has_ip or is_short or ml_prob > 0.60:
                raw_score = max(68, (0.70 * ml_prob * 100) + (0.30 * rule_eval["rule_score"]))
            else:
                raw_score = (0.70 * ml_prob * 100) + (0.30 * rule_eval["rule_score"])
        else:
            raw_score = rule_eval["rule_score"]
            
        # Specific URL reasons
        if feats.get("has_ip_address"):
            reasons.append(_get_msg("ip_reason", valid_lang))
            actions.append(_get_msg("ip_action", valid_lang))
        if feats.get("is_shortened"):
            reasons.append(_get_msg("shortened_reason", valid_lang))
            actions.append(_get_msg("shortened_action", valid_lang))
        if feats.get("subdomain_count", 0) >= 3:
            reasons.append(_get_msg("subdomain_reason", valid_lang, count=feats.get('subdomain_count')))
        if not feats.get("has_https") and not target_url.lower().startswith("https://") and not trusted:
            reasons.append(_get_msg("no_https_reason", valid_lang))
        if feats.get("suspicious_keyword_count", 0) > 0 and not trusted:
            reasons.append(_get_msg("banking_kw_reason", valid_lang, count=feats.get('suspicious_keyword_count')))
            
        reasons.extend(rule_eval["reasons"])
        actions.extend(rule_eval["actions"])
        
        if url_pred.get("prediction") == 1 and not trusted:
            reasons.append(_get_msg("url_ml_scam_reason", valid_lang))
            actions.append(_get_msg("url_ml_scam_action", valid_lang))
            
        risk_score = int(round(min(100, max(0, raw_score))))
        
    # =========================================================================
    # 2. Evaluate SMS / WhatsApp module
    # =========================================================================
    elif content_type == "sms":
        raw_text = text.strip()
        sms_pred = sms_predictor.predict(raw_text)
        ml_results["sms"] = sms_pred
        
        # Evaluate rules
        rule_eval = evaluate_rules(raw_text, lang=valid_lang)
        reasons.extend(rule_eval["reasons"])
        actions.extend(rule_eval["actions"])
        
        # Extract embedded URLs
        embedded_urls = override_urls if override_urls is not None else extract_urls(raw_text)
        url_predictions = []
        max_url_prob = 0.0
        
        for u in embedded_urls:
            u_pred = url_predictor.predict(u)
            url_predictions.append(u_pred)
            if u_pred.get("available") and u_pred.get("probability", 0) > max_url_prob:
                max_url_prob = u_pred["probability"]
                
        ml_results["embedded_urls"] = url_predictions
        
        # Combine Text ML + URL ML + Rules
        if sms_pred.get("available", False):
            text_prob = sms_pred["probability"]
            has_scam_rules = len(rule_eval["matched_rules"]) > 0
            
            if not has_scam_rules and max_url_prob < 0.35 and text_prob < 0.60:
                raw_score = text_prob * 25.0  # safe appointment/friend messages -> LOW RISK (0-15)
            elif has_scam_rules or max_url_prob >= 0.70:
                base_score = max(68, (0.45 * text_prob * 100) + (0.35 * max_url_prob * 100) + (0.20 * rule_eval["rule_score"]))
                raw_score = min(100, base_score + 10)
                if max_url_prob >= 0.7:
                    reasons.append(_get_msg("embedded_url_scam_reason", valid_lang))
                    actions.append(_get_msg("embedded_url_scam_action", valid_lang))
            else:
                raw_score = (0.60 * text_prob * 100) + (0.40 * rule_eval["rule_score"])
                
            if sms_pred.get("prediction") == 1 and has_scam_rules:
                reasons.append(_get_msg("text_ml_scam_reason", valid_lang))
        else:
            raw_score = rule_eval["rule_score"]
            
        risk_score = int(round(min(100, max(0, raw_score))))
        
    # =========================================================================
    # 3. Evaluate Email module
    # =========================================================================
    elif content_type == "email":
        if not body and text:
            body = text
            
        combined_text = f"{subject} {body}".strip()
        email_pred = email_predictor.predict(subject=subject, body=body, sender=sender)
        ml_results["email"] = email_pred
        
        # Rule evaluation
        rule_eval = evaluate_rules(combined_text, lang=valid_lang)
        reasons.extend(rule_eval["reasons"])
        actions.extend(rule_eval["actions"])
        
        # Extract embedded URLs
        embedded_urls = override_urls if override_urls is not None else extract_urls(combined_text)
        url_predictions = []
        max_url_prob = 0.0
        
        for u in embedded_urls:
            u_pred = url_predictor.predict(u)
            url_predictions.append(u_pred)
            # Only count as risky URL if not a trusted domain
            if not is_domain_trusted(u) and u_pred.get("available") and u_pred.get("probability", 0) > max_url_prob:
                max_url_prob = u_pred["probability"]
                
        ml_results["embedded_urls"] = url_predictions
        
        # Check sender domain matching & brand verification
        sender_is_mismatched = False
        sender_is_trusted = False
        
        if sender and "@" in sender:
            sender_lower = sender.lower()
            # Verified official senders
            if any(trusted in sender_lower for trusted in ["@netflix.com", "@google.com", "@apple.com", "@amazon.com", "@usps.com", "@chase.com"]):
                sender_is_trusted = True
                
            if any(brand in combined_text.lower() for brand in ["paypal", "amazon", "apple", "netflix", "bank", "chase"]):
                if not any(trusted in sender_lower for trusted in ["@paypal.com", "@amazon.com", "@apple.com", "@netflix.com", "@chase.com", "@usps.com"]):
                    sender_is_mismatched = True
                    reasons.append(_get_msg("sender_mismatch_reason", valid_lang, sender=sender))
                    actions.append(_get_msg("sender_mismatch_action", valid_lang))
                    rule_eval["rule_score"] = min(100, rule_eval["rule_score"] + 35)
                    
        if email_pred.get("available", False):
            text_prob = email_pred["probability"]
            has_scam_rules = len(rule_eval["matched_rules"]) > 0 or sender_is_mismatched
            
            if (sender_is_trusted or is_domain_trusted(combined_text)) and not has_scam_rules and max_url_prob < 0.50:
                raw_score = 10  # legitimate billing / notification receipt -> LOW RISK
            elif not has_scam_rules and max_url_prob < 0.40 and text_prob < 0.50:
                raw_score = text_prob * 25.0
            elif has_scam_rules or max_url_prob >= 0.70 or text_prob >= 0.65:
                base_score = max(68, (0.45 * text_prob * 100) + (0.35 * max_url_prob * 100) + (0.20 * rule_eval["rule_score"]))
                raw_score = min(100, base_score + 10)
                if max_url_prob >= 0.7:
                    reasons.append(_get_msg("email_embedded_url_reason", valid_lang))
                    actions.append(_get_msg("email_embedded_url_action", valid_lang))
            else:
                raw_score = (0.60 * text_prob * 100) + (0.40 * rule_eval["rule_score"])
                
            if email_pred.get("prediction") == 1 and has_scam_rules:
                reasons.append(_get_msg("email_ml_phishing_reason", valid_lang))
        else:
            raw_score = rule_eval["rule_score"]
            
        risk_score = int(round(min(100, max(0, raw_score))))
        
    else:
        risk_score = 0

    # Risk Level mapping
    if risk_score <= RISK_THRESHOLDS["LOW_MAX"]:
        risk_level = "LOW"
    elif risk_score <= RISK_THRESHOLDS["MEDIUM_MAX"]:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    meta = RISK_LEVEL_META[risk_level]
    
    # Generate structured explanations & safety checklist
    explanation = build_explanation_summary(
        risk_level=risk_level,
        reasons=reasons,
        actions=actions,
        lang=valid_lang
    )
    
    return {
        "content_type": content_type,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_label": meta["label"],
        "badge_class": meta["badge_class"],
        "color": meta["color"],
        "icon": meta["icon"],
        "summary": meta["summary"],
        "reasons": explanation["reasons"],
        "actions": explanation["actions"],
        "ml_results": ml_results
    }
