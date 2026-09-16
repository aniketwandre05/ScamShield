"""
ScamShield Flask Application
Main controller handling HTTP routing, OCR screenshot uploads, ML model integration,
hybrid risk scoring, accessibility views, and local history.
"""

import os
import sys
import uuid
import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

# Ensure root directory is on python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import (
    SECRET_KEY, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS,
    UPLOADS_DIR, SMS_MODEL_PATH, EMAIL_MODEL_PATH, URL_MODEL_PATH
)
from ocr.ocr_engine import extract_text_from_image
from ocr.content_detector import detect_content_structure
from risk.risk_engine import compute_hybrid_risk
from risk.phone_risk import PHONE_QUESTIONS, assess_phone_call_risk, get_localized_phone_questions
from translations import get_text, TRANSLATIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


@app.context_processor
def inject_localization():
    lang = session.get('lang', 'en')
    if lang not in ('en', 'mr', 'hi'):
        lang = 'en'
    return dict(
        t=lambda k: get_text(k, lang),
        current_lang=lang
    )


@app.route('/set_language/<lang>')
def set_language(lang):
    """Switches active session language (en, mr, hi) and redirects back to referring page."""
    if lang in ('en', 'mr', 'hi'):
        session['lang'] = lang
        session.modified = True
    return redirect(request.referrer or url_for('index'))


