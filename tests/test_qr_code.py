import io
import pytest
import qrcode
from PIL import Image
from app import app
from ocr.qr_detector import extract_qr_code


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def create_qr_bytes(payload: str) -> io.BytesIO:
    """Helper creating in-memory PNG bytes of a QR code."""
    qr = qrcode.QRCode(box_size=8, border=3)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def test_qr_detector_direct_urls():
    """Unit test for QR code detector parsing valid URLs."""
    # 1. Standard HTTPS
    buf1 = create_qr_bytes("https://wikipedia.org/wiki/Phishing")
    res1 = extract_qr_code(buf1.getvalue())
    assert res1["found"] is True
    assert res1["extracted_url"] == "https://wikipedia.org/wiki/Phishing"

    # 2. Shortened link
    buf2 = create_qr_bytes("http://bit.ly/bank-security-claim")
    res2 = extract_qr_code(buf2.getvalue())
    assert res2["found"] is True
    assert res2["extracted_url"] == "http://bit.ly/bank-security-claim"

    # 3. Raw IP address URL
    buf3 = create_qr_bytes("http://192.168.1.50/login")
    res3 = extract_qr_code(buf3.getvalue())
    assert res3["found"] is True
    assert res3["extracted_url"] == "http://192.168.1.50/login"


def test_qr_detector_non_qr_image():
    """Unit test: a plain image with no QR returns found=False gracefully."""
    blank_img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    buf = io.BytesIO()
    blank_img.save(buf, format="PNG")
    res = extract_qr_code(buf.getvalue())
    assert res["found"] is False
    assert res["extracted_url"] == ""


def test_analyze_url_with_safe_qr_upload(client):
    """Integration test: upload safe QR code to /analyze/url."""
    qr_buf = create_qr_bytes("https://google.com")
    data = {
        'input_mode': 'screenshot',
        'screenshot': (qr_buf, 'test_safe_qr.png')
    }
    res = client.post('/analyze/url', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'google.com' in html
    assert 'Decoded via QR Code Scanner' in html or 'QR कोड स्कॅनर' in html


def test_analyze_url_with_scam_qr_upload(client):
    """Integration test: upload malicious Quishing QR code to /analyze/url."""
    qr_buf = create_qr_bytes("http://bit.ly/urgent-bank-block-verify")
    data = {
        'input_mode': 'screenshot',
        'screenshot': (qr_buf, 'test_scam_qr.png')
    }
    res = client.post('/analyze/url', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'bit.ly/urgent-bank-block-verify' in html
    assert 'Decoded via QR Code Scanner' in html or 'QR कोड स्कॅनर' in html
    # High risk or medium risk score
    assert 'Potential Scam' in html or 'High Risk' in html or 'Suspicious' in html or 'धोका' in html


def test_url_ui_qr_labels_english(client):
    """Verifies English UI elements for URL / QR feature."""
    client.get('/set_language/en')

    # Home card
    res_home = client.get('/')
    html_home = res_home.data.decode('utf-8')
    assert 'CHECK URL / QR CODE' in html_home
    assert 'Check Link / QR →' in html_home

    # URL Check Page
    res_url = client.get('/check/url')
    html_url = res_url.data.decode('utf-8')
    assert 'Check Website Link or QR Code' in html_url
    assert 'Scan QR Code / Screenshot' in html_url
    assert 'Drop QR Code' in html_url


def test_url_ui_qr_labels_marathi(client):
    """Verifies Marathi UI elements for URL / QR feature."""
    client.get('/set_language/mr')

    res_home = client.get('/')
    html_home = res_home.data.decode('utf-8')
    assert 'वेब लिंक किंवा QR कोड तपासा' in html_home
    assert 'लिंक किंवा QR तपासा →' in html_home

    res_url = client.get('/check/url')
    html_url = res_url.data.decode('utf-8')
    assert 'वेबसाइट लिंक किंवा QR कोड तपासा' in html_url
    assert 'QR कोड / स्क्रीनशॉट स्कॅन करा' in html_url


def test_url_ui_qr_labels_hindi(client):
    """Verifies Hindi UI elements for URL / QR feature."""
    client.get('/set_language/hi')

    res_home = client.get('/')
    html_home = res_home.data.decode('utf-8')
    assert 'वेब लिंक या क्यूआर कोड जांचें' in html_home
    assert 'लिंक या क्यूआर जांचें →' in html_home

    res_url = client.get('/check/url')
    html_url = res_url.data.decode('utf-8')
    assert 'वेबसाइट लिंक या क्यूआर कोड जांचें' in html_url
    assert 'क्यूआर कोड / स्क्रीनशॉट स्कैन करें' in html_url
