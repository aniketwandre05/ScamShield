"""
Unit and Integration Tests for SMS Scam Detection Module
"""

import pytest
from ml.preprocessing import clean_text, extract_urls
from ml.prediction import sms_predictor


def test_sms_preprocessing():
    raw = "  URGENT! <b>Your Account</b> is locked! Visit http://scam.xyz/login now!  "
    cleaned = clean_text(raw)
    assert "urgent" in cleaned
    assert "<b>" not in cleaned
    assert "<b>" not in cleaned


def test_sms_url_extraction():
    msg = "Click https://bank-verify.com/login and http://bit.ly/123 to claim."
    urls = extract_urls(msg)
    assert len(urls) == 2
    assert "https://bank-verify.com/login" in urls
    assert "http://bit.ly/123" in urls


def test_sms_prediction_available():
    assert sms_predictor.is_available() is True


def test_sms_prediction_safe_sample():
    safe_text = "Hey are we still meeting for lunch tomorrow at 1 PM?"
    result = sms_predictor.predict(safe_text)
    assert result["available"] is True
    assert result["prediction"] == 0
    assert result["probability"] < 0.5


def test_sms_prediction_scam_sample():
    scam_text = "URGENT: Your Bank account has been blocked due to suspicious activity. Verify identity at http://bit.ly/bank-kyc or service will be closed."
    result = sms_predictor.predict(scam_text)
    assert result["available"] is True
    assert result["prediction"] == 1
    assert result["probability"] > 0.5
