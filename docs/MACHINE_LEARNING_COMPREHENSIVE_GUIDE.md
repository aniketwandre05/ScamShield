# SCAMSHIELD: Comprehensive Machine Learning Architecture, Theory & Implementation Guide

---

## Executive Overview: The Philosophy of ScamShield's AI
ScamShield is an AI-driven cybersecurity system built to detect fraud, social engineering attacks, and phishing links across three distinct digital vectors: **SMS/WhatsApp messages**, **Emails**, and **URLs/Hyperlinks**.

Most commercial tools treat fraud detection as a generic text-classification problem or rely exclusively on static blacklists (such as Google Safe Browsing). ScamShield's core premise is that **different attack vectors possess fundamentally different mathematical structures and threat dynamics**. Therefore, ScamShield implements a **Multi-Model, Hybrid Machine Learning Architecture** combining:
1. **Supervised Natural Language Processing (NLP)** with subword feature unions for short-text messages.
2. **Structural Document & Intent Modeling** with subject-line boosting for emails.
3. **Lexical & Information-Theoretic Structural Modeling** (22 handcrafted features) for URLs without making network requests.
4. **Deterministic Heuristic Threat Rules** that enforce zero-tolerance cybersecurity constraints.
5. **Calibrated Late-Stage Fusion** to produce an interpretable Estimated Risk Score ($0 - 100$).

---

## 1. Problem Formulation: How the ML Task Was Defined

### A. The Formal Machine Learning Problem
For any given user input $x$ (text string, email object, or URL), the machine learning task is formulated as **Supervised Binary Classification**:
$$\hat{y} = f(x; \theta) \in [0, 1]$$
Where:
- $\hat{y}$ is the continuous calibrated probability that input $x$ is malicious/fraudulent ($1 = \text{Scam/Phishing/Malicious}$, $0 = \text{Benign/Safe}$).
- $\theta$ represents the learned model parameters (weights in Logistic Regression, decision thresholds across trees in Random Forest).

### B. The Tri-Modal Decomposition: Why Not a Single Model?
When designing ScamShield, the first engineering question was:  
*Can one model classify SMS, Emails, and URLs simultaneously?*

| Threat Vector | Syntactic Nature | Information Density | Noise & Obfuscation | Failure Mode of a Single Model |
| :--- | :--- | :--- | :--- | :--- |
| **SMS / WhatsApp** | Terse ($<160$ chars), colloquial, unpunctuated. | Very high; concentrated emotional triggers (fear, greed). | Leetspeak, typos, phonetic Hinglish/Marathi transliteration. | A general model treats Hinglish/typos as out-of-vocabulary noise. |
| **Email** | Long-form ($500 - 5000$ chars), structured. | Sparse; scam intent concentrated in subject line and call-to-action button. | Clean formal English, business jargon, spoofed header names. | Long benign conversational text dilutes the few urgent scam keywords. |
| **URL / Link** | Non-natural language syntactic string (RFC 3986). | Purely structural; path depth, entropy, domain delimiters. | Homoglyphs, subdomains, URL shorteners, raw IP addresses. | Natural language tokenizers split URLs into meaningless sub-tokens or crash. |

**The Decision:** Decompose the input space into three dedicated, highly optimized domain pipelines.

---

## 2. Mathematical Foundations of the Algorithms Used

### Algorithm 1: Logistic Regression with Regularization (SMS & Email)

#### The Hypothesis Function:
Linear regression outputs values in $(-\infty, +\infty)$, which cannot represent probabilities. Logistic Regression maps linear combinations of features into valid probabilities $[0, 1]$ using the **Sigmoid (Logistic) Function**:
$$z = w^T x + b = \sum_{j=1}^d w_j x_j + b$$
$$P(y = 1 | x) = \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{1}{1 + e^{-(w^T x + b)}}$$

