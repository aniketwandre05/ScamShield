import sys
import json
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:5001"

passed = 0
failed = 0

def check(name, condition, extra=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name} {extra}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {extra}")

print("=" * 80)
print("STARTING SCAMSHIELD DEMO READINESS SYSTEM VERIFICATION")
print("=" * 80)

# Setup cookie jar for session
cookie_jar = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookie_jar)

# 1. Test All Main GET Routes
print("\n--- 1. Main Navigation Routes ---")
routes = [
    ("/", "Home Dashboard"),
    ("/check/sms", "SMS Checker Form"),
    ("/check/email", "Email Checker Form"),
    ("/check/url", "URL / QR Checker Form"),
    ("/check/phone", "Phone Questionnaire Form"),
    ("/history", "Scan History Page"),
    ("/learn", "Awareness & Quiz Center"),
    ("/report", "Incident Report & Helplines"),
]

for route, desc in routes:
    try:
        res = opener.open(f"{BASE_URL}{route}")
        status = res.status
        html = res.read().decode("utf-8")
        check(f"GET {route} ({desc})", status == 200 and len(html) > 500, f"[Status: {status}, Size: {len(html)} bytes]")
    except Exception as e:
        check(f"GET {route} ({desc})", False, f"[Exception: {e}]")

# 2. Test Multilingual Language Switching
print("\n--- 2. Language Switching (EN, MR, HI) ---")
for lang_code, lang_name, expected_snippet in [
    ("en", "English", "What would you like to check today?"),
    ("mr", "Marathi", "आज आपण काय तपासू इच्छिता?"),
    ("hi", "Hindi", "आज आप क्या जांचना चाहते हैं?")
]:
    try:
        # Switch language
        res = opener.open(f"{BASE_URL}/set_language/{lang_code}")
        # Fetch home
        res_home = opener.open(f"{BASE_URL}/")
        html = res_home.read().decode("utf-8")
        check(f"Language Switch -> {lang_name} ({lang_code})", expected_snippet in html, f"[Found expected localized greeting]")
    except Exception as e:
        check(f"Language Switch -> {lang_name}", False, f"[Exception: {e}]")

# Switch back to English for uniform testing
opener.open(f"{BASE_URL}/set_language/en")

# 3. Test Core Analysis Pipelines (POST)
print("\n--- 3. Core Analysis Workflows (SMS, Email, URL, Phone) ---")