def is_allowed_file(filename: str) -> bool:
    """Checks if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_to_history(content_type: str, snippet: str, result: dict):
    """Safely saves non-sensitive scan result summary into user session history."""
    if 'scan_history' not in session:
        session['scan_history'] = []
        
    history = session['scan_history']
    
    # Truncate snippet for privacy and size
    clean_snippet = (snippet[:80] + '...') if len(snippet) > 80 else snippet
    if not clean_snippet.strip():
        clean_snippet = f"{content_type.upper()} Assessment"
        
    history_entry = {
        "id": str(uuid.uuid4())[:8],
        "content_type": content_type,
        "snippet": clean_snippet,
        "risk_score": result.get("risk_score", 0),
        "risk_level": result.get("risk_level", "LOW"),
        "risk_label": result.get("risk_label", "Potentially Safe"),
        "badge_class": result.get("badge_class", "badge-safe"),
        "color": result.get("color", "#16a34a"),
        "timestamp": datetime.datetime.now().strftime("%b %d, %Y %I:%M %p")
    }
    
    # Keep last 15 items
    history.insert(0, history_entry)
    session['scan_history'] = history[:15]
    session.modified = True


@app.route('/')
def index():
    """Home page displaying the four primary check cards."""
    return render_template('index.html')


@app.route('/check/sms')
def check_sms():
    """SMS / WhatsApp message check form."""
    return render_template('sms.html')


@app.route('/analyze/sms', methods=['POST'])
def analyze_sms():
    """Processes SMS text or uploaded screenshot."""
    lang = session.get('lang', 'en')
    input_mode = request.form.get('input_mode', 'text')
    ocr_used = False
    analyzed_text = ""
    override_urls = None
    
    if input_mode == 'screenshot':
        if 'screenshot' not in request.files:
            return render_template('error.html', 
                error_title="No File Selected",
                error_message="Please choose a screenshot image file to scan.",
                return_url=url_for('check_sms'))
                
        file = request.files['screenshot']
        if file.filename == '':
            return render_template('error.html',
                error_title="No File Selected",
                error_message="Please select a valid image file from your device.",
                return_url=url_for('check_sms'))
                
        if not is_allowed_file(file.filename):
            return render_template('error.html',
                error_title="Unsupported File Format",
                error_message="Please upload a PNG, JPG, JPEG, or WEBP image.",
                return_url=url_for('check_sms'))
                
        # Save temporary file for OCR
        safe_name = f"sms_{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        temp_path = UPLOADS_DIR / safe_name
        try:
            file.save(temp_path)
            ocr_res = extract_text_from_image(str(temp_path), lang=lang)
        finally:
            # Clean up temp file immediately
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
                    
        if not ocr_res.get("success"):
            return render_template('error.html',
                error_title="Could Not Read Screenshot",
                error_message=ocr_res.get("error", "The image was blurry or contained no readable text. Please try pasting the message text instead."),
                return_url=url_for('check_sms'))
                
        ocr_used = True
        analyzed_text = ocr_res["text"]
        
        # Detect content structure and extracted URLs
        detected = detect_content_structure(analyzed_text)
        override_urls = detected.get("urls", [])
        
    else:
        analyzed_text = request.form.get('sms_text', '').strip()
        if not analyzed_text:
            return render_template('error.html',
                error_title="Empty Message",
                error_message="Please enter or paste the message text you would like to check.",
                return_url=url_for('check_sms'))
                
    # Run hybrid risk assessment
    result = compute_hybrid_risk('sms', text=analyzed_text, override_urls=override_urls, lang=lang)
    result['risk_label'] = get_text(f"risk_{result['risk_level'].lower()}", lang)
    result['summary'] = get_text(f"risk_{result['risk_level'].lower()}_summary", lang)
    add_to_history('SMS', analyzed_text, result)
    
    result['display_type'] = get_text('sms_display_type', lang)
    result['ocr_used'] = ocr_used
    result['preview_text'] = (analyzed_text[:180] + '...') if len(analyzed_text) > 180 else analyzed_text
    
    return render_template('result.html', **result)


@app.route('/check/email')
def check_email():
    """Email phishing check form."""
    return render_template('email.html')


@app.route('/analyze/email', methods=['POST'])
def analyze_email():
    """Processes Email content or uploaded screenshot."""
    lang = session.get('lang', 'en')
    input_mode = request.form.get('input_mode', 'text')
    ocr_used = False
    subject = ""
    body = ""
    sender = ""
    override_urls = None
    
    if input_mode == 'screenshot':
        if 'screenshot' not in request.files:
            return render_template('error.html', 
                error_title="No File Selected",
                error_message="Please choose a screenshot image file to scan.",
                return_url=url_for('check_email'))
                
        file = request.files['screenshot']
        if file.filename == '':
            return render_template('error.html',
                error_title="No File Selected",
                error_message="Please select a valid image file from your device.",
                return_url=url_for('check_email'))
                
        if not is_allowed_file(file.filename):
            return render_template('error.html',
                error_title="Unsupported File Format",
                error_message="Please upload a PNG, JPG, JPEG, or WEBP image.",
                return_url=url_for('check_email'))
                
        safe_name = f"email_{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        temp_path = UPLOADS_DIR / safe_name
        try:
            file.save(temp_path)
            ocr_res = extract_text_from_image(str(temp_path), lang=lang)
        finally:
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
                    
        if not ocr_res.get("success"):
            return render_template('error.html',
                error_title="Could Not Read Screenshot",
                error_message=ocr_res.get("error", "The image was blurry or contained no readable text. Please try pasting the email text instead."),
                return_url=url_for('check_email'))
                
        ocr_used = True
        extracted_text = ocr_res["text"]
        detected = detect_content_structure(extracted_text)
        
        subject = detected.get("subject", "Scanned Email Content")
        sender = detected.get("sender", "")
        body = detected.get("body", extracted_text)
        override_urls = detected.get("urls", [])
        
    else:
        subject = request.form.get('email_subject', '').strip()
        body = request.form.get('email_body', '').strip()
        sender = request.form.get('email_sender', '').strip()
        
        if not body and not subject:
            return render_template('error.html',
                error_title="Empty Email Details",
                error_message="Please provide the email subject line or body text.",
                return_url=url_for('check_email'))
                
    # Run hybrid risk assessment
    result = compute_hybrid_risk('email', subject=subject, body=body, sender=sender, override_urls=override_urls, lang=lang)
    result['risk_label'] = get_text(f"risk_{result['risk_level'].lower()}", lang)
    result['summary'] = get_text(f"risk_{result['risk_level'].lower()}_summary", lang)
    preview_snippet = f"Subject: {subject} | Body: {body}" if subject else body
    add_to_history('Email', preview_snippet, result)
    
    result['display_type'] = get_text('email_display_type', lang)
    result['ocr_used'] = ocr_used
    result['preview_text'] = (preview_snippet[:180] + '...') if len(preview_snippet) > 180 else preview_snippet
    
    return render_template('result.html', **result)


@app.route('/check/url')
def check_url():
    """URL link safety checker form."""
    return render_template('url.html')


@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    """Processes URL safety check from pasted link or uploaded screenshot."""
    lang = session.get('lang', 'en')
    input_mode = request.form.get('input_mode', 'text')
    ocr_used = False
    target_url = ""

    if input_mode == 'screenshot':
        if 'screenshot' not in request.files:
            return render_template('error.html',
                error_title="No File Selected",
                error_message="Please choose a screenshot image file to scan.",
                return_url=url_for('check_url'))
                
        file = request.files['screenshot']
        if file.filename == '':
            return render_template('error.html',
                error_title="No File Selected",
                error_message="Please select a valid image file from your device.",
                return_url=url_for('check_url'))
                
        if not is_allowed_file(file.filename):
            return render_template('error.html',
                error_title="Unsupported File Format",
                error_message="Please upload a PNG, JPG, JPEG, or WEBP image.",
                return_url=url_for('check_url'))
                
        safe_name = f"url_{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        temp_path = UPLOADS_DIR / safe_name
        try:
            file.save(temp_path)
            ocr_res = extract_text_from_image(str(temp_path), lang=lang)
        finally:
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

        if not ocr_res.get("success"):
            return render_template('error.html',
                error_title="Could Not Read Screenshot",
                error_message=ocr_res.get("error", "The image was blurry or contained no readable text. Please try pasting the link manually."),
                return_url=url_for('check_url'))

        ocr_used = True
        extracted_text = ocr_res["text"]
        detected = detect_content_structure(extracted_text)
        urls = detected.get("urls", [])

        if not urls:
            # Check if raw text might be a URL without http scheme
            words = extracted_text.split()
            for w in words:
                cleaned_w = w.strip('.,!?:;)"\'>]}')
                if '.' in cleaned_w and len(cleaned_w) > 4:
                    urls.append(cleaned_w)
                    break

        if not urls:
            return render_template('error.html',
                error_title="No Link Found in Screenshot",
                error_message=f"We could read text from this image ('{extracted_text[:100]}...'), but could not identify a valid website link (URL). Please paste the link manually.",
                return_url=url_for('check_url'))

        target_url = urls[0]

    else:
        target_url = request.form.get('url_input', '').strip()
        if not target_url:
            return render_template('error.html',
                error_title="Empty URL Link",
                error_message="Please paste a website link (URL) to check.",
                return_url=url_for('check_url'))
            
    result = compute_hybrid_risk('url', url=target_url, lang=lang)
    result['risk_label'] = get_text(f"risk_{result['risk_level'].lower()}", lang)
    result['summary'] = get_text(f"risk_{result['risk_level'].lower()}_summary", lang)
    add_to_history('URL', target_url, result)
    
    result['display_type'] = get_text('url_display_type', lang)
    result['ocr_used'] = ocr_used
    result['preview_text'] = target_url
    
    return render_template('result.html', **result)


@app.route('/check/phone')
def check_phone():
    """Phone call questionnaire view."""
    lang = session.get('lang', 'en')
    return render_template('phone.html', questions=get_localized_phone_questions(lang))


@app.route('/analyze/phone', methods=['POST'])
def analyze_phone():
    """Evaluates the 10-question phone call responses."""
    lang = session.get('lang', 'en')
    answers = {}
    for q in PHONE_QUESTIONS:
        qid = q["id"]
        val = request.form.get(qid, "no")
        answers[qid] = val
        
    result = assess_phone_call_risk(answers, lang=lang)
    snippet = f"Suspicious Call Check ({result['matched_count']}/{result['total_questions']} warning flags)"
    add_to_history('Phone Call', snippet, result)
    
    result['content_type'] = 'phone'
    result['display_type'] = get_text('phone_display_type', lang)
    result['ocr_used'] = False
    result['preview_text'] = snippet
    
    return render_template('result.html', **result)


@app.route('/history')
def view_history():
    """Displays local session scan history."""
    history = session.get('scan_history', [])
    return render_template('history.html', history=history)


@app.route('/history/clear', methods=['POST'])
def clear_history():
    """Clears local session scan history."""
    session['scan_history'] = []
    session.modified = True
    flash("Scan history has been cleared.", "info")
    return redirect(url_for('view_history'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
        error_title="Page Not Found (404)",
        error_message="The page you requested does not exist.",
        return_url=url_for('index')), 404


@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template('error.html',
        error_title="File Too Large",
        error_message="The uploaded screenshot exceeds the maximum allowed size of 16 MB.",
        return_url=url_for('index')), 413


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
        error_title="Application Notice",
        error_message="Something unexpected happened while processing your request. Please try again.",
        return_url=url_for('index')), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Starting ScamShield Server on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
