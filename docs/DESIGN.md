# System Design Document & Architectural Diagrams
## SCAMSHIELD: AI-Based Scam Detection and Risk Assessment System

This document provides complete architectural specifications, module diagrams, and data flow representations for ScamShield, including **14 comprehensive Mermaid diagrams** accurately reflecting the real codebase.

---

### Diagram 1: Overall System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer (HTML5 / CSS3 / Vanilla JS)"
        UI_Home["Home Page (4 Large Check Options)"]
        UI_SMS["SMS / WhatsApp Checker"]
        UI_Email["Phishing Email Checker"]
        UI_URL["URL Link Checker"]
        UI_Phone["Phone Call Questionnaire"]
        UI_Result["Result & Guidance Card"]
        UI_Hist["Session Scan History"]
    end

    subgraph "Application Controller Layer (Flask 3.0)"
        App["app.py (Route Controller & Request Dispatcher)"]
        Config["config.py (Thresholds & Paths)"]
    end

    subgraph "OCR & Vision Pipeline"
        ImgPre["ocr/image_preprocessing.py (Enhance, Grayscale, Denoise)"]
        OCREng["ocr/ocr_engine.py (WinOCR / Pytesseract Engine)"]
        ContDet["ocr/content_detector.py (Type & URL Router)"]
    end

    subgraph "Machine Learning Inference Layer"
        PreProc["ml/preprocessing.py (Clean Text & Extract Links)"]
        FeatExt["ml/feature_extraction.py (17 URL Features)"]
        SMS_Model["SMS Model (TF-IDF + Logistic Regression)"]
        Email_Model["Email Model (TF-IDF + Logistic Regression)"]
        URL_Model["URL Model (Random Forest Classifier)"]
    end

    subgraph "Hybrid Risk & Explainability Engine"
        Rules["risk/rules.py (Heuristic Threat Patterns)"]
        PhoneRisk["risk/phone_risk.py (10-Question Matrix)"]
        RiskEng["risk/risk_engine.py (Hybrid Risk Aggregator)"]
        Explain["risk/explanations.py (Actionable Advice Generator)"]
    end

    UI_Home --> App
    UI_SMS --> App
    UI_Email --> App
    UI_URL --> App
    UI_Phone --> App

    App --> ImgPre --> OCREng --> ContDet
    App --> PreProc
    App --> FeatExt
    
    PreProc --> SMS_Model
    PreProc --> Email_Model
    FeatExt --> URL_Model
    ContDet --> PreProc

    SMS_Model --> RiskEng
    Email_Model --> RiskEng
    URL_Model --> RiskEng
    Rules --> RiskEng
    PhoneRisk --> RiskEng

    RiskEng --> Explain --> UI_Result
    App --> UI_Hist
```

---

### Diagram 2: Overall Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Senior / Non-Technical User
    participant Browser as Frontend UI
    participant Backend as Flask Application
    participant OCR as OCR & Vision Pipeline
    participant ML as Machine Learning Models
    participant Risk as Hybrid Risk Engine

    User->>Browser: Selects Check Option (SMS/Email/URL/Phone)
    Browser->>Backend: Submits Text, Screenshot, URL, or Answers
    alt Screenshot Uploaded
        Backend->>OCR: Preprocess Image & Extract Text
        OCR-->>Backend: Return Clean Text & Embedded Links
    end
    Backend->>ML: Run Specialized Feature Extraction & Inference
    ML-->>Backend: Return Probabilities (P_Text, P_URL)
    Backend->>Risk: Compute Hybrid Risk Score & Matched Rules
    Risk-->>Backend: Return Score (0-100), Level, Reasons, Actions
    Backend->>Browser: Render Accessible Result Page
    Browser->>User: View Risk Gauge, Explanations & Next Steps
```

---

### Diagram 3: Context Diagram (Level-0 DFD / Context Model)

```mermaid
flowchart LR
    User([User / Senior Citizen])
    ScamShield[[ScamShield System]]
    Admin([Developer / Lab Evaluator])

    User -->|Submits SMS, Email, URL, Screenshot, Call Answers| ScamShield
    ScamShield -->|Returns Risk Score, Reasons & Safety Actions| User
    
    Admin -->|Executes Training Scripts & Evaluates Metrics| ScamShield
    ScamShield -->|Generates Performance Reports & Model Artifacts| Admin
```

---

### Diagram 4: DFD Level 0 (High-Level Data Flow)

