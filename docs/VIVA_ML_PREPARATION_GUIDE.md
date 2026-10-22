# SCAMSHIELD: Machine Learning Viva & Project Evaluation Guide
**Project Title:** ScamShield — Multilingual Hybrid AI Scam Detection System  
**Prepared For:** Project Viva, Internal/External Evaluation, and Academic Defense  
**Context:** Pune, Maharashtra, India  

---

## 1. 30-Second Elevator Pitch (The Opening Statement)
> *"ScamShield is a privacy-first, multilingual fraud detection system designed to protect vulnerable users from cyber scams across SMS, Email, and URLs. Instead of relying on a single slow black-box model, ScamShield utilizes a **Modular Hybrid AI Architecture**: three specialized machine learning models (Word+Character n-gram Logistic Regression for SMS, Subject-Boosted Logistic Regression for Email, and a 22-feature Random Forest for URLs) calibrated alongside a deterministic Heuristic Rule Engine. The system achieves over **99% accuracy**, executes inference in under **15 milliseconds**, and provides actionable safety advice in English, Marathi, and Hindi."*

---

## 2. Core Architectural Philosophy: Why Hybrid?
If examiners ask: **"Why not just use one big Deep Learning / LLM model?"**

1. **Feature Space Divergence:**
   - **SMS:** Short, unstructured, colloquial, abbreviations, Hinglish/Marathi code-mixing, high urgency.
   - **Email:** Structured, longer conversational body, subject line intent, sender headers.
   - **URL:** Purely syntactic strings requiring lexical, domain, and character-distribution analysis.
   - *Verdict:* A single text model completely fails on URLs; a URL model cannot parse conversational tone. Specialization yields higher accuracy.
2. **Inference Latency & CPU Efficiency:**
   - LLMs or BERT models take $500\text{ms} - 3000\text{ms}$ and require expensive GPUs.
   - ScamShield’s classical ML models run in **$<15\text{ms}$ on standard CPU hardware**, making real-time analysis instant.
3. **Mathematical Explainability (XAI):**
   - High-stakes security requires clear reasoning. Logistic Regression odds ratios and Random Forest feature importances allow ScamShield to tell the user *why* an input is risky, rather than outputting an opaque score.
4. **Safety via Heuristic Rules:**
   - Pure statistical models can be fooled by zero-day prompt phrasing. Pairing ML probabilities with zero-tolerance rules (e.g., raw IP address links, APK download links, urgent power disconnection threats) guarantees detection of critical fraud vectors.

---

## 3. The Three Machine Learning Models in Detail

### Model A: SMS Scam Classifier
- **Algorithm:** Multinomial / Binomial **Logistic Regression** with balanced class weighting (`class_weight='balanced'`).
- **Regularization:** $L_2$ penalty with tuned parameter $C = 5.0$.
- **Feature Extraction Pipeline:** `FeatureUnion` combining:
  1. **Word-level TF-IDF:** $n$-grams from $1$ to $3$ words, $7,000$ max sublinear features. Captures semantic phrases like `"account suspended"`, `"claim reward"`.
  2. **Character boundary TF-IDF (`char_wb`):** $n$-grams from $3$ to $5$ characters, $7,000$ max sublinear features. Captures typos, obfuscations (`p@ypal`, `s-b-i`, `kyc`), and transliterated Hinglish/Marathi words (`paise`, `bhejo`, `katil`).
- **Dataset:** SMS Spam Collection ($5,572$ records; $4,825$ benign, $747$ spam/scam).
- **Test Set Size:** $1,115$ samples (stratified $80/20$ split).
- **Performance Metrics:**
  - **Accuracy:** **$99.19\%$**
  - **Precision:** **$99.30\%$**
  - **Recall:** **$94.63\%$** (False negatives reduced from 17 down to only 8!)
  - **F1-Score:** **$96.91\%$**
  - **ROC-AUC:** **$0.9944$**
- **Confusion Matrix ($N = 1,115$):**
  - $\text{True Negatives (Safe)} = 965$
  - $\text{False Positives (Safe called Scam)} = 1$
  - $\text{False Negatives (Scam missed)} = 8$
  - $\text{True Positives (Scam caught)} = 141$

---

