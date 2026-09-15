"""
Unit Tests for Hybrid Risk Engine, Rule Heuristics, and Phone Questionnaire
"""

import pytest
from risk.rules import evaluate_rules
from risk.risk_engine import compute_hybrid_risk
from risk.phone_risk import assess_phone_call_risk


def test_rule_evaluation_otp():
    text = "Please share the 6-digit OTP sent to your phone to confirm transaction."
    res = evaluate_rules(text)
    assert "RULE_OTP_REQUEST" in res["matched_rules"]
    assert res["rule_score"] >= 25


def test_rule_evaluation_financial():
    text = "Kindly send payment using a $100 iTunes gift card or Western Union wire."
    res = evaluate_rules(text)
    assert "RULE_FINANCIAL_DEMAND" in res["matched_rules"]


def test_hybrid_risk_safe_sms():
    res = compute_hybrid_risk('sms', text="Hello, dinner is ready at home.")
    assert res["risk_score"] < 30
    assert res["risk_level"] == "LOW"


def test_hybrid_risk_scam_sms():
    scam_msg = "URGENT: Your account is suspended. Send OTP and verify card: http://bit.ly/bank-verify"
    res = compute_hybrid_risk('sms', text=scam_msg)
    assert res["risk_score"] >= 60
    assert res["risk_level"] == "HIGH"
    assert len(res["reasons"]) >= 1
    assert len(res["actions"]) >= 1


def test_phone_call_low_risk():
    answers = {"q1": "no", "q2": "no", "q3": "no", "q4": "no"}
    res = assess_phone_call_risk(answers)
    assert res["risk_score"] < 30
    assert res["risk_level"] == "LOW"


def test_phone_call_high_risk():
    # Answering YES to OTP, Bank details, and Urgency
    answers = {"q1": "yes", "q2": "yes", "q4": "yes", "q8": "yes"}
    res = assess_phone_call_risk(answers)
    assert res["risk_score"] >= 60
    assert res["risk_level"] == "HIGH"
    assert len(res["reasons"]) >= 3
