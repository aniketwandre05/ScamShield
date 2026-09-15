"""
Explanation and Recommendation Generator
Transforms technical ML outputs and matched heuristics into empathetic, plain-language guidance.
"""

from typing import List, Dict, Any


DEFAULT_SAFE_ACTIONS = [
    "Always verify unexpected messages through official customer support channels before taking action.",
    "Do not click on links or download attachments from unfamiliar or unexpected senders.",
    "Remember that legitimate institutions will never ask for your passwords or full PIN."
]

DEFAULT_SUSPICIOUS_ACTIONS = [
    "Do NOT click any links or download any files attached to this message.",
    "Do NOT reply, call phone numbers provided in the message, or share any personal details.",
    "If this claims to be from a service you use (bank, email, shopping), log into your account directly from your browser to check for real notifications."
]

DEFAULT_HIGH_RISK_ACTIONS = [
    "DO NOT click any links, open attachments, or reply to this message.",
    "DO NOT share any One-Time Password (OTP), credit card number, PIN, or bank information.",
    "Block the sender and report the message as spam or phishing in your email/messaging app.",
    "If you have already clicked a link or shared information, immediately contact your bank and change your account passwords."
]


def build_explanation_summary(
    risk_level: str,
    reasons: List[str],
    actions: List[str],
    has_urls: bool = False,
    url_risk_level: str = "LOW"
) -> Dict[str, Any]:
    """
    Constructs a clear visual explanation structure:
    - Clean deduplicated 'Why is this suspicious?' list
    - Prioritized 'What should you do?' checklist
    - Summary banner sentence
    """
    # Deduplicate reasons while preserving order
    unique_reasons = []
    for r in reasons:
        if r not in unique_reasons:
            unique_reasons.append(r)
            
    # If safe and no suspicious reasons found
    if not unique_reasons and risk_level == "LOW":
        unique_reasons = [
            "No aggressive scam phrases or urgent payment requests detected.",
            "Standard language structure with no identified threat or credential demand."
        ]
        
    # Deduplicate actions
    unique_actions = []
    for a in actions:
        if a not in unique_actions:
            unique_actions.append(a)
            
    # Add baseline safe guidance if empty
    if not unique_actions:
        if risk_level == "LOW":
            unique_actions = DEFAULT_SAFE_ACTIONS
        elif risk_level == "MEDIUM":
            unique_actions = DEFAULT_SUSPICIOUS_ACTIONS
        else:
            unique_actions = DEFAULT_HIGH_RISK_ACTIONS
            
    return {
        "reasons": unique_reasons,
        "actions": unique_actions
    }
