"""
Unit and Integration Tests for Email Phishing Detection Module
"""

import pytest
from ml.preprocessing import clean_text
from ml.prediction import email_predictor


def test_email_predictor_available():
    assert email_predictor.is_available() is True


def test_email_prediction_safe_sample():
    safe_body = "Hi team, attached is the project roadmap for Q3 review. Please check before Friday sync meeting."
    result = email_predictor.predict(subject="Project Roadmap", body=safe_body, sender="manager@company.org")
    assert result["available"] is True
    assert result["prediction"] == 0
    assert result["probability"] < 0.5


def test_email_prediction_phishing_sample():
    phish_body = "Dear Customer, your PayPal account was accessed from an unknown location. To restore access and verify your debit card and password, visit http://192.168.1.10/paypal-security immediately or your account will be deleted permanently."
    result = email_predictor.predict(
        subject="URGENT: Account Restricted",
        body=phish_body,
        sender="security@paypal-update-center.xyz"
    )
    assert result["available"] is True
    assert result["prediction"] == 1
    assert result["probability"] > 0.5


def test_email_empty_input():
    result = email_predictor.predict(subject="", body="", sender="")
    assert result["available"] is True
    assert result["prediction"] == 0
