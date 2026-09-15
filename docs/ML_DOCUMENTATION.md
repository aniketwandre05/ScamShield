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
- **Algorithm**: Multinomial / Binomial Logistic Regression with Balanced Class Weights.
- **Vectorization**: TF-IDF (Term Frequency - Inverse Document Frequency) with Unigram + Bigram ($n \in \{1, 2\}$) extraction.
- **Vocabulary Size**: 5,000 top sublinear features.
- **Preprocessing**: Lowercase conversion, HTML entity decoding, tag removal, whitespace compaction.

#### B. Phishing Email Classification Model
- **Algorithm**: Logistic Regression with Balanced Weights ($C=2.0$).
- **Vectorization**: TF-IDF Vectorizer (1–2 ngrams, 10,000 max features, sublinear term frequency scaling).
- **Preprocessing**: Concatenation of Subject and Body text, sender domain mismatch inspection.

#### C. URL Malicious / Scam Link Classification Model
- **Algorithm**: Random Forest Classifier (100 decision trees, max depth 15, minimum samples split 5).
- **Feature Space (17 Handcrafted Lexical & Structural Features)**:
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

---

### 3. Feature Importance (Top URL Features)

According to the Random Forest Gini importance analysis:
1. `has_https` (**68.72%**): Absence of HTTPS strongly correlates with malicious/phishing links.
2. `subdomain_count` (**11.57%**): Phishing pages heavily utilize deceptive subdomains (e.g. `paypal.com.account-verify.xyz`).
3. `count_special_chars` (**3.70%**): Obfuscated characters and encoding.
4. `count_dots` (**3.31%**): Deeply nested paths and IP formatting.
5. `count_slash` (**2.87%**): Unusually long file directories.

---

### 4. Evaluation Metrics & Confusion Matrices

All models were evaluated on independent, held-out test splits (20% test size, stratified sampling).

#### Summary Metrics Table

| Model Name | Test Size | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SMS Classifier** | 1,115 | **98.90%** | **94.35%** | **96.69%** | **95.51%** | **0.9964** |
| **Email Classifier** | 8,000 | **98.55%** | **98.28%** | **98.94%** | **98.61%** | **0.9986** |
| **URL Classifier** | 8,000 | **98.80%** | **99.59%** | **97.96%** | **98.77%** | **0.9977** |

#### Confusion Matrices

**SMS Classifier Confusion Matrix ($N=1,115$):**
$$\begin{pmatrix} \text{True Negative (Safe)} = 961 & \text{False Positive} = 5 \\ \text{False Negative} = 11 & \text{True Positive (Scam)} = 138 \end{pmatrix}$$

**Email Classifier Confusion Matrix ($N=8,000$):**
$$\begin{pmatrix} \text{True Negative (Safe)} = 3921 & \text{False Positive} = 79 \\ \text{False Negative} = 48 & \text{True Positive (Phishing)} = 3952 \end{pmatrix}$$

**URL Classifier Confusion Matrix ($N=8,000$):**
$$\begin{pmatrix} \text{True Negative (Benign)} = 3993 & \text{False Positive} = 7 \\ \text{False Negative} = 79 & \text{True Positive (Malicious)} = 3921 \end{pmatrix}$$

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
