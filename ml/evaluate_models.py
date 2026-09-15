"""
Model Evaluation and Metrics Aggregator
Evaluates all trained models (SMS, Email, URL) and generates a unified performance report.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import REPORTS_DIR, SMS_MODEL_PATH, SMS_VECTORIZER_PATH, EMAIL_MODEL_PATH, EMAIL_VECTORIZER_PATH, URL_MODEL_PATH
from ml.train_sms_model import load_sms_dataset
from ml.train_email_model import load_email_dataset
from ml.train_url_model import load_url_dataset
from ml.preprocessing import clean_text
from ml.feature_extraction import extract_url_features, FEATURE_NAMES
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report


def evaluate_all():
    print("=" * 70)
    print("SCAMSHIELD: EVALUATING ALL MACHINE LEARNING MODELS")
    print("=" * 70)
    
    results = []
    
    # 1. SMS Model
    if SMS_MODEL_PATH.exists() and SMS_VECTORIZER_PATH.exists():
        print("\n[1/3] Evaluating SMS Model...")
        sms_model = joblib.load(SMS_MODEL_PATH)
        sms_vec = joblib.load(SMS_VECTORIZER_PATH)
        df_sms = load_sms_dataset()
        df_sms['cleaned'] = df_sms['text'].apply(clean_text)
        
        # Sample test set for verification
        test_sample = df_sms.sample(n=min(1000, len(df_sms)), random_state=123)
        X_test = sms_vec.transform(test_sample['cleaned'])
        y_test = test_sample['target']
        
        preds = sms_model.predict(X_test)
        probs = sms_model.predict_proba(X_test)[:, 1]
        
        results.append({
            "Module": "SMS Message",
            "Model": "TF-IDF + Logistic Regression",
            "Accuracy": accuracy_score(y_test, preds),
            "Precision": precision_score(y_test, preds, zero_division=0),
            "Recall": recall_score(y_test, preds, zero_division=0),
            "F1-Score": f1_score(y_test, preds, zero_division=0),
            "ROC-AUC": roc_auc_score(y_test, probs)
        })
    else:
        print("[!] SMS Model not found. Run ml/train_sms_model.py first.")
        
    # 2. Email Model
    if EMAIL_MODEL_PATH.exists() and EMAIL_VECTORIZER_PATH.exists():
        print("\n[2/3] Evaluating Email Phishing Model...")
        email_model = joblib.load(EMAIL_MODEL_PATH)
        email_vec = joblib.load(EMAIL_VECTORIZER_PATH)
        df_email = load_email_dataset()
        
        test_sample = df_email.sample(n=min(2000, len(df_email)), random_state=123)
        test_sample['cleaned'] = test_sample['text'].apply(clean_text)
        X_test = email_vec.transform(test_sample['cleaned'])
        y_test = test_sample['target']
        
        preds = email_model.predict(X_test)
        probs = email_model.predict_proba(X_test)[:, 1]
        
        results.append({
            "Module": "Email Phishing",
            "Model": "TF-IDF + Logistic Regression",
            "Accuracy": accuracy_score(y_test, preds),
            "Precision": precision_score(y_test, preds, zero_division=0),
            "Recall": recall_score(y_test, preds, zero_division=0),
            "F1-Score": f1_score(y_test, preds, zero_division=0),
            "ROC-AUC": roc_auc_score(y_test, probs)
        })
    else:
        print("[!] Email Model not found. Run ml/train_email_model.py first.")
        
    # 3. URL Model
    if URL_MODEL_PATH.exists():
        print("\n[3/3] Evaluating URL Malicious Model...")
        url_model = joblib.load(URL_MODEL_PATH)
        df_url = load_url_dataset()
        
        test_sample = df_url.sample(n=min(2000, len(df_url)), random_state=123)
        feat_list = []
        for u in test_sample['url']:
            f = extract_url_features(str(u))
            feat_list.append([f[k] for k in FEATURE_NAMES])
        X_test = np.array(feat_list, dtype=float)
        y_test = test_sample['target'].values
        
        preds = url_model.predict(X_test)
        probs = url_model.predict_proba(X_test)[:, 1]
        
        results.append({
            "Module": "URL / Links",
            "Model": "Handcrafted Features + Random Forest",
            "Accuracy": accuracy_score(y_test, preds),
            "Precision": precision_score(y_test, preds, zero_division=0),
            "Recall": recall_score(y_test, preds, zero_division=0),
            "F1-Score": f1_score(y_test, preds, zero_division=0),
            "ROC-AUC": roc_auc_score(y_test, probs)
        })
    else:
        print("[!] URL Model not found. Run ml/train_url_model.py first.")
        
    if results:
        res_df = pd.DataFrame(results)
        print("\n" + "=" * 70)
        print("SUMMARY EVALUATION METRICS TABLE")
        print("=" * 70)
        print(res_df.to_string(index=False))
        
        summary_path = REPORTS_DIR / "overall_summary_evaluation.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("SCAMSHIELD: OVERALL HYBRID ML SYSTEM EVALUATION METRICS\n")
            f.write("=" * 70 + "\n\n")
            f.write(res_df.to_string(index=False))
            f.write("\n\nNote: All metrics computed on held-out test distributions.")
        print(f"\nSaved overall summary report to {summary_path}")


if __name__ == "__main__":
    evaluate_all()
