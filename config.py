"""
ScamShield Configuration Module
Defines paths, thresholds, model settings, and security constants.
"""

import os
from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
UPLOADS_DIR = BASE_DIR / "uploads"
DEMO_SAMPLES_DIR = BASE_DIR / "demo_samples"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure runtime directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application Settings
SECRET_KEY = os.getenv("SECRET_KEY", "scamshield-default-dev-secret-key-2026")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Model Paths
SMS_MODEL_PATH = MODELS_DIR / "sms_model.pkl"
SMS_VECTORIZER_PATH = MODELS_DIR / "sms_vectorizer.pkl"

EMAIL_MODEL_PATH = MODELS_DIR / "email_model.pkl"
EMAIL_VECTORIZER_PATH = MODELS_DIR / "email_vectorizer.pkl"

URL_MODEL_PATH = MODELS_DIR / "url_model.pkl"
URL_SCALER_PATH = MODELS_DIR / "url_scaler.pkl"

# Risk Thresholds
# 0-29: LOW RISK, 30-59: MEDIUM RISK, 60-100: HIGH RISK
RISK_THRESHOLDS = {
    "LOW_MAX": 29,
    "MEDIUM_MAX": 59,
    "HIGH_MIN": 60,
}

# Risk Levels Display Metadata
RISK_LEVEL_META = {
    "LOW": {
        "label": "Potentially Safe",
        "badge_class": "badge-safe",
        "color": "#16a34a",
        "icon": "shield-check",
        "summary": "This content shows no immediate signs of scam activity, but always remain vigilant."
    },
    "MEDIUM": {
        "label": "Suspicious (Medium Risk)",
        "badge_class": "badge-warning",
        "color": "#d97706",
        "icon": "exclamation-triangle",
        "summary": "This content exhibits some suspicious indicators. Proceed with caution."
    },
    "HIGH": {
        "label": "Potential Scam (High Risk)",
        "badge_class": "badge-danger",
        "color": "#dc2626",
        "icon": "shield-exclamation",
        "summary": "High likelihood of scam or phishing attempt. Do not share information or click links."
    }
}