# 3.1 SMS Check - Legitimate
try:
    data = urllib.parse.urlencode({"input_mode": "text", "sms_text": "Hey Mom, let's meet for lunch at 12:30 PM tomorrow."}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/sms", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("SMS Safe Message Analysis", res.status == 200 and "Potentially Safe" in html, "[Status: 200, Verdict: Potentially Safe]")
except Exception as e:
    check("SMS Safe Message Analysis", False, f"[{e}]")

# 3.2 SMS Check - Scam
try:
    data = urllib.parse.urlencode({"input_mode": "text", "sms_text": "URGENT: Your electricity power will be disconnected at 9:30 PM tonight due to unpaid bill. Call officer immediately at 9876543210"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/sms", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("SMS Scam Trap Analysis", res.status == 200 and "High Risk" in html, "[Status: 200, Verdict: High Risk]")
except Exception as e:
    check("SMS Scam Trap Analysis", False, f"[{e}]")

# 3.3 Email Check - Safe
try:
    data = urllib.parse.urlencode({
        "input_mode": "text",
        "email_subject": "Team Sync Meeting Notes",
        "email_sender": "colleague@company.com",
        "email_body": "Hi everyone, here are the meeting notes from today's design sync. Let me know if you have any feedback."
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/email", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Email Safe Message Analysis", res.status == 200 and "Potentially Safe" in html, "[Status: 200, Verdict: Potentially Safe]")
except Exception as e:
    check("Email Safe Message Analysis", False, f"[{e}]")

# 3.4 Email Check - Phishing
try:
    data = urllib.parse.urlencode({
        "input_mode": "text",
        "email_subject": "IMMEDIATE ACTION REQUIRED: Your Account Has Been Locked",
        "email_sender": "security-alert@suspicious-bank-notice.com",
        "email_body": "Dear customer, your bank account access has been suspended due to unauthorized login attempts. Click here to verify your password immediately: http://192.168.1.1/login"
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/email", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Email Phishing Trap Analysis", res.status == 200 and "High Risk" in html, "[Status: 200, Verdict: High Risk]")
except Exception as e:
    check("Email Phishing Trap Analysis", False, f"[{e}]")

# 3.5 URL Check - Safe Link
try:
    data = urllib.parse.urlencode({"input_mode": "text", "url_input": "https://www.google.com"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/url", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("URL Safe Link Analysis", res.status == 200 and "Potentially Safe" in html, "[Status: 200, Verdict: Potentially Safe]")
except Exception as e:
    check("URL Safe Link Analysis", False, f"[{e}]")

# 3.6 URL Check - Phishing Link
try:
    data = urllib.parse.urlencode({"input_mode": "text", "url_input": "http://192.168.1.50/paypal-security/login"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/url", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("URL Phishing Link Analysis", res.status == 200 and "High Risk" in html, "[Status: 200, Verdict: High Risk]")
except Exception as e:
    check("URL Phishing Link Analysis", False, f"[{e}]")

# 3.7 Phone Questionnaire - Safe Call
try:
    phone_data = {f"q{i}": "0" for i in range(1, 11)}
    data = urllib.parse.urlencode(phone_data).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/phone", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Phone Questionnaire - Safe Call", res.status == 200 and "Potentially Safe" in html, "[Score <= 20, Safe]")
except Exception as e:
    check("Phone Questionnaire - Safe Call", False, f"[{e}]")

# 3.8 Phone Questionnaire - High Risk Scam Call
try:
    phone_data = {f"q{i}": "1" for i in range(1, 11)}
    data = urllib.parse.urlencode(phone_data).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/phone", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Phone Questionnaire - High Risk Call", res.status == 200 and "High Risk" in html, "[Score >= 70, High Risk]")
except Exception as e:
    check("Phone Questionnaire - High Risk Call", False, f"[{e}]")

# 4. History, CSV Export & Clear History
print("\n--- 4. History Features & Local Session Management ---")
try:
    res = opener.open(f"{BASE_URL}/history")
    html = res.read().decode("utf-8")
    check("View Scan History (contains past scans)", "SMS" in html and "URL" in html, "[History correctly records session checks]")
except Exception as e:
    check("View Scan History", False, f"[{e}]")

try:
    res = opener.open(f"{BASE_URL}/history/export")
    csv_text = res.read().decode("utf-8")
    check("Export Scan History CSV", res.status == 200 and "Risk Score" in csv_text, f"[Received CSV with {len(csv_text.splitlines())} lines]")
except Exception as e:
    check("Export Scan History CSV", False, f"[{e}]")

try:
    req = urllib.request.Request(f"{BASE_URL}/history/clear", data=b"")
    res = opener.open(req)
    html_after = res.read().decode("utf-8")
    check("Clear History Action", res.status == 200 and ("No Scans Performed Yet" in html_after or "history-empty" in html_after or "cleared" in html_after), "[Cleared session scans successfully]")
except Exception as e:
    check("Clear History Action", False, f"[{e}]")

# 5. Feedback API & Report Scam Form
print("\n--- 5. User Feedback & Community Scam Reporting ---")
try:
    data = json.dumps({"helpful": True}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/feedback", data=data, headers={"Content-Type": "application/json"})
    res = opener.open(req)
    json_res = json.loads(res.read().decode("utf-8"))
    check("Assessment Feedback API (Thumbs up/down)", res.status == 200 and json_res.get("status") == "success", "[Feedback logged]")
except Exception as e:
    check("Assessment Feedback API", False, f"[{e}]")

try:
    data = urllib.parse.urlencode({"scam_type": "sms", "scam_details": "Test scam report from verification script"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/report", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Community Scam Report Submission", res.status == 200 and "Your incident report has been submitted" in html, "[Success message displayed]")
except Exception as e:
    check("Community Scam Report Submission", False, f"[{e}]")

# 6. Error Handling & Form Validations (Graceful Error Recovery)
print("\n--- 6. Error Handling & Edge Cases ---")
# 6.1 Empty SMS submission
try:
    data = urllib.parse.urlencode({"input_mode": "text", "sms_text": ""}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/sms", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Empty SMS Submissions -> Friendly Error Page", "Empty Message" in html or "error-recovery-panel" in html, "[Graceful friendly error page rendered]")
except Exception as e:
    check("Empty SMS Submissions", False, f"[{e}]")

# 6.2 Empty URL submission
try:
    data = urllib.parse.urlencode({"input_mode": "text", "url_input": ""}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/url", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Empty URL Submissions -> Friendly Error Page", "Empty URL" in html or "error-recovery-panel" in html, "[Graceful friendly error page rendered]")
except Exception as e:
    check("Empty URL Submissions", False, f"[{e}]")

# 6.3 Empty Email submission
try:
    data = urllib.parse.urlencode({"input_mode": "text", "email_subject": "", "email_body": ""}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/analyze/email", data=data)
    res = opener.open(req)
    html = res.read().decode("utf-8")
    check("Empty Email Submissions -> Friendly Error Page", "Empty Email" in html or "error-recovery-panel" in html, "[Graceful friendly error page rendered]")
except Exception as e:
    check("Empty Email Submissions", False, f"[{e}]")

# 6.4 404 Not Found Page
try:
    req = urllib.request.Request(f"{BASE_URL}/nonexistent-page-url-xyz")
    try:
        res = opener.open(req)
    except urllib.error.HTTPError as he:
        html = he.read().decode("utf-8")
        check("Custom 404 Error Page", he.code == 404 and "Page Not Found" in html, "[Custom branded 404 page rendered]")
except Exception as e:
    check("Custom 404 Error Page", False, f"[{e}]")

print("\n" + "=" * 80)
print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED")
print("=" * 80)
