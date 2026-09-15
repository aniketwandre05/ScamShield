# Software Requirements Specification (SRS)
## SCAMSHIELD: AI-Based Scam Detection and Risk Assessment System

---

### Table of Contents
1. Introduction
2. Purpose
3. Scope
4. Problem Statement
5. Objectives
6. Intended Users & Personas
7. Overall Description
8. System Architecture
9. System Workflow
10. Functional Requirements
11. Use Cases
12. Machine Learning Requirements
13. Optical Character Recognition (OCR) Requirements
14. Risk Assessment & Hybrid Engine
15. User Interface & Accessibility Requirements
16. Database & Session Design
17. External Interfaces
18. Non-Functional Requirements
19. Security Requirements
20. Privacy Requirements
21. Constraints
22. Limitations
23. Testing Requirements
24. Deployment & Installation
25. Risks & Mitigation Strategies
26. Future Enhancements
27. References
28. Appendices

---

### 1. Introduction
ScamShield is an accessible, AI-powered scam detection and risk assessment web application tailored for older adults, non-technical users, and general smartphone owners to evaluate suspicious communications before acting.

### 2. Purpose
The primary purpose of ScamShield is **proactive scam prevention**. By offering an intuitive interface to scan SMS messages, emails, website links (URLs), and phone calls, the system calculates an Estimated Risk Score (0–100) and supplies human-readable explanations and actionable safety instructions.

### 3. Scope
The application encompasses:
- Text-based and screenshot-based SMS analysis.
- Multi-field and screenshot-based email phishing analysis.
- Pre-click structural and lexical feature analysis for URLs.
- A 10-question behavioral questionnaire for suspicious incoming phone calls.
- A transparent explanation engine detailing "Why" and "What to do".

### 4. Problem Statement
Cybercriminals exploit social engineering, brand impersonation, and panic-inducing messages to target vulnerable populations. Most cybersecurity tools produce cryptic error logs, require browser permissions, or overwhelm users with complex dashboards. Non-technical users need a frictionless, single-click verification safety assistant.

### 5. Objectives
- Implement specialized classical ML models for text and URL inspection.
- Build a unified hybrid risk aggregation layer combining ML probabilities and heuristic indicators.
- Provide open-source screenshot OCR for effortless mobile usage.
- Ensure strict compliance with WCAG AAA/AA accessibility standards (large touch targets, high contrast, readable typography).

### 6. Intended Users & Personas
- **Primary**: Older adults (60+ years) seeking reassurance on unfamiliar texts/calls.
- **Secondary**: Non-technical smartphone users and families assisting relatives.
- **Tertiary**: Educational/Academic ML lab evaluators.

### 7. Overall Description
The user navigates to the home page, selects one of four large cards (SMS, Email, URL, Phone Call), inputs the suspicious item (or uploads a screenshot), and instantly receives a calibrated Risk Gauge, a Risk Level (Low, Medium, High), reasons for the score, and safety recommendations.

### 8. System Architecture
ScamShield utilizes a modular, multi-tier architecture:
- **Presentation Layer**: HTML5, CSS3, Vanilla JS.
- **Application Controller**: Flask 3.0 routing and request handling.
- **OCR & Vision Pipeline**: Grayscale/contrast enhancement and Windows Native / Tesseract OCR.
- **Machine Learning Layer**: TF-IDF vectorizers, Logistic Regression classifiers, and Random Forest URL classifiers.
- **Risk & Explanation Layer**: Rule-based pattern matching and plain-language recommendation generation.

### 9. System Workflow
1. User selection of communication channel.
2. Input ingestion (Text, Screenshot, URL, or Questionnaire).
3. Preprocessing (cleaning, tokenization, URL extraction, OCR enhancement).
4. Model inference (Text model, URL model, or Questionnaire scoring).
5. Heuristic rule evaluation.
6. Hybrid risk score calculation (0–100).
7. Explanation synthesis and presentation.

### 10. Functional Requirements
- **FR-1**: Home page shall present four distinct, large clickable check options.
- **FR-2**: SMS module shall accept text input and screenshot image files.
- **FR-3**: Email module shall accept sender, subject, body, or screenshot image files.
- **FR-4**: URL module shall accept raw URL strings and inspect them safely without initiating external HTTP web requests.
- **FR-5**: Phone module shall evaluate 10 discrete yes/no behavioral questions.
- **FR-6**: System shall compute an Estimated Risk Score between 0 and 100.
- **FR-7**: System shall display clear "Why Did We Give This Score?" bullet points.
- **FR-8**: System shall display clear "What Should You Do Now?" action items.
- **FR-9**: System shall provide local session history with a clear-history option.

