"""
ScamShield Machine Learning Comprehensive Architecture & Viva Guide Generator
Generates a complete, publication-grade academic PDF for project evaluation and defense.
Context: Pune, Maharashtra, India.
100% Free of missing glyph square boxes (no unmapped Unicode/emojis).
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 806, "ScamShield: Machine Learning Architecture, Theory & Viva Defense Guide")
            self.drawRightString(559, 806, "Dept. of Computer Engineering")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 800, 559, 800)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 25, page_str)
        self.drawString(36, 25, "Confidential - Academic Project & ML Technical Evaluation Report | Pune, Maharashtra")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)
        self.restoreState()


def build_ml_guide_pdf(filename="ScamShield_Machine_Learning_Comprehensive_Guide.pdf"):
    # Page setup: A4 with 36pt (0.5 inch) margins -> Printable width = 523pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    # Color Palette
    primary_color = colors.HexColor("#0F172A")    # Deep Slate
    secondary_color = colors.HexColor("#1E3A8A")  # Royal Navy
    accent_blue = colors.HexColor("#2563EB")      # Accent Blue
    accent_teal = colors.HexColor("#0D9488")      # Teal
    dark_neutral = colors.HexColor("#334155")     # Slate 700
    light_bg = colors.HexColor("#F8FAFC")         # Slate 50
    table_header_bg = colors.HexColor("#1E293B")  # Slate 800
    border_color = colors.HexColor("#CBD5E1")     # Slate 300

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=secondary_color,
        spaceAfter=3,
        alignment=1 # Center
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=dark_neutral,
        spaceAfter=6,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=secondary_color,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=accent_blue,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_neutral,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=primary_color
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=secondary_color,
        spaceBefore=4,
        spaceAfter=1
    )

    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=dark_neutral,
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE BANNER, ELEVATOR PITCH & ARCHITECTURAL FOUNDATION
    # =========================================================================
    story.append(Paragraph("SCAMSHIELD: MACHINE LEARNING ARCHITECTURE & VIVA GUIDE", title_style))
    story.append(Paragraph(
        "<b>Comprehensive AI/ML Theory, Mathematical Foundations, Feature Engineering & Viva Defense</b><br/>"
        "Project Context: Pune, Maharashtra, India | Continuous Technical Evaluation",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=6))

    # 30-Second Elevator Pitch Box
    pitch_text = (
        "<b>30-SECOND ELEVATOR SUMMARY (THE OPENING DEFENSE STATEMENT):</b><br/>"
        "<i>\"ScamShield is a privacy-first, multilingual fraud detection system designed to protect vulnerable users "
        "from cyber scams across SMS, Email, and URLs. Instead of relying on a single slow black-box model, ScamShield "
        "deploys a <b>Modular Hybrid AI Architecture</b>: three specialized machine learning models (Word+Character n-gram "
        "Logistic Regression for SMS, Subject-Boosted Logistic Regression for Email, and a 22-feature Random Forest for URLs) "
        "calibrated alongside a deterministic Heuristic Rule Engine. The system achieves over <b>99% accuracy</b>, executes "
        "inference in under <b>15 milliseconds on CPU</b>, and provides actionable safety advice in English, Marathi, and Hindi.\"</i>"
    )
    t_pitch = Table([[Paragraph(pitch_text, callout_style)]], colWidths=[523])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, accent_blue),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 6))

    # Section 1: Problem Formulation & Architecture
    story.append(Paragraph("1. Problem Formulation & Architecture: Why a Modular Hybrid System?", h1_style))
    story.append(Paragraph(
        "ScamShield formulates fraud detection as <b>Supervised Binary Classification</b>: for any given input x, "
        "the system computes a continuous calibrated probability <i>P(y=1|x) in [0, 1]</i> that x is malicious. "
        "Rather than forcing a single model across heterogeneous vectors, ScamShield decouples the problem into three specialized pipelines.",
        body_style
    ))

    # Why Modular Table
    arch_comparison = [
        [Paragraph("Attack Vector", table_header_style), Paragraph("Syntactic Structure", table_header_style), Paragraph("Where Threat Lives", table_header_style), Paragraph("Why a Single Generic Model Fails", table_header_style)],
        [Paragraph("SMS / WhatsApp", table_cell_bold), Paragraph("Short (<160 chars), unpunctuated, Hinglish/Marathi slang", table_cell_style), Paragraph("Urgent psychological coercion (light bill, lottery)", table_cell_style), Paragraph("Generic NLP models treat regional slang & typos as out-of-vocabulary noise.", table_cell_style)],
        [Paragraph("Email Phishing", table_cell_bold), Paragraph("Long-form (500-5000 chars), structured headers & body", table_cell_style), Paragraph("High density in Subject line & call-to-action link", table_cell_style), Paragraph("Long benign body text dilutes the few critical urgent threat keywords.", table_cell_style)],
        [Paragraph("URL / Links", table_cell_bold), Paragraph("Purely syntactic string (RFC 3986), non-natural language", table_cell_style), Paragraph("Shannon entropy, domain depth, high-risk TLDs", table_cell_style), Paragraph("Language tokenizers fail on URLs or split them into meaningless byte fragments.", table_cell_style)]
    ]
    t_arch = Table(arch_comparison, colWidths=[90, 130, 140, 163])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 6))

    # Classical ML vs Deep Learning Matrix
    story.append(Paragraph("2. Algorithmic Justification: Classical Machine Learning vs. Deep Learning / LLMs", h1_style))
    ml_vs_dl = [
        [Paragraph("Evaluation Criterion", table_header_style), Paragraph("ScamShield Classical ML (Current)", table_header_style), Paragraph("Deep Learning / Large Language Models (BERT/LLM)", table_header_style), Paragraph("Engineering Verdict", table_header_style)],
        [Paragraph("Inference Latency", table_cell_bold), Paragraph("<15 milliseconds on basic CPU", table_cell_style), Paragraph("500 - 3,000 milliseconds (requires GPU)", table_cell_style), Paragraph("PASS: Essential for real-time mobile/shopkeeper UPI checks", table_cell_bold)],
        [Paragraph("Memory & Binary Size", table_cell_bold), Paragraph("<50 MB RAM; ~3 MB model binaries (.pkl)", table_cell_style), Paragraph("2 GB - 10 GB VRAM required", table_cell_style), Paragraph("PASS: Runs on low-cost cloud tiers and edge devices", table_cell_bold)],
        [Paragraph("Mathematical Explainability", table_cell_bold), Paragraph("Direct log-odds weights & Gini feature importance", table_cell_style), Paragraph("Opaque multi-billion parameter black-box", table_cell_style), Paragraph("PASS: Enables plain-language trilingual XAI explanations", table_cell_bold)],
        [Paragraph("Adversarial Zero-Day Defense", table_cell_bold), Paragraph("Compounded with deterministic Heuristic Rule Engine", table_cell_style), Paragraph("Vulnerable to prompt injection & jailbreaking", table_cell_style), Paragraph("PASS: Deterministic rules guarantee zero-tolerance security", table_cell_bold)]
    ]
    t_mldl = Table(ml_vs_dl, colWidths=[110, 140, 140, 133])
    t_mldl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_mldl)

    # =========================================================================
    # PAGE 2: MATHEMATICAL FOUNDATIONS & FEATURE ENGINEERING
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Mathematical Foundations of the Deployed Algorithms", h1_style))

    math_content = (
        "<b>A. LOGISTIC REGRESSION WITH L2 REGULARIZATION (SMS & EMAIL):</b><br/>"
        "Logistic Regression maps linear combinations of input features into calibrated probabilities [0, 1] using the <b>Sigmoid (Logistic) Function</b>:<br/>"
        "&nbsp;&nbsp;&bull; Linear combination: <i>z = w<sup>T</sup>x + b = &sum; w<sub>j</sub> x<sub>j</sub> + b</i><br/>"
        "&nbsp;&nbsp;&bull; Probability output: <i>P(y = 1 | x) = &sigma;(z) = 1 / (1 + e<sup>-z</sup>)</i><br/>"
        "&nbsp;&nbsp;&bull; <b>Penalized Log-Loss (Binary Cross-Entropy) Objective:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>L(w) = - (1/N) &sum; [ y<sub>i</sub> ln(y_hat<sub>i</sub>) + (1 - y<sub>i</sub>) ln(1 - y_hat<sub>i</sub>) ] + (1 / 2C) ||w||<sub>2</sub><sup>2</sup></i><br/>"
        "&nbsp;&nbsp;&bull; <i>Why this works:</i> Convex loss surface guarantees global convergence. High-dimensional sparse TF-IDF spaces (14,000 dimensions) "
        "have linear decision boundaries that prevent overfitting. The inverse regularization parameter <i>C</i> was tuned to <b>C=5.0</b> for SMS and <b>C=3.0</b> for Email.<br/><br/>"
        "<b>B. RANDOM FOREST CLASSIFIER WITH GINI IMPURITY (URL LINKS):</b><br/>"
        "Random Forest is an ensemble of <i>B = 100</i> decision trees trained on bootstrap samples with random feature subsets:<br/>"
        "&nbsp;&nbsp;&bull; Ensemble Probability: <i>P_hat(y = 1 | x) = (1 / B) &sum; T<sub>b</sub>(x)</i><br/>"
        "&nbsp;&nbsp;&bull; <b>Gini Impurity Splitting Criterion:</b> <i>I<sub>G</sub>(p) = 1 - (p<sub>safe</sub><sup>2</sup> + p<sub>scam</sub><sup>2</sup>)</i> (pure leaf = 0.0, split = 0.5)<br/>"
        "&nbsp;&nbsp;&bull; <i>Hyperparameter constraints:</i> <b>max_depth=15</b> and <b>min_samples_split=5</b> prevent memorization of training URLs."
    )
    t_math = Table([[Paragraph(math_content, body_style)]], colWidths=[523])
    t_math.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_math)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Feature Engineering Innovations: Dual-Channel Subwords & 22 URL Features", h1_style))
    story.append(Paragraph(
        "<b>SMS Subword FeatureUnion:</b> Standard word tokenizers fail on intentional typos (<i>p@ypal, s-b-i</i>) and Hinglish/Marathi transliteration (<i>paise, light bill</i>). "
        "ScamShield uses <b>FeatureUnion</b> combining Word-level TF-IDF (1-3 ngrams, 7,000 features) and Character-boundary TF-IDF (char_wb, 3-5 ngrams, 7,000 features). "
        "Subword chunks match the root scam pattern regardless of spelling variations, <b>boosting Recall from 88.59% to 94.63%</b>.<br/>"
        "<b>Email Subject-Line Boosting:</b> In phishing, the subject line contains 2-3x higher scam intent density than the body. "
        "ScamShield double-weights the subject (<i>f\"{subject} {subject} {body}\"</i>), doubling subject feature frequencies without distorting body context.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 22 URL Features Table
    story.append(Paragraph("<b>Complete 22-Feature URL Structural Space (Zero Network Requests):</b>", h2_style))
    url_feat_table = [
        [Paragraph("Feature Group", table_header_style), Paragraph("Feature Name", table_header_style), Paragraph("Type", table_header_style), Paragraph("Threat Detection Rationale", table_header_style)],
        [Paragraph("Lengths", table_cell_bold), Paragraph("url_length, hostname_length, path_length, query_length", table_cell_style), Paragraph("Integer", table_cell_style), Paragraph("Malicious URLs elongate paths to conceal domains or pass encoded attack payloads.", table_cell_style)],
        [Paragraph("Delimiters", table_cell_bold), Paragraph("count_dots, count_hyphens, count_at, count_slash, count_equal", table_cell_style), Paragraph("Integer", table_cell_style), Paragraph("Chained hyphens (sbi-yono-update) and '@' symbols indicate credential injection.", table_cell_style)],
        [Paragraph("Structural", table_cell_bold), Paragraph("subdomain_count, count_digits, count_special_chars", table_cell_style), Paragraph("Integer", table_cell_style), Paragraph("Subdomain stacking (paypal.com.verify-login.xyz) mimics official hosts.", table_cell_style)],
        [Paragraph("Security Flags", table_cell_bold), Paragraph("has_https, has_ip_address, is_shortened, suspicious_keyword_count", table_cell_style), Paragraph("Binary/Int", table_cell_style), Paragraph("Flags raw IPv4 links, URL shorteners (bit.ly), and banking keywords (kyc, otp, login).", table_cell_style)],
        [Paragraph("Advanced Domain", table_cell_bold), Paragraph("entropy (Shannon Entropy of Hostname)", table_cell_style), Paragraph("Float", table_cell_style), Paragraph("H(S) = -&sum; p(c) log2 p(c). High entropy (>3.8) detects auto-generated DGA phishing domains.", table_cell_style)],
        [Paragraph("Advanced Domain", table_cell_bold), Paragraph("has_high_risk_tld", table_cell_style), Paragraph("Binary", table_cell_style), Paragraph("Flags heavily abused free/cheap extensions (.xyz, .top, .buzz, .cfd, .rest, .tk, .icu).", table_cell_style)],
        [Paragraph("Targeted Brand", table_cell_bold), Paragraph("brand_keyword_count, host_hyphen_count, digit_ratio_host", table_cell_style), Paragraph("Int/Float", table_cell_style), Paragraph("Catches targeted Indian brand lures (sbi, yono, paytm, mahadiscom) with numeric obfuscation.", table_cell_style)]
    ]
    t_url_feat = Table(url_feat_table, colWidths=[80, 140, 50, 253])
    t_url_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_url_feat)

    # =========================================================================
    # PAGE 3: HYBRID RISK ENGINE & EMPIRICAL EVALUATION METRICS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. The Hybrid Risk Calibration Engine: Blending ML with Deterministic Rules", h1_style))
    story.append(Paragraph(
        "Machine learning models provide continuous probabilities based on statistical patterns. However, cybersecurity requires strict zero-tolerance safeguards. "
        "ScamShield pairs the ML models with a <b>Heuristic Rule Engine</b> through late-stage linear fusion:",
        body_style
    ))

    # Formula Box
    formula_text = (
        "<b>HYBRID RISK SCORING FORMULAS:</b><br/>"
        "&bull; <b>With Embedded URL:</b> <i>Risk Score = 0.45 &times; (P<sub>Text</sub> &times; 100) + 0.35 &times; (P<sub>URL</sub> &times; 100) + 0.20 &times; S<sub>Rule</sub></i><br/>"
        "&bull; <b>Text Only (SMS / Email):</b> <i>Risk Score = 0.60 &times; (P<sub>Text</sub> &times; 100) + 0.40 &times; S<sub>Rule</sub></i><br/>"
        "&bull; <b>Standalone URL:</b> <i>Risk Score = 0.70 &times; (P<sub>URL</sub> &times; 100) + 0.30 &times; S<sub>Rule</sub></i><br/>"
        "&nbsp;&nbsp;&bull; <i>P<sub>Text</sub>, P<sub>URL</sub> in [0, 1]</i>: Continuous model probabilities.<br/>"
        "&nbsp;&nbsp;&bull; <i>S<sub>Rule</sub> in [0, 100]</i>: Cumulative penalty for deterministic red flags (Raw IP +40, Sender mismatch +35, Shortener +25, Power cut threat +50).<br/>"
        "<b>Calibrated Risk Tiers:</b> <b>Low Risk (0 - 39)</b>: Safe / verified | <b>Medium Risk (40 - 69)</b>: Cautionary warning | <b>High Risk (70 - 100)</b>: Active scam"
    )
    t_form = Table([[Paragraph(formula_text, body_style)]], colWidths=[523])
    t_form.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")), # Light amber
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D97706")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_form)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Empirical Evaluation Metrics & Confusion Matrices", h1_style))
    story.append(Paragraph(
        "All models were evaluated on independent, held-out test distributions (20% stratified test split). "
        "In fraud detection, <b>Recall is the primary safety metric</b> because a False Negative (missed scam) leads to financial catastrophe, "
        "whereas a False Positive merely triggers a cautionary alert.",
        body_style
    ))

    # Metrics Table
    summary_metrics = [
        [Paragraph("Module", table_header_style), Paragraph("Algorithm & Configuration", table_header_style), Paragraph("Test Size", table_header_style), Paragraph("Accuracy", table_header_style), Paragraph("Precision", table_header_style), Paragraph("Recall", table_header_style), Paragraph("F1-Score", table_header_style), Paragraph("ROC-AUC", table_header_style)],
        [Paragraph("SMS Message", table_cell_bold), Paragraph("FeatureUnion TF-IDF + Logistic Reg (C=5.0)", table_cell_style), Paragraph("1,115", table_cell_style), Paragraph("99.19%", table_cell_bold), Paragraph("99.30%", table_cell_style), Paragraph("94.63%", table_cell_bold), Paragraph("96.91%", table_cell_bold), Paragraph("0.9944", table_cell_style)],
        [Paragraph("Email Phishing", table_cell_bold), Paragraph("Subject-Boosted TF-IDF + Logistic Reg (C=3.0)", table_cell_style), Paragraph("8,000", table_cell_style), Paragraph("98.22%", table_cell_bold), Paragraph("97.89%", table_cell_style), Paragraph("98.58%", table_cell_bold), Paragraph("98.23%", table_cell_bold), Paragraph("0.9979", table_cell_style)],
        [Paragraph("URL / Links", table_cell_bold), Paragraph("Random Forest (100 trees, depth 15, 22 feats)", table_cell_style), Paragraph("8,000", table_cell_style), Paragraph("99.05%", table_cell_bold), Paragraph("99.90%", table_cell_bold), Paragraph("98.20%", table_cell_bold), Paragraph("99.04%", table_cell_bold), Paragraph("0.9984", table_cell_style)]
    ]
    t_sum = Table(summary_metrics, colWidths=[70, 145, 45, 48, 48, 48, 52, 52])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 6))

    # Confusion Matrices Table
    story.append(Paragraph("<b>Held-out Test Confusion Matrices:</b>", h2_style))
    cm_data = [
        [Paragraph("Model", table_header_style), Paragraph("True Negatives (TN)", table_header_style), Paragraph("False Positives (FP)", table_header_style), Paragraph("False Negatives (FN)", table_header_style), Paragraph("True Positives (TP)", table_header_style), Paragraph("Clinical Interpretation", table_header_style)],
        [Paragraph("SMS Classifier (N=1,115)", table_cell_bold), Paragraph("965 (Safe)", table_cell_style), Paragraph("1 (Safe flagged)", table_cell_style), Paragraph("8 (Scam missed)", table_cell_style), Paragraph("141 (Scam caught)", table_cell_bold), Paragraph("Only 1 false alarm out of 966 safe texts; caught 94.6% of scams.", table_cell_style)],
        [Paragraph("Email Classifier (N=8,000)", table_cell_bold), Paragraph("3,915 (Safe)", table_cell_style), Paragraph("85 (Safe flagged)", table_cell_style), Paragraph("57 (Phish missed)", table_cell_style), Paragraph("3,943 (Phish caught)", table_cell_bold), Paragraph("Caught 3,943 out of 4,000 phishing attacks; precision 97.9%.", table_cell_style)],
        [Paragraph("URL Classifier (N=8,000)", table_cell_bold), Paragraph("3,996 (Benign)", table_cell_style), Paragraph("4 (Benign flagged)", table_cell_style), Paragraph("72 (Malicious missed)", table_cell_style), Paragraph("3,928 (Malicious caught)", table_cell_bold), Paragraph("Exceptional 99.9% precision; only 4 false alarms across 4,000 benign URLs.", table_cell_style)]
    ]
    t_cm = Table(cm_data, colWidths=[110, 68, 68, 68, 68, 141])
    t_cm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,1), (4,-1), 'CENTER'),
    ]))
    story.append(t_cm)

    # =========================================================================
    # PAGE 4 & 5: VIVA CHEAT SHEET (TOP 12 QUESTIONS & MODEL ANSWERS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Viva Defense & Technical Evaluation: Top 12 Questions & Answers", h1_style))
    story.append(Paragraph("Carefully study these 12 questions; they represent the exact technical topics examiners interrogate during project defense:", body_style))
    story.append(Spacer(1, 4))

    qas = [
        ("Q1: Why is Recall prioritized over Precision in cyber scam detection?",
         "In fraud detection, a False Negative means a victim receives an active scam, believes it, and loses money. A False Positive merely causes minor friction by showing a cautionary warning on a safe message. High Recall (>94% on SMS, >98% on Email) ensures virtually no real scams slip through."),
        
        ("Q2: How did you prevent data leakage during training?",
         "We performed stratified 80/20 train/test splitting before applying any feature extraction or scaling. Vectorizers (TfidfVectorizer, FeatureUnion) and scalers were fitted strictly on X_train using fit_transform(), and then applied to X_test using transform() alone. No test data informed the vocabulary or parameters."),
        
        ("Q3: If an attacker uses a valid HTTPS link, how does your URL model catch it?",
         "Over 80% of modern phishing sites use free SSL certificates (Let's Encrypt). Our model does not rely solely on has_https; it incorporates Shannon entropy (detecting random auto-generated domains), High-risk TLD tracking (.xyz, .top), Indian brand lure scanning (sbi, yono, paytm in host), and subdomain stacking count."),
        
        ("Q4: How does the SMS model handle Hinglish and Marathi code-mixing?",
         "We implemented a FeatureUnion combining word n-grams (1-3) with character-boundary n-grams (char_wb, 3-5 characters). Subword fragments match the morphological patterns of regional transliterations (paise, bhejo, light bill) and typo variations, even if the complete word is not in an English dictionary."),
        
        ("Q5: Why did you use TF-IDF with sublinear_tf=True instead of simple CountVectorizer?",
         "CountVectorizer only counts raw frequency, allowing common uninformative words to dominate. TF-IDF boosts words that are unique to scam documents (suspended, kyc, lottery). Setting sublinear_tf=True (1 + ln(tf)) prevents long messages from dominating feature weights simply by repeating threat words."),
        
        ("Q6: What does the hyperparameter C do in Logistic Regression?",
         "C is the inverse of regularization strength (C = 1/lambda). A small C applies heavy shrinkage to weights to prevent overfitting; a large C fits training features more closely. We tuned C=5.0 for SMS and C=3.0 for Email to maximize recall while maintaining low false-positive rates."),
        
        ("Q7: What is Shannon Entropy and how does it detect malicious URLs?",
         "Shannon entropy measures information uncertainty and character randomness: H(S) = -&sum; p(c) log2 p(c). Legitimate domains (google.com, apple.com) have low entropy (1.5 - 2.8) due to phonetic redundancy. Auto-generated DGA domains (x7k9-p4zm1.com) have high entropy (>3.8)."),
        
        ("Q8: Why did you restrict max_depth=15 in Random Forest?",
         "Without max_depth, decision trees expand until all leaves are completely pure, causing extreme overfitting, bloated model sizes (>50 MB), and slow inference. Restricting to depth 15 with min_samples_split=5 ensures generalizability, keeps inference <5ms, and limits binary size to ~3 MB."),
        
        ("Q9: How do you handle class imbalance in the SMS dataset?",
         "In the raw SMS dataset, only 13.4% are spam and 86.6% are ham. A naive model would predict 'Safe' 100% of the time and achieve 86.6% accuracy while catching zero scams. We resolved this using class_weight='balanced', which multiplies the loss penalty for minority scam samples inversely proportional to class frequencies."),
        
        ("Q10: Why do you avoid making live network requests during URL analysis?",
         "1. User Safety: Visiting malicious links triggers drive-by malware or confirms active victim addresses to scammers. 2. Latency: Network round-trips take 1000 - 3000ms; local lexical extraction takes <2ms. 3. Privacy: The user's browsing activity is never shared with third parties."),
        
        ("Q11: What is the purpose of the OCR vision module and how does it integrate with ML?",
         "Elderly users and shopkeepers often receive fraud via WhatsApp screenshots rather than text. We use Tesseract OCR with OpenCV adaptive thresholding and grayscale conversion. The extracted text is automatically classified as SMS or URL and routed to the corresponding ML predictor seamlessly."),
        
        ("Q12: How is client privacy protected before machine learning inference?",
         "ScamShield includes a client-side Privacy Redaction Engine that scrubs Indian PII (Aadhaar 12-digit numbers, PAN 10-digit IDs, UPI VPA handles, and credit card numbers) using regular expressions before saving logs or sending text to inference routines.")
    ]

    for q, a in qas[:6]:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(f"&bull; <i>Model Answer:</i> {a}", qa_a_style))

    story.append(PageBreak())
    story.append(Paragraph("7. Viva Defense & Technical Evaluation (Continued)", h1_style))
    story.append(Spacer(1, 4))

    for q, a in qas[6:]:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(f"&bull; <i>Model Answer:</i> {a}", qa_a_style))

    story.append(Spacer(1, 6))

    # Section 8: Key Codebase Inventory
    story.append(Paragraph("8. Codebase Directory & File Inventory for Technical Review", h1_style))
    code_inv = [
        [Paragraph("Component", table_header_style), Paragraph("File Path", table_header_style), Paragraph("Key Class / Function", table_header_style)],
        [Paragraph("SMS Model Training", table_cell_bold), Paragraph("ml/train_sms_model.py", table_cell_style), Paragraph("train_sms_model() with FeatureUnion", table_cell_style)],
        [Paragraph("Email Model Training", table_cell_bold), Paragraph("ml/train_email_model.py", table_cell_style), Paragraph("train_email_model() with Subject Boosting", table_cell_style)],
        [Paragraph("URL Model Training", table_cell_bold), Paragraph("ml/train_url_model.py", table_cell_style), Paragraph("train_url_model() with 22 features", table_cell_style)],
        [Paragraph("Feature Engineering", table_cell_bold), Paragraph("ml/feature_extraction.py", table_cell_style), Paragraph("extract_url_features(), shannon_entropy()", table_cell_style)],
        [Paragraph("Inference Predictors", table_cell_bold), Paragraph("ml/prediction.py", table_cell_style), Paragraph("SMSPredictor, EmailPredictor, URLPredictor", table_cell_style)],
        [Paragraph("Hybrid Risk Engine", table_cell_bold), Paragraph("risk/risk_engine.py", table_cell_style), Paragraph("compute_hybrid_risk() with calibrated weights", table_cell_style)],
        [Paragraph("Privacy Redaction", table_cell_bold), Paragraph("risk/privacy.py", table_cell_style), Paragraph("mask_sensitive_data() (Aadhaar, PAN, UPI)", table_cell_style)],
        [Paragraph("Evaluation Runner", table_cell_bold), Paragraph("ml/evaluate_models.py", table_cell_style), Paragraph("evaluate_all() generating overall summary metrics", table_cell_style)]
    ]
    t_inv = Table(code_inv, colWidths=[110, 160, 253])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_inv)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")


if __name__ == "__main__":
    build_ml_guide_pdf()
