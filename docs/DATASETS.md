# Dataset Documentation
## SCAMSHIELD: Data Sources, Distribution, & Preprocessing

---

### 1. Overview of Datasets
ScamShield relies on three benchmark datasets representing distinct vectors of modern cyber fraud. All raw files are stored under `data/raw/`.

---

### 2. Dataset Specifics

#### A. SMS Spam Collection Dataset
- **File**: `data/raw/sms_spam.csv`
- **Total Samples**: 5,572 records
- **Class Distribution**:
  - `Ham (Safe)`: 4,825 messages (86.6%)
  - `Spam / Scam`: 747 messages (13.4%)
- **Attributes**: `v1` (Label: ham/spam), `v2` (Message text)
- **Source**: UCI Machine Learning Repository / Kaggle SMS Spam Collection.

#### B. Phishing Email Dataset
- **File**: `data/raw/email_phishing.csv`
- **Total Samples in Raw**: 82,486 records
- **Training Subset Sampled**: 40,000 balanced records (20,000 safe, 20,000 phishing)
- **Class Distribution**:
  - `0 (Safe Email)`: 50.0%
  - `1 (Phishing / Scam Email)`: 50.0%
- **Attributes**: `text_combined` (Cleaned email body and subject), `label` (Binary target).

#### C. Malicious and Benign URLs Dataset
- **File**: `data/raw/url_dataset.csv`
- **Total Samples in Raw**: 632,508 records
- **Training Subset Sampled**: 40,000 balanced records (20,000 benign, 20,000 malicious)
- **Class Distribution**:
  - `0 (Benign URL)`: 50.0%
  - `1 (Malicious / Phishing URL)`: 50.0%
- **Attributes**: `url` (Raw URL string), `result` (0=Benign, 1=Malicious).

---

### 3. Data Preprocessing & Cleaning Protocols

1. **Text Normalization**:
   - Decoding HTML entities (`&amp;` $\to$ `&`, `&lt;` $\to$ `<`).
   - Regular expression removal of HTML formatting tags (`<[^>]+>`).
   - Normalization of irregular line breaks and whitespace.
   - Case folding to lowercase.

2. **URL Extraction**:
   - Regular expression scanning (`(?:https?://|www\.)[a-zA-Z0-9.\-_~:/?#[\]@!$&'()*+,;=%]+`) to identify embedded links inside message text without breaking sentence semantics.

3. **URL Lexical Transformation**:
   - Extraction of 17 discrete numerical and boolean features (`url_length`, `subdomain_count`, `has_ip_address`, `has_https`, `is_shortened`, etc.) without initiating network requests.