```mermaid
flowchart TD
    User([User]) -->|Inputs| P1[1.0 Ingest & Validate Input]
    P1 -->|Image File| P2[2.0 OCR Text & Link Extraction]
    P1 -->|Raw Text| P3[3.0 Text Preprocessing & Cleaning]
    P1 -->|URL String| P4[4.0 URL Lexical Feature Extraction]
    P1 -->|Call Responses| P5[5.0 Questionnaire Risk Calculation]
    
    P2 --> P3
    P2 --> P4
    
    P3 --> P6[6.0 ML Text Classification]
    P3 --> P7[7.0 Heuristic Rule Pattern Matching]
    P4 --> P8[8.0 ML URL Classification]
    
    P6 --> P9[9.0 Hybrid Risk Aggregation Engine]
    P7 --> P9
    P8 --> P9
    P5 --> P9
    
    P9 --> P10[10.0 Explanation & Action Synthesis]
    P10 -->|Visual Results View| User
```

---

### Diagram 5: SMS Workflow

```mermaid
flowchart TD
    A[Start SMS Check] --> B{Input Choice}
    B -->|Pasted Text| C[Clean Text & Strip HTML]
    B -->|Screenshot| D[Preprocess Image & Run OCR]
    D --> C
    C --> E[Extract Any Embedded URLs]
    C --> F[TF-IDF Vectorization & SMS Logistic Regression]
    C --> G[Evaluate Heuristic Rule Patterns]
    E -->|URLs Found| H[Extract URL Features & Run URL Random Forest]
    E -->|No URLs| I[Skip URL Classifier]
    F --> J[Compute SMS Hybrid Score]
    G --> J
    H --> J
    I --> J
    J --> K[Render Result Page]
```

---

### Diagram 6: Email Workflow

```mermaid
flowchart TD
    A[Start Email Check] --> B{Input Choice}
    B -->|Paste Subject & Body| C[Combine Subject + Body & Clean]
    B -->|Screenshot| D[OCR Scan & Auto-Extract Sender/Subject/Body]
    D --> C
    C --> E[Extract Embedded Links]
    C --> F[TF-IDF Vectorization & Email Logistic Regression]
    C --> G[Check Brand Impersonation & Heuristic Rules]
    E -->|Links Present| H[URL Random Forest Classifier]
    E -->|No Links| I[Skip URL Model]
    F --> J[Combine Email ML + URL ML + Rules]
    G --> J
    H --> J
    I --> J
    J --> K[Render Phishing Assessment Result]
```

---

### Diagram 7: URL Workflow

```mermaid
flowchart TD
    A[Start URL Check] --> B[Input URL String]
    B --> C[Validate & Normalize URL Scheme]
    C --> D[Extract 17 Structural & Lexical Features]
    D --> E[Check IP Address, Shorteners, Subdomain Count, HTTPS]
    D --> F[Random Forest URL Model Inference]
    E --> G[Evaluate URL Keyword Rules]
    F --> H[Combine URL ML Prob 75% + Rules 25%]
    G --> H
    H --> I[Assign Risk Level: Low, Med, High]
    I --> J[Display Pre-Click Safety Advice]
```

---

### Diagram 8: Screenshot → OCR → Detection Workflow

```mermaid
flowchart TD
    A[Upload Screenshot] --> B[Validate Format: PNG/JPG/WEBP & Size <=16MB]
    B --> C[Image Preprocessing: Grayscale, Contrast x1.8, Sharpen x1.5]
    C --> D{Local OCR Engine}
    D -->|Windows 10/11 Native| E[WinOCR Engine]
    D -->|Fallback| F[Pytesseract Engine]
    E --> G[Text Clean & Normalization]
    F --> G
    G --> H[Content Detector & Router]
    H -->|Email Headers Detected| I[Route to Email Model]
    H -->|Standalone Link Detected| J[Route to URL Model]
    H -->|Chat / SMS Patterns| K[Route to SMS Model]
    H --> L[Extract All Embedded URLs]
    L --> M[Pass to URL Classifier for Hybrid Scoring]
```

---

### Diagram 9: Phone Questionnaire Workflow

```mermaid
flowchart TD
    A[Start Phone Call Check] --> B[Present 10 Senior-Friendly Questions]
    B --> C[User Selects YES / NO on Each Question Card]
    C --> D[Submit Answers]
    D --> E[Apply Weighted Risk Matrix]
    E -->|OTP / Bank / Password YES| F[High Urgency Triggers (+30 each)]
    E -->|Remote Install / Threats YES| G[Critical Security Triggers (+25 each)]
    E -->|Urgency / Prize YES| H[Social Engineering Triggers (+15 each)]
    F --> I[Sum Total Weighted Points capped at 100]
    G --> I
    H --> I
    I --> J[Map to Risk Level: Low, Medium, High]
    J --> K[Generate Clear Call Safety Checklist]
```

---

### Diagram 10: Risk Score Workflow

