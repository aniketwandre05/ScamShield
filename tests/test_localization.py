import pytest
from app import app
from risk.phone_risk import get_localized_phone_questions, assess_phone_call_risk


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_language_switch_marathi(client):
    res = client.get('/set_language/mr', follow_redirects=True)
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'आज आपण काय तपासू इच्छिता?' in html
    assert 'मराठी' in html
    assert 'स्कॅमशील्ड' in html


def test_language_switch_hindi(client):
    res = client.get('/set_language/hi', follow_redirects=True)
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'आज आप क्या जांचना चाहते हैं?' in html
    assert 'हिंदी' in html
    assert 'स्कैमशील्ड' in html


def test_language_switch_english(client):
    client.get('/set_language/mr')
    res = client.get('/set_language/en', follow_redirects=True)
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'What would you like to check today?' in html
    assert 'SCAMSHIELD' in html


def test_phone_questions_marathi(client):
    client.get('/set_language/mr')
    res = client.get('/check/phone')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'संशयास्पद फोन कॉल तपासा' in html
    assert 'होय (YES)' in html
    assert 'नाही (NO)' in html


def test_phone_questions_hindi(client):
    client.get('/set_language/hi')
    res = client.get('/check/phone')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'संदिग्ध फोन कॉल की जांच करें' in html
    assert 'हाँ (YES)' in html
    assert 'नहीं (NO)' in html


def test_sms_check_in_marathi(client):
    client.get('/set_language/mr')
    res = client.get('/check/sms')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'एसएमएस किंवा व्हॉट्सअॅप संदेश तपासा' in html
    assert 'संदेश मजकूर पेस्ट करा' in html


def test_email_check_in_hindi(client):
    client.get('/set_language/hi')
    res = client.get('/check/email')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'ईमेल सामग्री जांचें' in html
    assert 'ईमेल विवरण पेस्ट करें' in html


def test_url_check_in_marathi(client):
    client.get('/set_language/mr')
    res = client.get('/check/url')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'वेबसाइट लिंक (URL) तपासा' in html


def test_marathi_backend_sms_analysis(client):
    client.get('/set_language/mr')
    res = client.post('/analyze/sms', data={
        'sms_text': 'तुमचा बँक खाते तात्काळ ब्लॉक केले जाईल. कृपया OTP शेअर करा आणि व्हेरिफाय करा.'
    })
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    # Risk score should be high/medium
    assert 'धोका पातळी' in html or 'जोखीम' in html or 'सुरक्षा' in html
    # Check that Marathi action/reasons are present
    assert 'OTP किंवा पासवर्ड' in html or 'कधीही शेअर करू नका' in html or 'खाते' in html


def test_hindi_backend_sms_analysis(client):
    client.get('/set_language/hi')
    res = client.post('/analyze/sms', data={
        'sms_text': 'बधाई हो! आपने 25 लाख की लॉटरी जीती है। तुरंत क्लेम करने के लिए OTP भेजें।'
    })
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    # Risk score should be high
    assert 'जोखिम' in html or 'सुरक्षा' in html or 'खतरा' in html
    # Check that Hindi reasons/actions are present
    assert 'ओटीपी' in html or 'इनाम' in html or 'साझा न करें' in html


def test_marathi_backend_phone_analysis(client):
    client.get('/set_language/mr')
    res = client.post('/analyze/phone', data={
        'q_urgent': 'yes',
        'q_remote_access': 'yes',
        'q_money': 'yes',
        'q_otp': 'yes',
        'q_threat': 'yes',
        'q_unknown': 'yes'
    })
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    # Should have Marathi explanations and checklist
    assert 'तात्काळ' in html or 'स्क्रीन शेअरिंग' in html or 'कॉल' in html