### Model B: Phishing Email Classifier
- **Algorithm:** **Logistic Regression** with balanced weighting ($C = 3.0$).
- **Feature Extraction:** Sublinear TF-IDF Vectorizer ($1$ to $3$ $n$-grams, $12,000$ max features).
- **Domain-Specific Preprocessing:** **Subject-Line Weight Boosting**.
  - In phishing, the subject line contains $2-3\times$ higher scam intent density than the body (e.g., *"ACTION REQUIRED: Account Termination Notice"*).
  - ScamShield concatenates: `f"{subject} {subject} {body}"`, giving double mathematical frequency to subject tokens naturally in TF-IDF.
- **Dataset:** $40,000$ balanced samples drawn from Enron, Nazario, CEAS, and Nigerian Fraud datasets.
- **Test Set Size:** $8,000$ samples (stratified split).
- **Performance Metrics:**
  - **Accuracy:** **$98.22\%$**
  - **Precision:** **$97.89\%$**
  - **Recall:** **$98.58\%$** ($3,943$ out of $4,000$ phishing emails caught!)
  - **F1-Score:** **$98.23\%$**
  - **ROC-AUC:** **$0.9979$**
- **Confusion Matrix ($N = 8,000$):**
  - $\text{True Negatives} = 3,915$, $\text{False Positives} = 85$
  - $\text{False Negatives} = 57$, $\text{True Positives} = 3,943$

---

### Model C: Malicious & Phishing URL Classifier
- **Algorithm:** **Random Forest Classifier** ($100$ estimators, `max_depth=15`, `min_samples_split=5`).
- **Zero-Network Philosophy:** The model inspects the URL **strictly client/server-side without visiting the website**, preventing drive-by malware infections or tracking beacon execution.
- **Feature Space:** **22 Handcrafted Lexical, Domain & Structural Features**:
  1. `url_length`: Total character length.
  2. `hostname_length`: Length of host.
  3. `path_length` & `query_length`: Subpath and parameter lengths.
  4. Character counts: `count_dots`, `count_hyphens`, `count_at` (`@` credential injection), `count_question`, `count_equal`, `count_slash`, `count_digits`, `count_special_chars`.
  5. `subdomain_count`: Number of nested subdomain levels (e.g. `paypal.com.verify-login.xyz` has 2 subdomains).
  6. `has_https`: Boolean indicator ($1/0$).
  7. `has_ip_address`: Direct IPv4 host detector.
  8. `is_shortened`: Known shortener detector (`bit.ly`, `tinyurl`, `t.co`, etc.).
  9. `suspicious_keyword_count`: Frequency of credential lures (`login`, `verify`, `bank`, `update`, `kyc`, `otp`, `claim`, `bonus`).
  10. **`entropy` (Shannon Entropy):** Measures character randomness to catch auto-generated DGA phishing domains.
  11. **`has_high_risk_tld`:** Detects abused free/cheap extensions (`.xyz`, `.top`, `.buzz`, `.cfd`, `.rest`, `.tk`, `.icu`).
  12. **`host_hyphen_count`:** Frequency of hyphens in hostname (e.g. `sbi-yono-portal-update`).
  13. **`brand_keyword_count`:** Targeted Indian banking and payment brand lures (`sbi`, `yono`, `hdfc`, `paytm`, `phonepe`, `gpay`, `mahadiscom`).
  14. **`digit_ratio_host`:** Ratio of numeric digits to letters in hostname.
- **Top Feature Importances (Gini Index):**
  - `has_https`: $65.41\%$
  - `subdomain_count`: $9.65\%$
  - `count_dots`: $3.83\%$
  - `count_special_chars`: $3.76\%$
  - `count_slash`: $2.76\%$
- **Dataset:** $40,000$ balanced samples drawn from $632,508$ URLs.
- **Performance Metrics:**
  - **Accuracy:** **$99.05\%$**
  - **Precision:** **$99.90\%$** (Only 4 false alarms out of 4,000 safe URLs!)
  - **Recall:** **$98.20\%$**
  - **F1-Score:** **$99.04\%$**
  - **ROC-AUC:** **$0.9984$**

---

## 4. Overall Model Performance Comparison Table

