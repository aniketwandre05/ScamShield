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
            r'\b(?:your\s+)?(?:otp|verification\s+code)\s+is\s+\d+\b'
        ],
        "reason": "Requests your One-Time Password (OTP), security code, or PIN.",
        "action": "Never share OTPs, PINs, or verification codes with anyone, even if they claim to be from your bank."
    },
    {
        "id": "RULE_FINANCIAL_DEMAND",
        "category": "Financial Request",
        "weight": 25,
        "patterns": [
            r'\b(?:debit\s+card|credit\s+card|cvv|card\s+number|routing\s+number)\s+(?:number|details|is\s+required)\b',
            r'\b(?:wire\s+transfer|western\s+union|moneygram|gift\s+card|itunes\s+card|google\s+play\s+card|crypto|bitcoin|usdt)\b',
            r'\b(?:send\s+money|transfer\s+funds|unpaid\s+invoice|claim\s+fee|processing\s+fee)\b'
        ],
        "reason": "Asks for bank details, card numbers, or payments via wire transfer / gift cards.",
        "action": "Do not make payments or provide banking credentials. Banks and legitimate agencies never demand payment via gift cards or wire transfers."
    },
    {
        "id": "RULE_URGENCY_THREAT",
        "category": "High Pressure / Urgency",
        "weight": 20,
        "patterns": [
            r'\b(?:urgent|immediately|within\s+\d+\s+(?:hours?|mins?|minutes?))\s*[:!]?',
            r'\b(?:account|card|access)\s+(?:has\s+been\s+)?(?:suspended|blocked|locked|terminated|closed)\b',
            r'\b(?:legal\s+action|law\s+enforcement|arrest\s+warrant|police\s+case|court\s+notice)\b',
            r'\b(?:final\s+warning|last\s+notice|immediate\s+action\s+required)\b'
        ],
        "reason": "Creates artificial urgency or threatens account closure / legal consequences.",
        "action": "Stay calm. Scammers use artificial panic to force quick decisions. Legitimate companies give reasonable time to resolve issues."
    },
    {
        "id": "RULE_PRIZE_REWARD",
        "category": "Unrealistic Reward",
        "weight": 20,
        "patterns": [
            r'\b(?:congratulations|congrats)\b.*?\b(?:won|winner|lottery|prize|reward)\b',
            r'\b(?:you\s+have\s+been\s+selected\s+to\s+receive|claim\s+your\s+(?:prize|reward|gift|bonus))\b',
            r'\b(?:unclaimed\s+funds|inheritance\s+of|\$\d+,\d+\s+cash\s+prize)\b'
        ],
        "reason": "Offers unexpected prizes, lottery winnings, or free money.",
        "action": "If you didn't enter a contest, you didn't win. Never pay fees or share personal details to claim a 'prize'."
    },
    {
        "id": "RULE_IMPERSONATION",
        "category": "Brand Impersonation",
        "weight": 15,
        "patterns": [
            r'\b(?:irs|customs|social\s+security\s+administration|tax\s+department)\b',
            r'\b(?:amazon\s+security|paypal\s+security|apple\s+support|microsoft\s+support|netflix\s+billing)\b.*?\b(?:alert|urgent|verify|locked|suspend)\b',
            r'\b(?:kyc\s+update\s+required|pan\s+card\s+blocked|account\s+verification\s+team)\b'
        ],
        "reason": "Claims to be from a well-known institution, government body, or tech support.",
        "action": "Verify directly by visiting the organization's official website or calling the customer service number on your actual physical card/bill."
    },
    {
        "id": "RULE_SUSPICIOUS_LINK",
        "category": "Link Risk",
        "weight": 15,
        "patterns": [
            r'https?://(?:bit\.ly|tinyurl\.com|t\.co|cutt\.ly|is\.gd|tiny\.cc)/[a-zA-Z0-9_-]+',
            r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?(?:/[^\s]*)?',
            r'\b(?:click\s+here\s+to\s+verify|tap\s+here\s+to\s+unlock)\b'
        ],
        "reason": "Contains a shortened link or urges you to click an unverified address.",
        "action": "Do not click on links sent in unsolicited messages. Type the official website address directly in your browser."
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
        "action": r["action"]
    })


def evaluate_rules(text: str) -> Dict[str, Any]:
    """
    Evaluates text against heuristic scam patterns.
    Returns matched rules, cumulative rule score, reasons, and actions.
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
