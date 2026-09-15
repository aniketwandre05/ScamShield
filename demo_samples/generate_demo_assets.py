"""
Generate Demonstration Samples and Clean Realistic Screenshot Assets
Creates pure, realistic UI screenshots for SMS, Email, and URLs (Legitimate vs Scam).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
DEMO_DIR = BASE_DIR / "demo_samples"
SMS_DIR = DEMO_DIR / "sms"
EMAIL_DIR = DEMO_DIR / "email"
URL_DIR = DEMO_DIR / "url"
IMG_DIR = DEMO_DIR / "screenshots"

for d in [SMS_DIR, EMAIL_DIR, URL_DIR, IMG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def create_demo_screenshots():
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 14)
        font_body = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_url = ImageFont.truetype("cour.ttf", 16)
    except Exception:
        font_header = font_sub = font_body = font_bold = font_url = ImageFont.load_default()

    # =========================================================================
    # 1. SMS LEGITIMATE (SAFE)
    # =========================================================================
    img_sms_safe = Image.new('RGB', (750, 260), color='#f1f5f9')
    d = ImageDraw.Draw(img_sms_safe)
    # App header
    d.rectangle([(0, 0), (750, 55)], fill='#2563eb')
    d.text((25, 12), "Messages - Clinic Reminder", font=font_header, fill='#ffffff')
    d.text((25, 36), "+1 (555) 019-4820 - Verified Clinic", font=font_sub, fill='#bfdbfe')
    # Safe Message Bubble
    d.rectangle([(40, 80), (710, 220)], fill='#ffffff', outline='#cbd5e1', width=2)
    d.text((60, 100), "Hello Sarah, your dental cleaning appointment is confirmed for", font=font_body, fill='#0f172a')
    d.text((60, 130), "Tuesday, October 14th at 10:30 AM at Main Street Clinic.", font=font_body, fill='#0f172a')
    d.text((60, 165), "Reply YES to confirm or call 555-019-4820 to reschedule.", font=font_body, fill='#0f172a')
    d.text((60, 195), "10:15 AM - Delivered", font=font_sub, fill='#94a3b8')
    img_sms_safe.save(IMG_DIR / "sms_legitimate.png")
    img_sms_safe.save(IMG_DIR / "sample_sms_safe.png")

    # =========================================================================
    # 2. SMS SCAM (SUSPICIOUS / HIGH RISK)
    # =========================================================================
    img_sms_scam = Image.new('RGB', (750, 280), color='#f1f5f9')
    d = ImageDraw.Draw(img_sms_scam)
    # App header
    d.rectangle([(0, 0), (750, 55)], fill='#1e293b')
    d.text((25, 12), "Unknown Sender - Bank Alert Security", font=font_header, fill='#ffffff')
    d.text((25, 36), "+1 (800) 555-0199", font=font_sub, fill='#94a3b8')
    # Scam Message Bubble
    d.rectangle([(40, 80), (710, 250)], fill='#ffffff', outline='#fca5a5', width=2)
    d.text((60, 100), "URGENT: Your Chase Bank debit card has been LOCKED.", font=font_bold, fill='#b91c1c')
    d.text((60, 130), "Unauthorized withdrawal of $899.00 was detected in Miami.", font=font_body, fill='#0f172a')
    d.text((60, 165), "To restore access and verify your One-Time Password (OTP),", font=font_body, fill='#0f172a')
    d.text((60, 195), "visit: http://bit.ly/chase-card-unlock-verify", font=font_bold, fill='#2563eb')
    d.text((60, 225), "Failure to verify within 2 hours will freeze all accounts.", font=font_body, fill='#b91c1c')
    img_sms_scam.save(IMG_DIR / "sms_scam.png")
    img_sms_scam.save(IMG_DIR / "sample_sms_scam.png")

    # =========================================================================
    # 3. EMAIL LEGITIMATE (SAFE)
    # =========================================================================
    img_email_safe = Image.new('RGB', (850, 360), color='#ffffff')
    d = ImageDraw.Draw(img_email_safe)
    # Email Client Header
    d.rectangle([(0, 0), (850, 95)], fill='#f8fafc', outline='#e2e8f0', width=2)
    d.text((30, 15), "Subject: Your Monthly Netflix Subscription Invoice (#NF-88391)", font=font_header, fill='#0f172a')
    d.text((30, 46), "From: Netflix Billing <billing@netflix.com>", font=font_body, fill='#475569')
    d.text((30, 70), "To: sarah.miller@gmail.com - Date: Oct 12, 2026", font=font_sub, fill='#64748b')
    # Email Body
    d.text((30, 120), "Hi Sarah,", font=font_body, fill='#0f172a')
    d.text((30, 150), "Thank you for being a Netflix member. Your monthly plan has renewed.", font=font_body, fill='#0f172a')
    d.text((30, 185), "Amount Billed: $15.49 USD", font=font_bold, fill='#0f172a')
    d.text((30, 215), "Payment Method: Visa ending in *1042", font=font_body, fill='#0f172a')
    d.text((30, 250), "You can view your full billing history anytime at https://www.netflix.com/youraccount", font=font_body, fill='#2563eb')
    d.text((30, 290), "Questions? Visit our Help Center at https://help.netflix.com", font=font_body, fill='#475569')
    img_email_safe.save(IMG_DIR / "email_legitimate.png")

    # =========================================================================
    # 4. EMAIL SCAM (PHISHING / HIGH RISK)
    # =========================================================================
    img_email_scam = Image.new('RGB', (850, 400), color='#ffffff')
    d = ImageDraw.Draw(img_email_scam)
    # Email Client Header
    d.rectangle([(0, 0), (850, 95)], fill='#fef2f2', outline='#fca5a5', width=2)
    d.text((30, 15), "Subject: [FINAL WARNING] Your PayPal Account Has Been Suspended", font=font_header, fill='#b91c1c')
    d.text((30, 46), "From: PayPal Support Team <service-security@paypal-notice-alert24.xyz>", font=font_bold, fill='#b91c1c')
    d.text((30, 70), "To: victim@gmail.com - Immediate Action Required", font=font_sub, fill='#64748b')
    # Email Body
    d.text((30, 115), "Dear Valued Customer,", font=font_bold, fill='#0f172a')
    d.text((30, 145), "We detected unauthorized login attempts to your PayPal account from Russia.", font=font_body, fill='#0f172a')
    d.text((30, 175), "To restore access and verify your debit card and password immediately,", font=font_body, fill='#0f172a')
    d.text((30, 205), "please confirm your identity within 24 hours at the security portal below:", font=font_body, fill='#0f172a')
    # Button box
    d.rectangle([(30, 240), (450, 295)], fill='#0070ba', outline='#005ea6', width=2)
    d.text((50, 258), "Click: http://192.168.1.10/paypal-security/login.html", font=font_url, fill='#ffffff')
    d.text((30, 315), "Failure to verify will result in permanent account termination.", font=font_bold, fill='#b91c1c')
    img_email_scam.save(IMG_DIR / "email_scam.png")
    img_email_scam.save(IMG_DIR / "sample_email_phish.png")

    # =========================================================================
    # 5. URL LEGITIMATE (SAFE)
    # =========================================================================
    img_url_safe = Image.new('RGB', (850, 150), color='#ffffff')
    d = ImageDraw.Draw(img_url_safe)
    # Browser Top Bar
    d.rectangle([(0, 0), (850, 50)], fill='#e2e8f0')
    d.ellipse([(20, 18), (34, 32)], fill='#ef4444')
    d.ellipse([(44, 18), (58, 32)], fill='#eab308')
    d.ellipse([(68, 18), (82, 32)], fill='#22c55e')
    # Address Bar
    d.rectangle([(110, 8), (820, 42)], fill='#ffffff', outline='#94a3b8', width=1)
    d.text((125, 14), "https://www.google.com/search?q=weather+today", font=font_body, fill='#15803d')
    d.text((40, 75), "Google Search - Official & Secure Web Portal", font=font_header, fill='#1e40af')
    d.text((40, 105), "Official Domain: https://www.google.com", font=font_body, fill='#0f172a')
    img_url_safe.save(IMG_DIR / "url_legitimate.png")

    # =========================================================================
    # 6. URL SCAM (MALICIOUS / PHISHING)
    # =========================================================================
    img_url_scam = Image.new('RGB', (850, 150), color='#ffffff')
    d = ImageDraw.Draw(img_url_scam)
    # Browser Top Bar
    d.rectangle([(0, 0), (850, 50)], fill='#e2e8f0')
    d.ellipse([(20, 18), (34, 32)], fill='#ef4444')
    d.ellipse([(44, 18), (58, 32)], fill='#eab308')
    d.ellipse([(68, 18), (82, 32)], fill='#22c55e')
    # Address Bar
    d.rectangle([(110, 8), (820, 42)], fill='#fef2f2', outline='#ef4444', width=2)
    d.text((125, 14), "http://192.168.1.100/secure-bank-login/verify/update.php", font=font_body, fill='#b91c1c')
    d.text((40, 75), "Warning: Insecure Portal - IP Host", font=font_header, fill='#b91c1c')
    d.text((40, 105), "Unencrypted Destination: http://192.168.1.100/secure-bank-login/verify", font=font_body, fill='#0f172a')
    img_url_scam.save(IMG_DIR / "url_scam.png")

    print("Successfully generated clean demonstration screenshot assets!")


if __name__ == "__main__":
    create_demo_screenshots()
