"""
ScamShield Privacy & Data Protection Module
Provides automatic masking for sensitive personal data (credit card numbers,
CVVs, OTP codes, and passwords) and HTML-safe suspicious keyword highlighting.
"""

import re
import html


def mask_sensitive_data(text: str) -> str:
    """
    Detects and masks sensitive credentials in user input to adhere to
    HCI trust, safety, and ethical data handling standards.
    """
    if not text:
        return ""

    masked = text

    # 1. Mask 13-16 digit payment card numbers (preserving last 4 digits)
    def _mask_card(match):
        raw = match.group(0)
        digits = re.sub(r'\D', '', raw)
        if len(digits) in (13, 14, 15, 16):
            return f"****-****-****-{digits[-4:]}"
        return raw

    masked = re.sub(r'\b(?:\d[ -]*?){13,16}\b', _mask_card, masked)

    # 2. Mask CVV / CVC security codes
    masked = re.sub(
        r'(?i)\b(cvv|cvc|security\s*code|सुरक्षा\s*कोड)[:\s]*\d{3,4}\b',
        r'\1: ***',
        masked
    )

    # 3. Mask explicit OTP codes
    masked = re.sub(
        r'(?i)\b(otp|one\s*time\s*password|pin|ओटीपी|पिन)[:\s]*\d{4,8}\b',
        r'\1: ******',
        masked
    )

    # 4. Mask explicit passwords
    masked = re.sub(
        r'(?i)\b(password|passwd|pwd|पासवर्ड)[:\s]*\S+',
        r'\1: ********',
        masked
    )

    return masked


SUSPICIOUS_WORDS_PATTERN = re.compile(
    r'(?i)\b('
    # English keywords
    r'urgent|urgently|immediately|immediate|blocked|block|locked|suspend|suspended|'
    r'verify|verification|verifying|re-verify|kyc|pan|aadhaar|update|confirm|'
    r'otp|pin|password|passwd|credentials|cvv|security code|'
    r'lottery|winner|won|prize|jackpot|reward|gift card|bonus|congratulations|'
    r'wire transfer|penalty|fine|arrest|police|cbi|customs|fbi|court|lawsuit|legal action|'
    r'account closure|deactivation|electricity bill|power cut|disconnected|'
    r'click here|claim now|claim prize|http[s]?://\S+'
    r')\b|'
    # Devanagari (Marathi & Hindi) keywords
    r'('
    r'तात्काळ|त्वरित|तातडीने|ब्लॉक|बंद|निलंबित|व्हेरिफाय|सत्यापित|अपडेट|केवायसी|'
    r'ओटीपी|पिन|पासवर्ड|लॉटरी|विजेता|जिंकले|बक्षीस|इनाम|दंड|अटक|पोलीस|'
    r'खाते|खाता|पैसे पाठवा|वीज खंडित|वीज बिल'
    r')',
    re.UNICODE
)


def highlight_suspicious_keywords(text: str) -> str:
    """
    HTML-escapes text for XSS safety and highlights suspicious fraud keywords
    with an accessible <mark class="suspicious-keyword"> tag.
    """
    if not text:
        return ""

    escaped = html.escape(text)

    def _replace_kw(m):
        return f'<mark class="suspicious-keyword">{m.group(0)}</mark>'

    return SUSPICIOUS_WORDS_PATTERN.sub(_replace_kw, escaped)