#### Why Logistic Regression for Text Classification?
1. **Convex Optimization:** The loss surface of Logistic Regression is strictly convex, guaranteeing convergence to the global optimum without getting trapped in local minima.
2. **High-Dimensional Sparsity:** Text represented by TF-IDF has thousands of dimensions ($d = 7,000 - 14,000$), but most inputs contain only $20 - 50$ active words (sparse vector). Linear decision boundaries are computationally optimal and mathematically sound in such high dimensions (Vapnik-Chervonenkis dimension theory).
3. **Calibrated Probabilities:** Unlike Support Vector Machines (SVMs) which output uncalibrated geometric margins, Logistic Regression directly outputs log-odds, making its output suitable for risk fusion formulas.
4. **Log-Odds Interpretability:** The weight $w_j$ represents the increase in log-odds of a scam for word $j$:
   $$\ln\left(\frac{P}{1 - P}\right) = w^T x + b$$
   If word $j$ (`disconnection`) has a large positive weight $w_j$, its presence directly increases scam probability.

#### Loss Function & $L_2$ Regularization:
To train the weights $w$, the model minimizes the **Penalized Binary Cross-Entropy (Log-Loss)**:
$$\mathcal{L}(w) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(\hat{y}_i) + (1 - y_i) \ln(1 - \hat{y}_i) \right] + \frac{1}{2C} \|w\|_2^2$$
Where:
- $y_i \in \{0, 1\}$ is the ground truth.
- $\hat{y}_i = \sigma(w^T x_i + b)$ is the model prediction.
- $\|w\|_2^2 = \sum_{j=1}^d w_j^2$ is the $L_2$ Ridge penalty that prevents any single word weight from exploding.
- $C = \frac{1}{\lambda}$ is the inverse regularization strength:
  - Small $C$ $\implies$ heavy regularization (simpler model, prevents overfitting).
  - Large $C$ $\implies$ weak regularization (allows model to fit training features closely).
  - **In ScamShield:** We tuned $C=5.0$ for SMS and $C=3.0$ for Email to balance high recall with strong generalization.

---

### Algorithm 2: Random Forest Classifier (URLs)

#### What is an Ensemble of Decision Trees?
A single Decision Tree splits features using threshold inequalities (e.g., `has_https <= 0.5`, `subdomain_count > 2`). However, single trees have high variance and overfit rapidly.  
A **Random Forest** is an ensemble method combining **Bagging (Bootstrap Aggregating)** and **Random Feature Subspace Selection**:
1. It trains $B = 100$ independent decision trees.
2. Each tree is trained on a distinct bootstrap sample (random sample with replacement) of the training data.
3. At each split within a tree, only a random subset of features $m = \sqrt{D} \approx \sqrt{22} \approx 4-5$ features is evaluated.
4. The ensemble probability is the average of predictions across all $100$ trees:
   $$\hat{P}(y = 1 | x) = \frac{1}{B} \sum_{b=1}^B T_b(x)$$

#### Splitting Criterion: Gini Impurity
At each node, the Random Forest selects the feature and threshold that maximizes the reduction in **Gini Impurity**:
$$I_G(p) = 1 - \sum_{k=0}^1 p_k^2 = 1 - (p_{\text{safe}}^2 + p_{\text{scam}}^2)$$
Where $p_k$ is the proportion of samples belonging to class $k$ at that node.
- A pure node ($100\%$ safe or $100\%$ scam) has $I_G = 0$.
- An evenly split node ($50\%$ safe, $50\%$ scam) has maximum impurity $I_G = 0.5$.

#### Why Random Forest for URLs?
1. **Non-Linear Interactions:** URL features have complex logical relationships (e.g., *a high subdomain count is benign on `google.com`, but malicious when combined with an unknown TLD and no HTTPS*). Trees model non-linear interactions naturally without requiring manual polynomial feature engineering.
2. **Mixed Feature Scales:** URL features include binary flags ($0$ or $1$ for `has_https`), integer counts ($0$ to $50$ for `url_length`), and continuous floats ($0.0$ to $4.5$ for `entropy`). Decision trees are invariant to monotonic feature scaling, eliminating the need for normalization.
3. **Overfitting Control via Hyperparameters:**
   - `n_estimators=100`: High enough for variance reduction; low enough for $<5\text{ms}$ inference.
   - `max_depth=15`: Stops tree growth before memorizing individual URLs.
   - `min_samples_split=5`: Prevents splitting on statistical noise.