| Module | Algorithm | Features | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **SMS Message** | Word+Char TF-IDF + Logistic Reg ($C=5.0$) | $14,000$ n-grams | **99.19%** | **99.30%** | **94.63%** | **96.91%** | **0.9944** |
| **Email Phishing** | Subject-Boosted TF-IDF + Logistic Reg ($C=3.0$) | $12,000$ n-grams | **98.22%** | **97.89%** | **98.58%** | **98.23%** | **0.9979** |
| **URL / Links** | Random Forest ($100$ trees, depth $15$) | $22$ Lexical Feats | **99.05%** | **99.90%** | **98.20%** | **99.04%** | **0.9984** |

---

## 5. The Hybrid Risk Scoring Formula
Explain this clearly to the examiner:

$$\text{Risk Score} = \begin{cases} 
0.45 \cdot (P_{\text{Text}} \times 100) + 0.35 \cdot (P_{\text{URL}} \times 100) + 0.20 \cdot S_{\text{Rule}} & \text{if embedded link is present} \\
0.60 \cdot (P_{\text{Text}} \times 100) + 0.40 \cdot S_{\text{Rule}} & \text{if text only (SMS or Email)} \\
0.70 \cdot (P_{\text{URL}} \times 100) + 0.30 \cdot S_{\text{Rule}} & \text{if standalone URL input}
\end{cases}$$

- $P_{\text{Text}} \in [0, 1]$: Prediction probability from the SMS or Email model.
- $P_{\text{URL}} \in [0, 1]$: Prediction probability from the Random Forest URL model.
- $S_{\text{Rule}} \in [0, 100]$: Cumulative heuristic threat penalty (e.g. Sender mismatch $+35$, Raw IP $+40$, Shortener $+25$, Urgent Electricity cut threat $+50$).

### Risk Tiers:
- **Low Risk ($0 - 39$):** Safe, official, or low-probability messaging.
- **Medium Risk ($40 - 69$):** Cautionary warning; suspicious elements detected.
- **High Risk ($70 - 100$):** Active scam/phishing threat; explicit actionable defense instructions shown.

---

## 6. Top 12 Viva Questions & Answers (Cheat Sheet)

### Q1: Why is Recall prioritized over Precision in scam detection?
> **Answer:** In fraud detection, a **False Negative** means a victim receives a scam message, believes it, clicks the link, and loses their life savings. A **False Positive** merely means a user is shown a cautionary tip for a safe message. Therefore, catching scams (High Recall) is vital to user protection. Our SMS recall is $94.63\%$ and Email recall is $98.58\%$.

### Q2: What is data leakage and how did you prevent it?
> **Answer:** Data leakage occurs when test information influences the training process (e.g., fitting vectorizers or scalers on the entire dataset before splitting). We prevented this by:
> 1. Splitting data into $80\%$ Train and $20\%$ Test using `train_test_split` with stratification.
> 2. Calling `fit_transform()` strictly on `X_train`, and only `transform()` on `X_test`.

### Q3: If a scammer uses a valid HTTPS link, how does your URL model catch it?
> **Answer:** Historically, models relied heavily on `has_https`. To prevent evasion on modern HTTPS phishing sites, our model includes:
> 1. **Shannon Entropy:** Detects pseudo-random domain names.
> 2. **High-Risk TLD Detection:** Identifies abused extensions like `.xyz`, `.top`, `.buzz`.
> 3. **Brand Typosquatting Keywords:** Scans for deceptive brand names inside the domain (e.g., `sbi-yono-update.pages.dev`).
> 4. **Subdomain Stacking:** Counts deceptive subdomain levels.

### Q4: How does your model handle code-mixed language like Hinglish or Marathi?
> **Answer:** Pure word-level tokenization drops words that aren't in a dictionary. We implemented a **`FeatureUnion` of Word and Character-boundary n-grams (`char_wb`, $3-5$ characters)**. Even if an attacker spells `"paise bhej"` or `"bill bharave"`, subword fragments match fraud patterns regardless of spelling variations or transliteration.

