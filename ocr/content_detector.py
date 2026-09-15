"""
Screenshot Content Detector and Router
Determines whether OCR-extracted text resembles an SMS/WhatsApp message, an Email, or a standalone URL,
and extracts any embedded links for unified analysis.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ml.preprocessing import extract_urls


# Patterns characteristic of emails
EMAIL_HEADER_PATTERNS = [
    re.compile(r'^(?:from|to|subject|date|cc|bcc):\s*(.+)$', re.IGNORECASE | re.MULTILINE),
    re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    re.compile(r'\b(?:dear\s+(?:customer|user|member|sir|madam|client)|sincerely|best regards|kind regards)\b', re.IGNORECASE)
]

# Patterns characteristic of messaging apps (WhatsApp, SMS, Telegram)
MESSAGING_PATTERNS = [
    re.compile(r'\b(?:today|yesterday|\d{1,2}:\d{2}\s*(?:am|pm)?)\b', re.IGNORECASE),
    re.compile(r'\b(?:type a message|send message|delivered|read|typing\.\.\.)\b', re.IGNORECASE),
    re.compile(r'\b(?:otp|code is|do not share|valid for|expir(?:es|y))\b', re.IGNORECASE)
]


def detect_content_structure(text: str) -> Dict[str, Any]:
    """
    Analyzes OCR text and determines the primary content category:
    - 'url' : If text consists predominantly of a URL
    - 'email': If headers, email addresses, or formal email sign-offs are present
    - 'sms'  : Default for chat/text message structures
    
    Also extracts all embedded URLs for downstream multi-model risk assessment.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "primary_type": "sms",
            "urls": [],
            "has_urls": False,
            "sender": "",
            "subject": "",
            "body": ""
        }

    raw_text = text.strip()
    urls = extract_urls(raw_text)
    has_urls = len(urls) > 0

    # 1. Check if the entire text is essentially just a single URL
    words = raw_text.split()
    if len(words) <= 3 and has_urls and len(urls[0]) > len(raw_text) * 0.7:
        return {
            "primary_type": "url",
            "urls": urls,
            "has_urls": True,
            "sender": "",
            "subject": "",
            "body": raw_text
        }

    # 2. Check for Email characteristics
    email_score = 0
    sender = ""
    subject = ""

    # Look for From: / Subject:
    for line in raw_text.splitlines():
        line_clean = line.strip()
        from_match = re.match(r'^(?:from|sender):\s*(.+)$', line_clean, re.IGNORECASE)
        if from_match:
            sender = from_match.group(1).strip()
            email_score += 2

        subj_match = re.match(r'^(?:subject|re|fwd):\s*(.+)$', line_clean, re.IGNORECASE)
        if subj_match:
            subject = subj_match.group(1).strip()
            email_score += 2

    # Look for email address patterns
    email_addrs = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', raw_text)
    if email_addrs:
        email_score += len(email_addrs)
        if not sender:
            sender = email_addrs[0]

    # Look for formal email greetings/closings
    for pat in EMAIL_HEADER_PATTERNS:
        if pat.search(raw_text):
            email_score += 1

    # Decide primary type
    if email_score >= 2 or (sender and subject):
        primary_type = "email"
    else:
        primary_type = "sms"

    return {
        "primary_type": primary_type,
        "urls": urls,
        "has_urls": has_urls,
        "sender": sender,
        "subject": subject,
        "body": raw_text
    }