---

## 3. Deep Dive into Feature Engineering: What Was Built & Why

Feature engineering is the process of transforming raw inputs into mathematical vectors that maximize the classifier's predictive power.

### A. SMS Feature Pipeline: The Subword `FeatureUnion`

#### The Problem:
Standard NLP tokenizes text on whitespace and punctuation. In real-world scams in India:
- Scammers write in Romanized Marathi/Hindi: *"Priy grahak aple MSEDCL light bill update kara nahi tar ratri bij purwatha khandit honar."*
- Scammers introduce deliberate typos to bypass filters: `p@ypal`, `k-y-c`, `urgnt`, `cl1ck`.
- Word-level vectorizers drop these words as unknown/out-of-vocabulary.

#### The Solution: Dual-Channel `FeatureUnion`
ScamShield combines two distinct vectorizers operating in parallel:
```
                      Raw Cleaned Text
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   Channel 1: Word TF-IDF            Channel 2: Char-WB TF-IDF
  • n-grams: (1, 2, 3)              • n-grams: (3, 4, 5)
  • max_features: 7,000             • max_features: 7,000
  • sublinear_tf: True              • analyzer: 'char_wb'
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                 Concatenated Feature Space
                   (14,000 Sparse Features)
```

1. **Word-Level Channel:** Evaluates semantic meaning across unigrams, bigrams, and trigrams:
   - `account` (unigram)
   - `account suspended` (bigram)
   - `immediate payment required` (trigram)
2. **Character-WB Channel (`char_wb`):** Evaluates character substrings within word boundaries.
   - For the word `urgnt`, character 4-grams extract: `_urg`, `urgn`, `rgnt`, `gnt_`.
   - Even if the full word is misspelled, the subword chunks match the root scam pattern.
   - For regional words (`paise`, `bhejo`), subword roots are captured automatically.

#### Mathematical TF-IDF Formula with Sublinear Scaling:
$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$
Where:
$$\text{Sublinear TF}(t, d) = 1 + \ln(\text{count}(t, d)) \quad \text{if count} > 0 \text{ else } 0$$
$$\text{IDF}(t) = \ln\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$
- $N$ is the total number of documents.
- $\text{DF}(t)$ is the document frequency (number of documents containing term $t$).
- *Why Sublinear TF?* A message mentioning `"urgent"` 10 times is not 10 times more threatening than a message mentioning it twice. Logarithmic scaling dampens excessive term frequency.

---

### B. Email Feature Pipeline: Subject-Line Weight Boosting

#### The Empirical Finding:
In enterprise phishing and consumer email attacks, the email body is frequently cloned directly from legitimate corporate templates (clean privacy footers, legitimate logos, standard formatting). The malicious payload exists in:
1. The **Subject line** (creates urgency, panic, or false authority).
2. The **Call-to-Action link/button**.

#### The Implementation:
During preprocessing in [`ml/train_email_model.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/train_email_model.py) and [`ml/prediction.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/prediction.py):
```python
if subject:
    combined_text = f"{subject} {subject} {body}".strip()
else:
    combined_text = body.strip()
```
- **Why this works:** Repeating the subject line doubles the raw term frequency of subject words prior to TF-IDF transformation. Terms like `"Notice"`, `"Suspension"`, and `"Unauthorized Access"` in the subject line naturally achieve twice the weighting in the resulting vector, preventing benign conversational email bodies from diluting the scam signal.

---

### C. URL Feature Pipeline: 22 Handcrafted Features

