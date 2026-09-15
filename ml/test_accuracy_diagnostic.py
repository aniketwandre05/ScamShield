"""
End-to-End Accuracy & Risk Calibration Diagnostic Script
Tests all legitimate and scam samples across SMS, Email, URL, and OCR screenshots,
verifying that:
  - Legitimate inputs produce LOW RISK (0-29)
  - Scam/Phishing inputs produce HIGH RISK (60-100)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ocr.ocr_engine import extract_text_from_image
from ocr.content_detector import detect_content_structure
from risk.risk_engine import compute_hybrid_risk
from config import DEMO_SAMPLES_DIR


def run_diagnostic():
    print("=" * 75)
    print("SCAMSHIELD ACCURACY & CALIBRATION VERIFICATION")
    print("=" * 75)

    samples = [
        # --- 1. SMS SAMPLES ---
        {
            "category": "SMS Legitimate (Pasted)",
            "type": "sms",
            "text": "Hello Sarah, your dental cleaning appointment is confirmed for Tuesday, October 14th at 10:30 AM at Main Street Clinic. Reply YES to confirm or call 555-019-4820.",
            "expected": "LOW"
        },
        {
            "category": "SMS Scam (Pasted)",
            "type": "sms",
            "text": "URGENT: Your Chase Bank debit card has been LOCKED. Unauthorized withdrawal of $899.00 was detected in Miami. Visit http://bit.ly/chase-card-unlock to verify OTP.",
            "expected": "HIGH"
        },
        # --- 2. EMAIL SAMPLES ---
        {
            "category": "Email Legitimate (Pasted)",
            "type": "email",
            "subject": "Your Monthly Netflix Subscription Invoice (#NF-88391)",
            "sender": "billing@netflix.com",
            "text": "Hi Sarah, thank you for being a Netflix member. Your monthly plan has renewed. Amount Billed: $15.49 USD. View your full billing history at https://www.netflix.com/youraccount",
            "expected": "LOW"
        },
        {
            "category": "Email Scam / Phishing (Pasted)",
            "type": "email",
            "subject": "[FINAL WARNING] Your PayPal Account Has Been Suspended",
            "sender": "service-security@paypal-notice-alert24.xyz",
            "text": "Dear Valued Customer, we detected unauthorized login attempts from Russia. To restore access, verify your debit card and netbanking password at http://192.168.1.10/paypal-security immediately.",
            "expected": "HIGH"
        },
        # --- 3. URL SAMPLES ---
        {
            "category": "URL Legitimate (Pasted)",
            "type": "url",
            "url": "https://www.google.com/search?q=weather+today",
            "expected": "LOW"
        },
        {
            "category": "URL Scam / Phishing (Pasted)",
            "type": "url",
            "url": "http://192.168.1.100/secure-bank-login/verify/update.php",
            "expected": "HIGH"
        },
        # --- 4. SCREENSHOTS (OCR) ---
        {
            "category": "SMS Legitimate (Screenshot)",
            "type": "screenshot_sms",
            "file": "sms_legitimate.png",
            "expected": "LOW"
        },
        {
            "category": "SMS Scam (Screenshot)",
            "type": "screenshot_sms",
            "file": "sms_scam.png",
            "expected": "HIGH"
        },
        {
            "category": "Email Legitimate (Screenshot)",
            "type": "screenshot_email",
            "file": "email_legitimate.png",
            "expected": "LOW"
        },
        {
            "category": "Email Scam (Screenshot)",
            "type": "screenshot_email",
            "file": "email_scam.png",
            "expected": "HIGH"
        },
        {
            "category": "URL Legitimate (Screenshot)",
            "type": "screenshot_url",
            "file": "url_legitimate.png",
            "expected": "LOW"
        },
        {
            "category": "URL Scam (Screenshot)",
            "type": "screenshot_url",
            "file": "url_scam.png",
            "expected": "HIGH"
        },
    ]

    all_passed = True

    for s in samples:
        stype = s["type"]
        if stype.startswith("screenshot"):
            img_path = DEMO_SAMPLES_DIR / "screenshots" / s["file"]
            ocr_res = extract_text_from_image(str(img_path))
            text = ocr_res["text"]
            detected = detect_content_structure(text)

            if "email" in stype:
                res = compute_hybrid_risk(
                    "email",
                    subject=detected.get("subject", ""),
                    body=detected.get("body", text),
                    sender=detected.get("sender", ""),
                    override_urls=detected.get("urls", [])
                )
            elif "url" in stype:
                target = detected["urls"][0] if detected["urls"] else text
                res = compute_hybrid_risk("url", url=target)
            else:
                res = compute_hybrid_risk("sms", text=text, override_urls=detected.get("urls", []))
        elif stype == "email":
            res = compute_hybrid_risk("email", subject=s.get("subject", ""), body=s.get("text", ""), sender=s.get("sender", ""))
        elif stype == "url":
            res = compute_hybrid_risk("url", url=s["url"])
        else:
            res = compute_hybrid_risk("sms", text=s["text"])

        score = res["risk_score"]
        level = res["risk_level"]
        exp = s["expected"]
        passed = (level == exp) or (exp == "LOW" and score <= 29) or (exp == "HIGH" and score >= 60)

        status_str = "[PASS]" if passed else "[FAIL]"
        if not passed:
            all_passed = False

        print(f"{status_str} {s['category']:<35} -> Score: {score:>2}/100 | Level: {level:<6} (Expected: {exp})")

    print("=" * 75)
    if all_passed:
        print("ALL TESTS PASSED: Accuracy & Risk Level distinction is 100% calibrated!")
    else:
        print("Calibration adjustments needed for highlighted test cases.")


if __name__ == "__main__":
    run_diagnostic()
