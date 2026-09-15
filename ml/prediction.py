"""
Unified Machine Learning Prediction Interface
Provides loaded model caching, inference execution, and probability calibration for SMS, Email, and URL inputs.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import joblib
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import SMS_MODEL_PATH, SMS_VECTORIZER_PATH, EMAIL_MODEL_PATH, EMAIL_VECTORIZER_PATH, URL_MODEL_PATH, URL_SCALER_PATH
from ml.preprocessing import clean_text
from ml.feature_extraction import extract_url_features, FEATURE_NAMES


class BasePredictor:
    """Base class for loaded models with lazy loading and availability checks."""
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._is_loaded = False
        
    def is_available(self) -> bool:
        raise NotImplementedError
        
    def load(self) -> bool:
        raise NotImplementedError


class SMSPredictor(BasePredictor):
    """Predictor for SMS and WhatsApp text messages."""
    
    def is_available(self) -> bool:
        return SMS_MODEL_PATH.exists() and SMS_VECTORIZER_PATH.exists()
        
    def load(self) -> bool:
        if not self.is_available():
            return False
        if not self._is_loaded:
            try:
                self.model = joblib.load(SMS_MODEL_PATH)
                self.vectorizer = joblib.load(SMS_VECTORIZER_PATH)
                self._is_loaded = True
            except Exception as e:
                print(f"Error loading SMS model: {e}")
                return False
        return True
        
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs ML prediction on SMS text.
        Returns prediction (0=Safe, 1=Scam), probability, and status.
        """
        if not self.load():
            return {
                "available": False,
                "error": "SMS ML model is not trained yet. Please run the training script.",
                "prediction": 0,
                "probability": 0.0,
                "label": "Unknown"
            }
            
        cleaned = clean_text(text)
        if not cleaned:
            return {
                "available": True,
                "prediction": 0,
                "probability": 0.0,
                "label": "Safe",
                "message": "Empty text provided"
            }
            
        vec = self.vectorizer.transform([cleaned])
        prob = float(self.model.predict_proba(vec)[0, 1])
        pred = int(prob >= 0.5)
        
        return {
            "available": True,
            "prediction": pred,
            "probability": prob,
            "label": "Potential Scam" if pred == 1 else "Potentially Safe",
            "cleaned_text": cleaned
        }


class EmailPredictor(BasePredictor):
    """Predictor for Email content (Subject + Body)."""
    
    def is_available(self) -> bool:
        return EMAIL_MODEL_PATH.exists() and EMAIL_VECTORIZER_PATH.exists()
        
    def load(self) -> bool:
        if not self.is_available():
            return False
        if not self._is_loaded:
            try:
                self.model = joblib.load(EMAIL_MODEL_PATH)
                self.vectorizer = joblib.load(EMAIL_VECTORIZER_PATH)
                self._is_loaded = True
            except Exception as e:
                print(f"Error loading Email model: {e}")
                return False
        return True
        
    def predict(self, subject: str = "", body: str = "", sender: str = "") -> Dict[str, Any]:
        """
        Runs ML prediction on Email content.
        """
        if not self.load():
            return {
                "available": False,
                "error": "Email ML model is not trained yet. Please run the training script.",
                "prediction": 0,
                "probability": 0.0,
                "label": "Unknown"
            }
            
        combined_text = f"{subject} {body}".strip()
        cleaned = clean_text(combined_text)
        
        if not cleaned:
            return {
                "available": True,
                "prediction": 0,
                "probability": 0.0,
                "label": "Safe",
                "message": "Empty email content provided"
            }
            
        vec = self.vectorizer.transform([cleaned])
        prob = float(self.model.predict_proba(vec)[0, 1])
        pred = int(prob >= 0.5)
        
        return {
            "available": True,
            "prediction": pred,
            "probability": prob,
            "label": "Potential Phishing / Scam" if pred == 1 else "Potentially Safe",
            "cleaned_text": cleaned
        }


class URLPredictor(BasePredictor):
    """Predictor for URL safety using Handcrafted Lexical Features."""
    
    def is_available(self) -> bool:
        return URL_MODEL_PATH.exists()
        
    def load(self) -> bool:
        if not self.is_available():
            return False
        if not self._is_loaded:
            try:
                self.model = joblib.load(URL_MODEL_PATH)
                self._is_loaded = True
            except Exception as e:
                print(f"Error loading URL model: {e}")
                return False
        return True
        
    def predict(self, url: str) -> Dict[str, Any]:
        """
        Runs ML prediction on URL string.
        """
        if not self.load():
            return {
                "available": False,
                "error": "URL ML model is not trained yet. Please run the training script.",
                "prediction": 0,
                "probability": 0.0,
                "label": "Unknown",
                "features": {}
            }
            
        if not isinstance(url, str) or not url.strip():
            return {
                "available": True,
                "prediction": 0,
                "probability": 0.0,
                "label": "Safe",
                "features": {}
            }
            
        url = url.strip()
        features = extract_url_features(url)
        feat_vector = np.array([features[k] for k in FEATURE_NAMES], dtype=float).reshape(1, -1)
        
        prob = float(self.model.predict_proba(feat_vector)[0, 1])
        pred = int(prob >= 0.5)
        
        return {
            "available": True,
            "url": url,
            "prediction": pred,
            "probability": prob,
            "label": "Suspicious / Malicious URL" if pred == 1 else "Potentially Safe URL",
            "features": features
        }


# Singleton instances for reuse
sms_predictor = SMSPredictor()
email_predictor = EmailPredictor()
url_predictor = URLPredictor()