### 11. Use Cases
- **UC-1**: Senior user receives SMS claiming bank is locked; uploads screenshot; system flags High Risk (87/100) and warns against sharing OTP.
- **UC-2**: User receives email offering unclaimed funds; pastes text; system flags High Risk (86/100) and warns against wire transfers.
- **UC-3**: User checks shortened URL before clicking; system identifies hidden destination and IP host.
- **UC-4**: User checks unknown phone call asking for AnyDesk install; system advises immediately hanging up.

### 12. Machine Learning Requirements
- **ML-1**: SMS classifier shall use TF-IDF + Logistic Regression with balanced class weights.
- **ML-2**: Email classifier shall use TF-IDF + Logistic Regression with sublinear term frequency.
- **ML-3**: URL classifier shall extract 17 handcrafted features and predict via Random Forest (100 estimators).
- **ML-4**: All models shall achieve >95% accuracy and >0.98 ROC-AUC on benchmark test splits.

### 13. Optical Character Recognition (OCR) Requirements
- **OCR-1**: Image preprocessing shall apply contrast stretching, sharpening, and binarization.
- **OCR-2**: System shall support PNG, JPG, JPEG, and WEBP formats up to 16 MB.
- **OCR-3**: Extracted text shall be automatically parsed for embedded URLs.

### 14. Risk Assessment & Hybrid Engine
- Low Risk: 0–29 (Potentially Safe)
- Medium Risk: 30–59 (Suspicious)
- High Risk: 60–100 (Potential Scam)
- When embedded links exist, weights are 50% Text ML, 30% URL ML, 20% Heuristics.

### 15. User Interface & Accessibility Requirements
- High contrast ratio (WCAG compliant).
- Minimum button height of 48px.
- Base typography size: 18px with A+/A- scaling controls.
- Keyboard navigability with visible focus rings.

### 16. Database & Session Design
- Privacy-first session storage for recent scans.
- No storage of raw sensitive user credentials or message contents.

### 17. External Interfaces
- Standard web browser (Chrome, Edge, Firefox, Safari).
- Local operating system file dialog for screenshot uploads.

### 18. Non-Functional Requirements
- **Performance**: Response time under 500ms for text inference; under 1.5s for OCR screenshots.
- **Reliability**: Graceful degradation when models or OCR components are missing.
- **Maintainability**: Clean PEP 8 Python code with centralized configuration.

### 19. Security Requirements
- Safe URL parsing without executing web requests to target links.
- Secure filename sanitization (`secure_filename`).
- Immediate deletion of temporary uploaded screenshot files.
- CSRF protection and payload size restrictions (16 MB).

### 20. Privacy Requirements
- ScamShield never permanently persists user message contents or phone numbers.
- Clear user disclaimer on safe data handling.

### 21. Constraints
- Must run locally without requiring paid third-party cloud APIs.
- Must execute on standard student laptops.

### 22. Limitations
- Primary NLP models trained on English corpus.
- Offline static analysis without live sandbox execution.

### 23. Testing Requirements
- Unit tests for preprocessing, feature extractors, and risk calibration.
- Integration tests for all Flask routes and error scenarios.

### 24. Deployment & Installation
- Simple Python virtual environment setup via `requirements.txt`.
- Standalone execution with `python app.py`.

### 25. Risks & Mitigation Strategies
- **Risk**: User over-relies on system verdict.
- **Mitigation**: Prominently display "Estimated Risk Score" and "Potentially Safe" rather than "Guaranteed Safe".

### 26. Future Enhancements
- Multi-lingual scam pattern detection.
- Browser extension for real-time browsing protection.

### 27. References
- Scikit-Learn Machine Learning Documentation.
- SMS Spam Collection Dataset (UCI ML Repository).
- Anti-Phishing Working Group (APWG) Reports.

### 28. Appendices
- Configuration parameters list (`config.py`).
- Evaluation metric definitions (Precision, Recall, F1, ROC-AUC).
