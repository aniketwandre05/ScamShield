"""
Train URL Phishing / Malicious Classification Model
Extracts 17 handcrafted lexical and structural features and trains a Random Forest Classifier.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RAW_DATA_DIR, MODELS_DIR, REPORTS_DIR, URL_MODEL_PATH, URL_SCALER_PATH
from ml.feature_extraction import extract_url_features, FEATURE_NAMES


def load_url_dataset():
    data_path = RAW_DATA_DIR / "url_dataset.csv"
    if not data_path.exists():
        fallback_path = Path(__file__).resolve().parent.parent / "URL" / "balanced_urls.csv"
        if fallback_path.exists():
            data_path = fallback_path
        else:
            raise FileNotFoundError(f"URL dataset not found at {data_path} or {fallback_path}")
            
    try:
        df = pd.read_csv(data_path, encoding='utf-8')
    except Exception:
        df = pd.read_csv(data_path, encoding='latin-1', encoding_errors='ignore')
    
    # Identify url and label columns
    if 'url' in df.columns and 'result' in df.columns:
        df = df[['url', 'result']].rename(columns={'result': 'target'})
    elif 'url' in df.columns and 'label' in df.columns:
        df['target'] = df['label'].astype(str).str.lower().map({
            'benign': 0, 'safe': 0, 'good': 0, '0': 0,
            'malicious': 1, 'bad': 1, 'phishing': 1, 'scam': 1, '1': 1, 'defacement': 1, 'malware': 1
        })
        df = df[['url', 'target']]
    else:
        df = df.iloc[:, :2]
        df.columns = ['url', 'target']
        
    df = df.dropna(subset=['url', 'target'])
    df['target'] = df['target'].astype(int)
    return df


def train_url_model():
    print("=" * 60)
    print("Training URL Malicious / Scam Detection Model")
    print("=" * 60)
    
    df = load_url_dataset()
    print(f"Loaded {len(df)} URL records.")
    print(f"Class distribution: {df['target'].value_counts().to_dict()} (0=Benign/Safe, 1=Malicious/Scam)")
    
    # Sample 40,000 balanced records (20k benign, 20k malicious) for feature extraction and training
    if len(df) > 40000:
        print("Sampling 40,000 balanced URLs for feature extraction and training...")
        df_safe = df[df['target'] == 0].sample(n=min(20000, sum(df['target'] == 0)), random_state=42)
        df_mal = df[df['target'] == 1].sample(n=min(20000, sum(df['target'] == 1)), random_state=42)
        df = pd.concat([df_safe, df_mal]).sample(frac=1, random_state=42).reset_index(drop=True)
        print(f"Sampled dataset size: {len(df)}")
        
    print("Extracting handcrafted URL lexical features...")
    # Extract features
    features_list = []
    for idx, row in df.iterrows():
        feat = extract_url_features(str(row['url']))
        features_list.append([feat[k] for k in FEATURE_NAMES])
        if (idx + 1) % 10000 == 0 or idx + 1 == len(df):
            print(f"  Extracted {idx + 1}/{len(df)} URLs...")
            
    X = np.array(features_list, dtype=float)
    y = df['target'].values
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    
    # Train Random Forest Classifier
    print("Training Random Forest Classifier (100 estimators, max_depth=15)...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n--- URL Model Evaluation Results ---")
    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f} ({prec*100:.2f}%)")
    print(f"Recall:    {rec:.4f} ({rec*100:.2f}%)")
    print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
    print(f"ROC-AUC:   {roc_auc:.4f} ({roc_auc*100:.2f}%)")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Benign URL', 'Malicious/Scam URL']))
    
    # Print Feature Importances
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    print("\nTop 5 Most Important URL Features:")
    for i in range(min(5, len(FEATURE_NAMES))):
        print(f"  {i+1}. {FEATURE_NAMES[sorted_idx[i]]}: {importances[sorted_idx[i]]:.4f}")
        
    # Save model and feature list
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, URL_MODEL_PATH)
    joblib.dump(FEATURE_NAMES, URL_SCALER_PATH)  # saves feature specification
    print(f"Saved URL model to {URL_MODEL_PATH}")
    
    # Save report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "url_evaluation.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SCAMSHIELD URL MODEL EVALUATION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Algorithm: Random Forest (100 estimators, max_depth=15) on 17 Handcrafted Lexical Features\n")
        f.write(f"Features: {', '.join(FEATURE_NAMES)}\n")
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
        f.write("Top 5 Feature Importances:\n")
        for i in range(min(5, len(FEATURE_NAMES))):
            f.write(f"  {i+1}. {FEATURE_NAMES[sorted_idx[i]]}: {importances[sorted_idx[i]]:.4f}\n")
        f.write("\nDetailed Classification Report:\n")
        f.write(classification_report(y_test, y_pred, target_names=['Benign URL', 'Malicious/Scam URL']))
        
    print(f"Saved evaluation report to {report_path}")
    return model, {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "roc_auc": roc_auc}


if __name__ == "__main__":
    train_url_model()
