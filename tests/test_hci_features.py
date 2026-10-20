"""
ScamShield HCI Feature Test Suite
Verifies all HCI Implementation Checklist features:
1. Sensitive data masking (credit cards, OTP, CVV, passwords)
2. Suspicious keyword highlighting (safe escaping, mark tags)
3. New routes (/learn, /report, /history/export, /api/feedback)
4. UI elements (privacy banner, action buttons, onboarding guide)
5. Multi-language support for new pages and controls
"""

import pytest
from app import app
from risk.privacy import mask_sensitive_data, highlight_suspicious_keywords


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_privacy_masking_credit_card():
    text = "Please transfer fee to card 4111 2222 3333 4444 now."
    masked = mask_sensitive_data(text)
    assert "****-****-****-4444" in masked
    assert "4111" not in masked


def test_privacy_masking_otp_and_cvv():
    text = "Your OTP: 876543 and CVV: 789 should not be shared."
    masked = mask_sensitive_data(text)
    assert "OTP: ******" in masked
    assert "CVV: ***" in masked
    assert "876543" not in masked


def test_privacy_masking_password():
    text = "Login with password: SuperSecretPassword123"
    masked = mask_sensitive_data(text)
    assert "password: ********" in masked
    assert "SuperSecretPassword123" not in masked


def test_keyword_highlighting_xss_safe():
    malicious_input = "<script>alert('xss')</script> URGENT: account blocked with OTP"
    highlighted = highlight_suspicious_keywords(malicious_input)
    assert "<script>" not in highlighted
    assert "&lt;script&gt;" in highlighted
    assert '<mark class="suspicious-keyword">URGENT</mark>' in highlighted
    assert '<mark class="suspicious-keyword">blocked</mark>' in highlighted
    assert '<mark class="suspicious-keyword">OTP</mark>' in highlighted


def test_learn_route(client):
    res = client.get('/learn')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Scam Awareness' in html or 'शिक्षण केंद्र' in html or 'जागरूकता' in html
    assert 'Electricity Bill Disconnection' in html
    assert 'Remote Screen Share' in html
    assert 'cybercrime.gov.in' in html


def test_learn_route_marathi(client):
    client.get('/set_language/mr')
    res = client.get('/learn')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'फसवणूक जागृती आणि शिक्षण केंद्र' in html


def test_report_route_get_and_post(client):
    # GET
    res = client.get('/report')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert '1930' in html
    assert 'cybercrime.gov.in' in html

    # POST submission
    res_post = client.post('/report', data={
        'scam_type': 'sms',
        'offender_info': '+91 9999999999',
        'scam_details': 'Received electricity disconnection threat.'
    })
    assert res_post.status_code == 200
    html_post = res_post.data.decode('utf-8')
    assert 'Report Received' in html_post or 'नोंदवली' in html_post or 'दर्ज' in html_post


def test_history_export_csv(client):
    # Add an item to history by checking SMS
    client.post('/analyze/sms', data={
        'sms_text': 'URGENT: Your account is suspended. Verify OTP 1234.'
    })
    res = client.get('/history/export')
    assert res.status_code == 200
    assert 'text/csv' in res.content_type
    csv_data = res.data.decode('utf-8')
    assert 'ID,Content Type,Snippet,Risk Score,Risk Level,Date & Time' in csv_data
    assert 'SMS' in csv_data


def test_api_feedback(client):
    res = client.post('/api/feedback', json={'helpful': True, 'url': '/result'})
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'success'


def test_privacy_banner_and_tools_on_forms(client):
    for route in ('/check/sms', '/check/email', '/check/url'):
        res = client.get(route)
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert 'privacy-warning-banner' in html
        assert 'btn-action-paste' in html
        assert 'btn-action-clear' in html
        assert 'btn-action-voice' not in html


def test_result_page_hci_elements(client):
    res = client.post('/analyze/sms', data={
        'sms_text': 'URGENT: Your bank account is locked. Verify at http://bit.ly/bank-security-verify'
    })
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'btn-read-aloud' in html
    assert 'btn-copy-summary' in html
    assert 'btn-share-warning' in html
    assert 'result-feedback-widget' in html
    assert 'result-disclaimer-note' in html
    assert 'suspicious-keyword' in html


def test_download_assignment_pdf(client):
    res = client.get('/download/assignment-pdf')
    assert res.status_code == 200
    assert 'application/pdf' in res.content_type
    assert len(res.data) > 10000  # valid PDF binary content