### Q5: Why did you use TF-IDF instead of simple CountVectorizer (Bag of Words)?
> **Answer:** CountVectorizer only counts word frequency, meaning common words (`the`, `is`, `to`) dominate. **TF-IDF (Term Frequency – Inverse Document Frequency)** penalizes ubiquitous words and boosts terms that are rare across documents but frequent in scam messages (e.g., `disconnection`, `KYC`, `suspended`, `bonus`). We also enabled `sublinear_tf=True` ($1 + \log(\text{tf})$) to prevent long messages from disproportionately dominating feature weights.

### Q6: What does the hyperparameter $C$ do in Logistic Regression?
> **Answer:** $C$ is the inverse of regularization strength ($C = \frac{1}{\lambda}$). A smaller $C$ applies heavy regularization, forcing feature weights closer to zero (preventing overfitting). A larger $C$ allows the model to fit data more closely. We tuned $C=5.0$ for SMS and $C=3.0$ for Email to balance high recall with strong generalization.

### Q7: What is Shannon Entropy and how does it help detect malicious URLs?
> **Answer:** Shannon entropy measures information uncertainty and character randomness:
> $$H(S) = -\sum_{i=1}^n P(c_i) \log_2 P(c_i)$$
> Legitimate domains like `google.com` or `apple.com` have low entropy ($1.5 - 2.5$). Auto-generated phishing domains created by Domain Generation Algorithms (DGA), like `x7k9-p4zm1.com`, have high entropy ($>3.8$).

### Q8: Why did you set `max_depth=15` in Random Forest?
> **Answer:** Without setting `max_depth`, decision trees expand until all leaves are pure, leading to severe overfitting and gigantic model file sizes. Capping `max_depth=15` with `min_samples_split=5` ensures the model learns robust generalized rules, runs inference in $<5\text{ms}$, and keeps binary size compact ($\sim 3\text{MB}$).

### Q9: How do you handle class imbalance in the SMS dataset?
> **Answer:** In the raw SMS dataset, only $13.4\%$ are spam and $86.6\%$ are ham. If untreated, a naive model would predict "Safe" for everything and achieve $86.6\%$ accuracy. We addressed this using **`class_weight='balanced'`**, which automatically multiplies the loss function penalty for minority scam samples inversely proportional to class frequencies.

### Q10: Why do you avoid making live network requests during URL analysis?
> **Answer:** 
> 1. **User Safety:** Opening a malicious link or resolving its DNS can trigger drive-by malware downloads or notify the attacker that the target email/number is active.
> 2. **Latency:** DNS lookups and HTTP handshakes take $1000 - 3000\text{ms}$; our lexical feature extraction takes $<2\text{ms}$.
> 3. **Privacy:** The user's browsing activity is never exposed to third-party tracking.

### Q11: What is the purpose of the OCR module and how does it integrate with ML?
> **Answer:** Senior citizens and shopkeepers often receive scams via WhatsApp or phone screenshot rather than raw text. We use **Tesseract OCR** with OpenCV adaptive thresholding and grayscale conversion. The extracted text is then classified into SMS or URL content and forwarded to the appropriate ML predictor automatically.

### Q12: How is client privacy protected before machine learning inference?
> **Answer:** ScamShield includes a **Privacy Redaction Engine** that scrubs Indian PII (Aadhaar 12-digit numbers, PAN 10-character alphanumeric IDs, UPI VPA handles, and credit card numbers) using regular expressions before saving logs or sending text to inference routines.

---

## 7. Key File Locations in Codebase

| Component | File Path |
| :--- | :--- |
| **SMS Training Script** | [`ml/train_sms_model.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/train_sms_model.py) |
| **Email Training Script** | [`ml/train_email_model.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/train_email_model.py) |
| **URL Training Script** | [`ml/train_url_model.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/train_url_model.py) |
| **URL Feature Extraction** | [`ml/feature_extraction.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/feature_extraction.py) |
| **Prediction Engine** | [`ml/prediction.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/prediction.py) |
| **Hybrid Risk Engine** | [`risk/risk_engine.py`](file:///c:/Users/anike/Downloads/ScamShield/risk/risk_engine.py) |
| **Evaluation Aggregator** | [`ml/evaluate_models.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/evaluate_models.py) |
| **Comprehensive ML Doc** | [`docs/ML_DOCUMENTATION.md`](file:///c:/Users/anike/Downloads/ScamShield/docs/ML_DOCUMENTATION.md) |
