"""
Train Phishing Email Scam Classification Model
Uses TF-IDF Vectorizer and Logistic Regression with balanced weights.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RAW_DATA_DIR, MODELS_DIR, REPORTS_DIR, EMAIL_MODEL_PATH, EMAIL_VECTORIZER_PATH
from ml.preprocessing import clean_text


def load_email_dataset():
    data_path = RAW_DATA_DIR / "email_phishing.csv"
    if not data_path.exists():
        fallback_path = Path(__file__).resolve().parent.parent / "Email" / "phishing_email.csv"
        if fallback_path.exists():
            data_path = fallback_path
        else:
            raise FileNotFoundError(f"Email dataset not found at {data_path} or {fallback_path}")
            
    try:
        df = pd.read_csv(data_path, encoding='utf-8')
    except Exception:
        df = pd.read_csv(data_path, encoding='latin-1', encoding_errors='ignore')
    
    # Identify text and label columns
    if 'text_combined' in df.columns and 'label' in df.columns:
        df = df[['text_combined', 'label']].rename(columns={'text_combined': 'text'})
    elif 'body' in df.columns and 'label' in df.columns:
        if 'subject' in df.columns:
            df['text'] = df['subject'].fillna('') + " " + df['body'].fillna('')
        else:
            df['text'] = df['body']
        df = df[['text', 'label']]
    elif 'Email Text' in df.columns and 'Email Type' in df.columns:
        df = df[['Email Text', 'Email Type']].rename(columns={'Email Text': 'text', 'Email Type': 'label'})
    else:
        df = df.iloc[:, :2]
        df.columns = ['text', 'label']
        
    # Map label to binary (0=Safe, 1=Phishing/Scam)
    if df['label'].dtype == object:
        df['label'] = df['label'].astype(str).str.lower().str.strip()
        df['target'] = df['label'].map({'safe email': 0, 'phishing email': 1, 'ham': 0, 'spam': 1, '0': 0, '1': 1, 'safe': 0, 'scam': 1})
    else:
        df['target'] = df['label'].astype(int)
        
    df = df.dropna(subset=['text', 'target'])
    df['target'] = df['target'].astype(int)
    return df


def train_email_model():
    print("=" * 60)
    print("Training Phishing Email Detection Model")
    print("=" * 60)
    
    df = load_email_dataset()
    print(f"Loaded {len(df)} Email records.")
    print(f"Class distribution: {df['target'].value_counts().to_dict()} (0=Safe, 1=Phishing/Scam)")
    
    # If dataset is very large (>50,000), sample evenly up to 40,000 for fast optimal training while preserving high accuracy
    if len(df) > 40000:
        print("Sampling 40,000 balanced records for optimal memory and fast training...")
        df_safe = df[df['target'] == 0].sample(n=min(20000, sum(df['target'] == 0)), random_state=42)
        df_scam = df[df['target'] == 1].sample(n=min(20000, sum(df['target'] == 1)), random_state=42)
        df = pd.concat([df_safe, df_scam]).sample(frac=1, random_state=42).reset_index(drop=True)
        print(f"Sampled dataset size: {len(df)}")
        
    print("Cleaning text...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        df['cleaned_text'], df['target'],
        test_size=0.2, random_state=42, stratify=df['target']
    )
    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    
    # Vectorize with TF-IDF (1-2 ngrams, 10,000 max features, min_df=2)
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Logistic Regression
    print("Training Logistic Regression Model...")
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    y_pred_proba = model.predict_proba(X_test_vec)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n--- Email Model Evaluation Results ---")
    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f} ({prec*100:.2f}%)")
    print(f"Recall:    {rec:.4f} ({rec*100:.2f}%)")
    print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
    print(f"ROC-AUC:   {roc_auc:.4f} ({roc_auc*100:.2f}%)")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe Email', 'Phishing/Scam Email']))
    
    # Save models
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, EMAIL_MODEL_PATH)
    joblib.dump(vectorizer, EMAIL_VECTORIZER_PATH)
    print(f"Saved Email model to {EMAIL_MODEL_PATH}")
    print(f"Saved Email vectorizer to {EMAIL_VECTORIZER_PATH}")
    
    # Save report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "email_evaluation.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SCAMSHIELD EMAIL MODEL EVALUATION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Algorithm: TF-IDF (1-2 ngrams, 10,000 max features) + Logistic Regression (C=2.0, balanced)\n")
        f.write(f"Total Processed Samples: {len(df)}\n")
        f.write(f"Train Size: {len(X_train)}, Test Size: {len(X_test)}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Accuracy:  {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall:    {rec:.4f}\n")
        f.write(f"F1 Score:  {f1:.4f}\n")
        f.write(f"ROC-AUC:   {roc_auc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(f"[[TN={cm[0][0]}, FP={cm[0][1]}],\n [FN={cm[1][0]}, TP={cm[1][1]}]]\n\n")
        f.write("Detailed Classification Report:\n")
        f.write(classification_report(y_test, y_pred, target_names=['Safe Email', 'Phishing/Scam Email']))
        
    print(f"Saved evaluation report to {report_path}")
    return model, vectorizer, {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "roc_auc": roc_auc}


if __name__ == "__main__":
    train_email_model()
