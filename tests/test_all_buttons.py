import io
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_navigation_buttons(client):
    """Checks that all header navigation and language switcher links respond with 200."""
    routes = [
        '/',
        '/check/sms',
        '/check/email',
        '/check/url',
        '/check/phone',
        '/history',
        '/learn',
        '/report'
    ]
    for r in routes:
        res = client.get(r)
        assert res.status_code == 200, f"Route {r} failed with status {res.status_code}"

    # Language switches
    for lang in ('en', 'mr', 'hi'):
        res = client.get(f'/set_language/{lang}', follow_redirects=True)
        assert res.status_code == 200


def test_global_header_buttons_present(client):
    """Verifies that font scaling, theme toggle, and a11y buttons are present in base DOM."""
    res = client.get('/')
    html = res.data.decode('utf-8')

    assert 'id="btn-font-decrease"' in html
    assert 'id="btn-font-reset"' in html
    assert 'id="btn-font-increase"' in html
    assert 'id="theme-toggle-btn"' in html
    assert 'id="a11y-menu-btn"' in html
    assert 'id="btn-toggle-dyslexia"' in html
    assert 'id="btn-toggle-contrast"' in html
    assert 'id="modal-btn-cancel"' in html
    assert 'id="modal-btn-confirm"' in html


def test_sms_page_buttons_and_interactions(client):
    """Verifies SMS form buttons, paste/clear tools, and demo buttons."""
    res = client.get('/check/sms')
    html = res.data.decode('utf-8')

    assert 'data-tab="paste-tab"' in html
    assert 'data-tab="upload-tab"' in html
    assert 'btn-action-paste' in html
    assert 'btn-action-clear' in html
    assert 'btn-reset-form' in html
    assert 'id="btn-submit-sms"' in html
    assert 'btn-demo-safe' in html
    assert 'btn-demo-scam' in html
    assert 'btn-choose-file' in html
    assert 'btn-take-photo' in html
    assert 'file-input-choose' in html
    assert 'file-input-camera' in html

    # Test POST submission button (text)
    post_res = client.post('/analyze/sms', data={'sms_text': 'URGENT: Verify your account now http://scam.xyz'})
    assert post_res.status_code == 200
    assert 'ScamShield' in post_res.data.decode('utf-8') or 'स्कॅमशील्ड' in post_res.data.decode('utf-8') or 'स्कैमशील्ड' in post_res.data.decode('utf-8')

    # Test POST submission button (camera upload)
    cam_res = client.post('/analyze/sms', data={
        'input_mode': 'screenshot',
        'screenshot_camera': (io.BytesIO(b'dummy image bytes'), 'camera.jpg')
    }, content_type='multipart/form-data')
    assert cam_res.status_code == 200


def test_email_page_buttons_and_interactions(client):
    """Verifies Email form buttons, multi-field reset, and submit."""
    res = client.get('/check/email')
    html = res.data.decode('utf-8')

    assert 'id="btn-submit-email"' in html
    assert 'btn-reset-form' in html
    assert 'btn-demo-safe' in html
    assert 'btn-demo-scam' in html
    assert 'btn-choose-file' in html
    assert 'btn-take-photo' in html

    # Test POST submission
    post_res = client.post('/analyze/email', data={
        'email_subject': 'Security alert',
        'email_body': 'Please confirm your password immediately.',
        'email_sender': 'alert@security-notice.com'
    })
    assert post_res.status_code == 200


def test_url_page_buttons_and_interactions(client):
    """Verifies URL form buttons and demo buttons."""
    res = client.get('/check/url')
    html = res.data.decode('utf-8')

    assert 'id="btn-submit-url"' in html
    assert 'btn-reset-form' in html
    assert 'btn-demo-safe' in html
    assert 'btn-demo-scam' in html
    assert 'btn-choose-file' in html
    assert 'btn-take-photo' in html

    # Test POST submission
    post_res = client.post('/analyze/url', data={'url_input': 'https://google.com'})
    assert post_res.status_code == 200


def test_phone_page_buttons_and_interactions(client):
    """Verifies phone questionnaire buttons, radios, and reset."""
    res = client.get('/check/phone')
    html = res.data.decode('utf-8')

    assert 'id="btn-submit-phone"' in html
    assert 'id="btn-reset-phone"' in html
    assert 'type="radio"' in html

    # Test POST submission
    post_res = client.post('/analyze/phone', data={'q1': 'no', 'q2': 'yes'})
    assert post_res.status_code == 200


def test_result_page_buttons(client):
    """Verifies result action buttons: copy, share, accordion toggle, feedback, closure."""
    res = client.post('/analyze/sms', data={'sms_text': 'Account locked http://bit.ly/bank'})
    assert res.status_code == 200
    html = res.data.decode('utf-8')

    assert 'id="btn-copy-summary"' in html
    assert 'id="btn-share-warning"' in html
    assert 'id="btn-toggle-details"' in html
    assert 'btn-feedback' in html

    # Feedback API POST
    fb_res = client.post('/api/feedback', json={'helpful': True, 'url': '/analyze/sms'})
    assert fb_res.status_code == 200


def test_history_page_buttons_and_modals(client):
    """Verifies history clear, print, export, and search/filter controls."""
    # First perform a scan to populate history
    client.post('/analyze/sms', data={'sms_text': 'Meeting for coffee tomorrow'})

    res = client.get('/history')
    html = res.data.decode('utf-8')

    assert 'id="btn-print-history"' in html
    assert 'id="btn-open-clear-modal"' in html
    assert 'id="history-search"' in html
    assert 'id="history-filter-level"' in html

    # Test Export CSV endpoint
    csv_res = client.get('/history/export')
    assert csv_res.status_code == 200
    assert 'text/csv' in csv_res.content_type

    # Test Clear History endpoint
    clear_res = client.post('/history/clear', follow_redirects=True)
    assert clear_res.status_code == 200


def test_learn_quiz_buttons(client):
    """Verifies all interactive quiz buttons and feedback containers on Learn page."""
    res = client.get('/learn')
    html = res.data.decode('utf-8')

    assert 'class="quiz-card"' in html
    assert 'class="btn-quiz-opt"' in html
    assert 'data-correct="true"' in html
    assert 'data-correct="false"' in html
    assert 'class="quiz-feedback"' in html
    assert 'data-feedback-correct=' in html
    assert 'data-feedback-wrong=' in html


def test_report_page_buttons(client):
    """Verifies helpline click links and community report submit button."""
    res = client.get('/report')
    html = res.data.decode('utf-8')

    assert 'href="tel:1930"' in html
    assert 'href="https://cybercrime.gov.in"' in html
    assert 'type="submit"' in html

    # Test report form submission
    post_res = client.post('/report', data={
        'scam_type': 'phone',
        'offender_info': '+91 9123456789',
        'scam_details': 'Caller claimed to be police officer demanding money.'
    })
    assert post_res.status_code == 200
    res_text = post_res.data.decode('utf-8')
    assert 'Report Received' in res_text or 'तक्रार प्राप्त' in res_text or 'रिपोर्ट प्राप्त' in res_text
