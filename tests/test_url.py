"""
Unit and Integration Tests for URL Feature Extraction and ML Classification
"""

import pytest
from ml.feature_extraction import extract_url_features, FEATURE_NAMES
from ml.prediction import url_predictor


def test_url_feature_extraction():
    url = "http://192.168.1.1:8080/secure-login/bank/verify.php?user=test&token=123"
    feats = extract_url_features(url)
    
    assert feats["has_ip_address"] == 1
    assert feats["has_https"] == 0
    assert feats["suspicious_keyword_count"] >= 3  # secure, login, bank, verify
    assert feats["count_dots"] >= 4
    assert feats["count_question"] == 1
    assert feats["count_equal"] == 2
    assert len(feats) == len(FEATURE_NAMES)


def test_url_shortener_detection():
    short_url = "https://bit.ly/claim-prize-100"
    feats = extract_url_features(short_url)
    assert feats["is_shortened"] == 1


def test_url_predictor_available():
    assert url_predictor.is_available() is True


def test_url_prediction_safe_sample():
    safe_url = "https://www.google.com"
    result = url_predictor.predict(safe_url)
    assert result["available"] is True
    assert result["prediction"] == 0
    assert result["probability"] < 0.5


def test_url_prediction_malicious_sample():
    mal_url = "http://192.168.1.50/paypal-security/account-verify/signin/update.html"
    result = url_predictor.predict(mal_url)
    assert result["available"] is True
    assert result["prediction"] == 1
    assert result["probability"] > 0.5
