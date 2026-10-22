# Machine Learning Methodology & Evaluation Report
## SCAMSHIELD: Hybrid Machine Learning Architecture

---

### 1. Architectural Philosophy
ScamShield rejects a single "black-box" model in favor of a **modular, hybrid machine-learning architecture**. Different vectors of social engineering possess distinct feature distributions:
- **SMS & WhatsApp messages** are short, high-density texts characterized by abbreviations and aggressive urgency.
- **Emails** possess structural metadata (headers, subject, sender domain) and longer conversational bodies.
- **URLs** are purely syntactic strings requiring lexical, domain, and structural character analysis before network traversal.

By deploying specialized models for text and URLs and combining them with heuristic rule evaluation, ScamShield ensures maximum interpretability, ultra-low latency, and reliable scam detection.

---

### 2. Specialized Models & Feature Engineering

#### A. SMS Scam Classification Model
- **Algorithm**: Multinomial / Binomial Logistic Regression with Balanced Class Weights ($C=5.0$).
- **Vectorization**: FeatureUnion combining:
  1. Word-level TF-IDF: Unigram, Bigram, and Trigram ($n \in \{1, 2, 3\}$), 7,000 sublinear features.
  2. Character-wb TF-IDF: Subword character boundaries ($n \in \{3, 4, 5\}$), 7,000 sublinear features to capture typos, leetspeak, and Hinglish/Marathi transliteration.
- **Preprocessing**: Lowercase conversion, HTML entity decoding, tag removal, whitespace compaction.

#### B. Phishing Email Classification Model
- **Algorithm**: Logistic Regression with Balanced Weights ($C=3.0$).
- **Vectorization**: TF-IDF Vectorizer ($1–3$ ngrams, 12,000 max features, sublinear term frequency scaling).
- **Preprocessing**: Subject-line weight boosting (double-weighted subject line to amplify high scam intent density) and body text normalization.

#### C. URL Malicious / Scam Link Classification Model
- **Algorithm**: Random Forest Classifier (100 decision trees, max depth 15, minimum samples split 5).
- **Feature Space (22 Handcrafted Lexical, Domain & Structural Features)**:
  1. `url_length`: Total character count.
  2. `hostname_length`: Hostname length.
  3. `path_length`: Length of path segment.
  4. `query_length`: Length of query parameters.
  5. `count_dots`: Frequency of `.` in URL.
  6. `count_hyphens`: Frequency of `-` in URL.
  7. `count_at`: Frequency of `@` (credential injection flag).
  8. `count_question`: Frequency of `?` parameters.
  9. `count_equal`: Frequency of `=` assignments.
  10. `count_slash`: Frequency of `/` directory separators.
  11. `count_digits`: Total digit count.
  12. `count_special_chars`: Total non-alphanumeric characters.
  13. `subdomain_count`: Number of nested subdomains.
  14. `has_https`: Boolean indicator (1 = HTTPS, 0 = HTTP).
  15. `has_ip_address`: Boolean indicator for raw IPv4 addresses.
  16. `is_shortened`: Boolean indicator for known shorteners (`bit.ly`, `tinyurl`, etc.).
  17. `suspicious_keyword_count`: Frequency of keywords (`login`, `verify`, `bank`, `update`, `kyc`, `otp`, `claim`, `bonus`).
  18. `entropy`: Shannon entropy measuring character randomness (detects DGA/auto-generated scam domains).
  19. `has_high_risk_tld`: Boolean flag for heavily abused free/cheap TLDs (`.xyz`, `.top`, `.buzz`, `.cfd`, `.rest`, `.tk`, `.icu`, etc.).
  20. `host_hyphen_count`: Frequency of hyphens in hostname (e.g. `sbi-yono-update`).
  21. `brand_keyword_count`: Frequency of targeted Indian financial/utility brand lures in hostname (`sbi`, `yono`, `paytm`, `phonepe`, `gpay`, `mahadiscom`, etc.).
  22. `digit_ratio_host`: Numerical ratio of digits to characters in hostname.

---

### 3. Feature Importance (Top URL Features)

According to the Random Forest Gini importance analysis:
1. `has_https` (**65.41%**): Absence of HTTPS strongly correlates with malicious/phishing links.
2. `subdomain_count` (**9.65%**): Phishing pages heavily utilize deceptive subdomains (e.g. `paypal.com.account-verify.xyz`).
3. `count_dots` (**3.83%**): Deeply nested paths and IP formatting.
4. `count_special_chars` (**3.76%**): Obfuscated characters and encoding.
5. `count_slash` (**2.76%**): Unusually long file directories.

---

### 4. Evaluation Metrics & Confusion Matrices

All models were evaluated on independent, held-out test splits (stratified sampling).

#### Summary Metrics Table

| Model Name | Test Size | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SMS Classifier** | 1,115 | **99.19%** | **99.30%** | **94.63%** | **96.91%** | **0.9944** |
| **Email Classifier** | 8,000 | **98.22%** | **97.89%** | **98.58%** | **98.23%** | **0.9979** |
| **URL Classifier** | 8,000 | **99.05%** | **99.90%** | **98.20%** | **99.04%** | **0.9984** |

#### Confusion Matrices

**SMS Classifier Confusion Matrix ($N=1,115$):**
$$\begin{pmatrix} \text{True Negative (Safe)} = 965 & \text{False Positive} = 1 \\ \text{False Negative} = 8 & \text{True Positive (Scam)} = 141 \end{pmatrix}$$

**Email Classifier Confusion Matrix ($N=8,000$):**
$$\begin{pmatrix} \text{True Negative (Safe)} = 3915 & \text{False Positive} = 85 \\ \text{False Negative} = 57 & \text{True Positive (Phishing)} = 3943 \end{pmatrix}$$

**URL Classifier Confusion Matrix ($N=8,000$):**
$$\begin{pmatrix} \text{True Negative (Benign)} = 3996 & \text{False Positive} = 4 \\ \text{False Negative} = 72 & \text{True Positive (Malicious)} = 3928 \end{pmatrix}$$

---

### 5. Hybrid Risk Calibration & Formula

To prevent false confidence from purely statistical probabilities or blind keyword triggers, the **Hybrid Risk Engine** computes:

$$\text{Risk Score} = \begin{cases} 
0.50 \cdot (P_{\text{Text}} \times 100) + 0.30 \cdot (P_{\text{URL}} \times 100) + 0.20 \cdot S_{\text{Rule}} & \text{if embedded URL is present} \\
0.60 \cdot (P_{\text{Text}} \times 100) + 0.40 \cdot S_{\text{Rule}} & \text{if text only} \\
0.75 \cdot (P_{\text{URL}} \times 100) + 0.25 \cdot S_{\text{Rule}} & \text{if standalone URL}
\end{cases}$$

Where:
- $P_{\text{Text}} \in [0, 1]$ is the specialized text model probability.
- $P_{\text{URL}} \in [0, 1]$ is the Random Forest link probability.
- $S_{\text{Rule}} \in [0, 100]$ is the cumulative heuristic threat score.