```mermaid
flowchart TD
    A[Raw Classifier Probabilities & Rules] --> B{Are Embedded URLs Present?}
    B -->|Yes| C["Formula: 0.50*(P_Text*100) + 0.30*(P_URL*100) + 0.20*S_Rule"]
    B -->|No| D["Formula: 0.60*(P_Text*100) + 0.40*S_Rule"]
    
    C --> E[Cap Score between 0 and 100]
    D --> E
    
    E --> F{Score Range}
    F -->|0 - 29| G["LOW RISK: Potentially Safe (Green #16a34a)"]
    F -->|30 - 59| H["MEDIUM RISK: Suspicious (Amber #d97706)"]
    F -->|60 - 100| I["HIGH RISK: Potential Scam (Red #dc2626)"]
    
    G --> J[Build Human-Readable Reasons & Safety Actions]
    H --> J
    I --> J
```

---

### Diagram 11: Use Case Diagram

```mermaid
flowchart LR
    SeniorUser((Senior User))
    
    subgraph "ScamShield Application"
        UC1[Check Suspicious SMS]
        UC2[Check Phishing Email]
        UC3[Check Malicious URL]
        UC4[Assess Suspicious Phone Call]
        UC5[Upload & OCR Screenshot]
        UC6[View Plain-Language Reasons]
        UC7[View Actionable Safety Steps]
        UC8[View / Clear Local History]
        UC9[Adjust Font Size A+/A-]
    end

    SeniorUser --> UC1
    SeniorUser --> UC2
    SeniorUser --> UC3
    SeniorUser --> UC4
    SeniorUser --> UC5
    SeniorUser --> UC6
    SeniorUser --> UC7
    SeniorUser --> UC8
    SeniorUser --> UC9
```

---

### Diagram 12: Session History Data Model (ER / Session Schema)

```mermaid
erDiagram
    USER_SESSION ||--o{ SCAN_HISTORY_RECORD : maintains
    SCAN_HISTORY_RECORD {
        string id PK "Unique scan identifier (UUID 8-char)"
        string content_type "SMS, Email, URL, or Phone"
        string snippet "Sanitized preview text snippet"
        int risk_score "Estimated risk score (0-100)"
        string risk_level "LOW, MEDIUM, or HIGH"
        string risk_label "Display label string"
        string badge_class "CSS badge style class"
        string color "Hex color code"
        string timestamp "Human-readable timestamp"
    }
```

---

### Diagram 13: UI Navigation Flow

```mermaid
flowchart TD
    Home["Home Page (/)"] --> SMS["/check/sms (SMS Checker)"]
    Home --> Email["/check/email (Email Checker)"]
    Home --> URL["/check/url (URL Checker)"]
    Home --> Phone["/check/phone (Phone Questionnaire)"]
    Home --> Hist["/history (Scan History)"]

    SMS -->|Submit| Res["/analyze/sms -> Result Page"]
    Email -->|Submit| Res["/analyze/email -> Result Page"]
    URL -->|Submit| Res["/analyze/url -> Result Page"]
    Phone -->|Submit| Res["/analyze/phone -> Result Page"]

    Res -->|Check Another| Home
    Res -->|View History| Hist
    Hist -->|Clear History| Hist
    Hist -->|Back to Home| Home
```

---

### Diagram 14: ML Architecture & Training Flow

```mermaid
flowchart TD
    subgraph "Dataset Storage"
        D1["data/raw/sms_spam.csv (5,572 rows)"]
        D2["data/raw/email_phishing.csv (82,486 rows)"]
        D3["data/raw/url_dataset.csv (632,508 rows)"]
    end

    subgraph "Training Scripts (ml/)"
        T1["train_sms_model.py"]
        T2["train_email_model.py"]
        T3["train_url_model.py"]
    end

    subgraph "Feature Pipelines"
        F1["clean_text() -> TF-IDF (1-2 ngrams, 5000 max)"]
        F2["clean_text() -> TF-IDF (1-2 ngrams, 10000 max)"]
        F3["extract_url_features() -> 17 Handcrafted Lexical Features"]
    end

    subgraph "Serialized Models (models/)"
        M1["sms_model.pkl & sms_vectorizer.pkl"]
        M2["email_model.pkl & email_vectorizer.pkl"]
        M3["url_model.pkl & url_scaler.pkl"]
    end

    D1 --> T1 --> F1 --> M1
    D2 --> T2 --> F2 --> M2
    D3 --> T3 --> F3 --> M3

    subgraph "Evaluation (evaluate_models.py)"
        E["Accuracy, Precision, Recall, F1, ROC-AUC Reports"]
    end

    M1 --> E
    M2 --> E
    M3 --> E
```