Because ScamShield avoids making network calls, it relies on static structural analysis. The 22 features extracted in [`ml/feature_extraction.py`](file:///c:/Users/anike/Downloads/ScamShield/ml/feature_extraction.py) are:

| Feature Name | Type | Mathematical / Logical Definition | Threat Rationale |
| :--- | :--- | :--- | :--- |
| `url_length` | Integer | $\text{len}(url)$ | Malicious URLs are often elongated to hide destination domains or pass exploit payloads. |
| `hostname_length` | Integer | $\text{len}(hostname)$ | Hostnames $>30$ characters often indicate dynamic DNS or domain stacking. |
| `path_length` | Integer | $\text{len}(path)$ | Deep nested subdirectories are used to mimic legitimate website hierarchy. |
| `query_length` | Integer | $\text{len}(query)$ | Long query strings often carry tracking tokens, redirect targets, or victim identifiers. |
| `count_dots` | Integer | Frequency of `.` | Excessive dots indicate multiple subdomains or IP address obfuscation. |
| `count_hyphens` | Integer | Frequency of `-` | Legitimate brands rarely use hyphens; phishing domains chain hyphens (`sbi-yono-update`). |
| `count_at` | Integer | Frequency of `@` | RFC 3986 treats text before `@` as user credentials; everything after is the real destination. Used for URL spoofing. |
| `count_question` | Integer | Frequency of `?` | Parameter delimiter. |
| `count_equal` | Integer | Frequency of `=` | Parameter assignments. |
| `count_slash` | Integer | Frequency of `/` | File separator frequency. |
| `count_digits` | Integer | Total numeric characters in URL | Scammers use numeric identifiers, timestamps, or raw IP fragments. |
| `count_special_chars`| Integer | Non-alphanumeric character count | Obfuscation, hex encoding (`%20`), or symbol stacking. |
| `subdomain_count` | Integer | $\max(0, \text{len}(parts) - 2)$ | Deceptive subdomain stacking (e.g., `paypal.com.account-verify.xyz` has 2 subdomains). |
| `has_https` | Boolean | $1$ if scheme is `https://`, else $0$ | Absence of encryption is strongly correlated with amateur fraud sites. |
| `has_ip_address` | Boolean | Regex match for IPv4 structure | Direct IP addresses (e.g. `http://192.168.1.1/login`) bypass domain name registration checks. |
| `is_shortened` | Boolean | Matches known shortener domains (`bit.ly`, `tinyurl`) | URL shorteners conceal the true destination domain from user inspection. |
| `suspicious_keyword_count`| Integer | Frequency of credential keywords (`login`, `verify`, `bank`, `kyc`, `otp`) | Detects credential-harvesting intent in URL paths. |
| **`entropy`** | Float | **Shannon Entropy of hostname** | Measures character randomness. Auto-generated DGA domains have high entropy ($>3.8$). |
| **`has_high_risk_tld`** | Boolean | Checks if domain ends with high-risk TLDs (`.xyz`, `.top`, `.buzz`, `.cfd`, `.tk`) | Free and ultra-cheap TLDs are predominantly registered by malicious actors. |
| **`host_hyphen_count`** | Integer | Frequency of `-` specifically within hostname | Hostname hyphens distinguish domain spoofing from path hyphens. |
| **`brand_keyword_count`** | Integer | Frequency of Indian brands in hostname (`sbi`, `yono`, `paytm`, `phonepe`, `mahadiscom`) | Catches targeted brand typosquatting. |
| **`digit_ratio_host`** | Float | $\frac{\text{digits in host}}{\text{len}(host) + 10^{-5}}$ | Scammers introduce digits into subdomains to generate unique victim links. |

#### Shannon Entropy Deep Dive:
Claude Shannon’s information entropy measures the unpredictability of characters in a string $S$:
$$H(S) = -\sum_{i=1}^k P(c_i) \log_2 P(c_i)$$
Where $P(c_i)$ is the empirical probability of character $c_i$ appearing in $S$.
- English words in brand names have redundant letter patterns $\implies$ Low Entropy ($1.5 - 2.8$).
- Phishing domains generated by algorithms (e.g., `q7x9-v2zp1.xyz`) have high randomness $\implies$ High Entropy ($>3.8$).

---

## 4. Addressing Real-World Challenges in Cybersecurity ML

### Challenge 1: Severe Class Imbalance
In the real world and in benchmark datasets, benign messages vastly outnumber scam messages (in SMS, only $13.4\%$ are scams).
- **The Risk:** A model trained on unbalanced data achieves $86.6\%$ accuracy simply by predicting "Safe" $100\%$ of the time, missing every single scam (Recall $= 0\%$).
- **ScamShield's Solution:** **Cost-Sensitive Learning (`class_weight='balanced'`)**.
  During Logistic Regression training, the loss function assigns weights inversely proportional to class frequencies:
  $$w_c = \frac{N}{2 \times N_c}$$
  Where $N$ is total samples and $N_c$ is samples in class $c$. This penalizes the model far more heavily when it misclassifies a rare scam sample than when it misclassifies a common safe sample.

### Challenge 2: The Recall vs. Precision Asymmetry
In academic benchmarks, developers often optimize for overall Accuracy. In cybersecurity, this is a dangerous error:
- **False Positive (FP):** The model flags a safe family message or utility receipt as suspicious.
  - *Consequence:* The user sees a caution warning, verifies the sender, and experiences minor friction.
- **False Negative (FN):** The model fails to flag an active bank phishing link or electricity cut scam.
  - *Consequence:* The user clicks the link, enters their credentials, and suffers catastrophic financial theft.
- **ScamShield's Decision:** **Prioritize Recall ($>94\%$) while keeping Precision above $97\%$**.

### Challenge 3: Evasion via Modern HTTPS Certificates
Historically, phishing models gave $>68\%$ importance to whether a site had HTTPS. In 2024–2026, free certificate authorities (Let's Encrypt) mean over $80\%$ of phishing sites now use valid HTTPS.
- **ScamShield's Solution:** Reduced reliance on `has_https` by introducing hostname entropy, brand keyword lure scanning, and high-risk TLD tracking, ensuring HTTPS-enabled phishing links are caught effectively.

---

## 5. The Hybrid Risk Calibration Engine: Blending ML with Rules

Machine learning models produce continuous probabilities based on historical correlations. However, cybersecurity requires strict deterministic boundaries. ScamShield couples the ML models with a **Heuristic Rule Engine** ([`risk/risk_engine.py`](file:///c:/Users/anike/Downloads/ScamShield/risk/risk_engine.py)).

### The Scoring Equation:
$$\text{Risk Score} = \begin{cases} 
0.45 \cdot (P_{\text{Text}} \times 100) + 0.35 \cdot (P_{\text{URL}} \times 100) + 0.20 \cdot S_{\text{Rule}} & \text{if embedded URL is present} \\
0.60 \cdot (P_{\text{Text}} \times 100) + 0.40 \cdot S_{\text{Rule}} & \text{if text only (SMS or Email)} \\
0.70 \cdot (P_{\text{URL}} \times 100) + 0.30 \cdot S_{\text{Rule}} & \text{if standalone URL}
\end{cases}$$

### Why This Calibration Works:
1. **Compounding Threat Multipliers:** If an SMS has a moderate text score ($P_{\text{Text}} = 0.55$) but contains a verified high-risk URL ($P_{\text{URL}} = 0.95$), the embedded link pulls the overall risk into the **High Risk** zone ($>70$).
2. **Deterministic Overrides:** If a message contains zero-day text that confuses the NLP model, but contains a raw IPv4 link or a `.apk` download link, the Heuristic Rule score $S_{\text{Rule}}$ adds an immediate $+40$ to $+50$ penalty, ensuring the user is alerted.
3. **Verified Safe Whitelist Dampening:** If the domain is verified official (`google.com`, `apple.com`, `onlinesbi.sbi`), the engine dampens false positive risks to ensure trusted receipts aren't blocked.

---

## 6. Complete Empirical Evaluation Matrix

All models were evaluated on independent, held-out test splits ($20\%$ test size, stratified sampling).

| Module | Algorithm | Features | Test Samples | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SMS Message** | Word+Char TF-IDF + Logistic Reg ($C=5.0$) | $14,000$ | $1,115$ | **99.19%** | **99.30%** | **94.63%** | **96.91%** | **0.9944** |
| **Email Phishing** | Subject-Boosted TF-IDF + Logistic Reg ($C=3.0$) | $12,000$ | $8,000$ | **98.22%** | **97.89%** | **98.58%** | **98.23%** | **0.9979** |
| **URL / Links** | Random Forest ($100$ trees, depth $15$) | $22$ | $8,000$ | **99.05%** | **99.90%** | **98.20%** | **99.04%** | **0.9984** |

### Confusion Matrices:

#### SMS Classifier ($N = 1,115$):
$$\begin{pmatrix} \text{TN (Safe correctly identified)} = 965 & \text{FP (Safe falsely flagged)} = 1 \\ \text{FN (Scam missed)} = 8 & \text{TP (Scam caught)} = 141 \end{pmatrix}$$

#### Email Classifier ($N = 8,000$):
$$\begin{pmatrix} \text{TN} = 3915 & \text{FP} = 85 \\ \text{FN} = 57 & \text{TP} = 3943 \end{pmatrix}$$

#### URL Classifier ($N = 8,000$):
$$\begin{pmatrix} \text{TN} = 3996 & \text{FP} = 4 \\ \text{FN} = 72 & \text{TP} = 3928 \end{pmatrix}$$

---

## 7. Supporting AI & HCI Subsystems

1. **Multimodal OCR Ingestion ([`ocr/ocr_engine.py`](file:///c:/Users/anike/Downloads/ScamShield/ocr/ocr_engine.py)):**
   - Uses Tesseract OCR coupled with OpenCV adaptive thresholding and grayscale pre-processing to extract text from user screenshots.
   - Detects whether the screenshot contains an SMS thread or a URL bar and routes it to the corresponding ML pipeline automatically.
2. **Client-Side Privacy Redactor ([`risk/privacy.py`](file:///c:/Users/anike/Downloads/ScamShield/risk/privacy.py)):**
   - Masks sensitive Indian PII before inference or logging:
     - Aadhaar: `\b[2-9][0-9]{3}\s[0-9]{4}\s[0-9]{4}\b` $\implies$ `[REDACTED_AADHAAR]`
     - PAN: `\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b` $\implies$ `[REDACTED_PAN]`
     - UPI ID: `[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}` $\implies$ `[REDACTED_UPI]`
3. **Trilingual Explainable AI ([`translations.py`](file:///c:/Users/anike/Downloads/ScamShield/translations.py)):**
   - Instead of presenting users with technical metrics (e.g. *"Log-loss is 0.04"*), ScamShield translates feature triggers into plain language checklists in **English**, **Marathi (मराठी)**, and **Hindi (हिंदी)**, ensuring usability across Pune and Maharashtra demographics.

---

## 8. Summary Table of Key Hyperparameters & Architectural Choices

| Component | Technical Choice | Why This Was Chosen |
| :--- | :--- | :--- |
| **SMS Vectorizer** | `FeatureUnion(Word (1-3) + Char-WB (3-5))` | Solves out-of-vocabulary typos, leetspeak, and Hinglish/Marathi transliteration. |
| **SMS Regularization** | $C=5.0$, `class_weight='balanced'` | Compensates for the $13.4\%$ spam minority class; raises Recall to $94.63\%$. |
| **Email Preprocessing** | Subject-Line Weight Doubling | Amplifies high-threat intent in subject lines without diluting body text. |
| **Email Regularization** | $C=3.0$, `max_features=12000` | Optimal bias-variance tradeoff across $40,000$ training records. |
| **URL Algorithm** | Random Forest ($100$ trees, depth $15$) | Models non-linear interactions between $22$ lexical features without network calls. |
| **URL Entropy** | Shannon Entropy on Hostname | Identifies pseudo-random strings produced by Domain Generation Algorithms (DGA). |
| **Risk Calibrator** | Linear Weighted Late Fusion | Balances continuous ML probabilities with zero-tolerance deterministic security rules. |
| **Inference Target** | Local CPU ($<15\text{ms}$) | Low latency, zero GPU dependence, cost-effective deployment on small virtual servers. |
