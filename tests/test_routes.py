"""
Integration Tests for Flask Web Application Routes
"""

import io
import pytest
from app import app
from config import DEMO_SAMPLES_DIR


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


def test_home_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"SCAMSHIELD" in res.data
    assert b"CHECK SMS" in res.data
    assert b"CHECK EMAIL" in res.data
    assert b"CHECK URL" in res.data
    assert b"CHECK PHONE CALL" in res.data


def test_sms_check_get(client):
    res = client.get('/check/sms')
    assert res.status_code == 200
    assert b"Check SMS or WhatsApp Message" in res.data


def test_sms_analyze_text(client):
    res = client.post('/analyze/sms', data={
        'input_mode': 'text',
        'sms_text': 'URGENT: Bank account locked. Verify OTP at http://bit.ly/unlock'
    })
    assert res.status_code == 200
    assert b"ScamShield Assessment Result" in res.data
    assert b"Estimated Risk Score" in res.data


def test_email_analyze_text(client):
    res = client.post('/analyze/email', data={
        'input_mode': 'text',
        'email_subject': 'Security Alert: Immediate Action Required',
        'email_body': 'Your account has been suspended. Click http://192.168.1.1/login to verify your password.',
        'email_sender': 'alert@security-scam.xyz'
    })
    assert res.status_code == 200
    assert b"ScamShield Assessment Result" in res.data


def test_url_analyze_post(client):
    res = client.post('/analyze/url', data={
        'url_input': 'http://192.168.1.10/fake-bank-login'
    })
    assert res.status_code == 200
    assert b"Website Link (URL)" in res.data


def test_phone_analyze_post(client):
    res = client.post('/analyze/phone', data={
        'q1': 'yes',
        'q2': 'yes',
        'q3': 'no'
    })
    assert res.status_code == 200
    assert b"Phone Call Assessment" in res.data


def test_sms_analyze_screenshot_upload(client):
    sample_img_path = DEMO_SAMPLES_DIR / "screenshots" / "sample_sms_scam.png"
    assert sample_img_path.exists()
    
    with open(sample_img_path, 'rb') as f:
        img_bytes = f.read()
        
    data = {
        'input_mode': 'screenshot',
        'screenshot': (io.BytesIO(img_bytes), 'sample_sms_scam.png')
    }
    res = client.post('/analyze/sms', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    assert b"Extracted via OCR Screenshot Scanner" in res.data


def test_url_analyze_screenshot_upload(client):
    sample_img_path = DEMO_SAMPLES_DIR / "screenshots" / "url_scam.png"
    assert sample_img_path.exists()
    
    with open(sample_img_path, 'rb') as f:
        img_bytes = f.read()
        
    data = {
        'input_mode': 'screenshot',
        'screenshot': (io.BytesIO(img_bytes), 'url_scam.png')
    }
    res = client.post('/analyze/url', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    assert b"Extracted via OCR Screenshot Scanner" in res.data


def test_history_and_clear(client):
    # Perform a scan
    client.post('/analyze/url', data={'url_input': 'https://www.google.com'})
    
    # View history
    res = client.get('/history')
    assert res.status_code == 200
    assert b"google.com" in res.data
    
    # Clear history
    clear_res = client.post('/history/clear', follow_redirects=True)
    assert clear_res.status_code == 200
    assert b"No Scans Performed Yet" in clear_res.data


def test_empty_inputs_error_handling(client):
    res = client.post('/analyze/sms', data={'input_mode': 'text', 'sms_text': ''})
    assert res.status_code == 200
    assert b"Empty Message" in res.data
