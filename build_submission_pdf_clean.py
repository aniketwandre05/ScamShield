"""
ScamShield HCI Continuous Evaluation Assignment - Publication-Grade PDF Generator
Exact 9-Page Rebuild conforming to user requirements:
1. Zero mentions of Pune, participant locations, or device names anywhere in the PDF.
2. Reframed natural academic text (no blank gaps, dashes, or awkward omissions).
3. Page 5 titled "Interview Photographs" with a clean blank mounting page (NO blank boxes).
4. Page 6 of original PDF completely deleted. Total page count is EXACTLY 9.
5. High-resolution wireframe blueprints (Page 8) and academic poster (Page 9) preserved.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print exact 'Page X of Y' total page count."""
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header on Pages 2 through 9 (Clean reframing without geographic tags)
        if self._pageNumber > 1:
            self.drawString(36, 806, "ScamShield: HCI Continuous Evaluation Assignment (20 Marks) | Academic Field Study & Prototype")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 800, 559, 800)

        # Running Footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 25, page_str)
        self.drawString(36, 25, "Confidential - Academic Project Report | Dept. of Computer Engineering")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)
        self.restoreState()


def build_submission_pdf(filename="Submission PDF.pdf"):
    # Target page dimensions: A4 (595.27 x 841.89 pt), margins: 36pt L/R, 44pt T/B.
    # Printable width: 523.27 pt, Printable height: 753.89 pt.
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
    primary_color = colors.HexColor("#1E3A8A")   # Deep Navy
    secondary_color = colors.HexColor("#2563EB") # Royal Blue
    dark_neutral = colors.HexColor("#0F172A")    # Slate 900
    text_muted = colors.HexColor("#475569")      # Slate 600
    bg_light = colors.HexColor("#F8FAFC")        # Off-white
    border_color = colors.HexColor("#CBD5E1")    # Border gray

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=primary_color,
        spaceAfter=2,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=secondary_color,
        spaceAfter=3,
        alignment=1
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_neutral,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_color,
        spaceBefore=5,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11.5,
        textColor=secondary_color,
        spaceBefore=4,
        spaceAfter=2.5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=dark_neutral,
        spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.4,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    # 2-Column Interview Card Styles
    card_hdr_left = ParagraphStyle(
        'CHL',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white
    )

    card_hdr_right = ParagraphStyle(
        'CHR',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#93C5FD"),
        alignment=2
    )

    card_field_title = ParagraphStyle(
        'CFT',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=primary_color,
        spaceAfter=1
    )

    card_field_body = ParagraphStyle(
        'CFB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.9,
        leading=9.0,
        textColor=dark_neutral
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, SCOPE & IDENTIFICATION OF USER GROUPS
    # =========================================================================
    story.append(Paragraph("CONTINUOUS EVALUATION ASSIGNMENT (20 MARKS)", title_style))
    story.append(Paragraph("HUMAN-COMPUTER INTERACTION (HCI) FIELD STUDY & PROTOTYPE", title_style))
    story.append(Paragraph("Project: ScamShield - Accessible, Multilingual Scam Detection &amp; Decision-Support System", subtitle_style))
    story.append(Paragraph("Target Demographic: Multi-Generational &amp; Regional Language Cohorts | Academic Year: 2026-2027<br/>Course: Human-Computer Interaction | Submission: Comprehensive 7-Stage Engineering &amp; Field Report", meta_style))
    story.append(Spacer(1, 4))

    # Team Members Table
    team_data = [
        [
            Paragraph("<b>Aniket Wandre</b><br/><font size=\"7\" color=\"#475569\">MIS No. 112415240</font>", table_cell_style),
            Paragraph("<b>Sudarshan Jyotik</b><br/><font size=\"7\" color=\"#475569\">MIS No. 112415216</font>", table_cell_style),
            Paragraph("<b>Parth Solanke</b><br/><font size=\"7\" color=\"#475569\">MIS No. 112415213</font>", table_cell_style),
            Paragraph("<b>FACULTY GUIDE</b><br/><font size=\"7\" color=\"#1E3A8A\"><b>Dr. Shrikant Salve</b></font>", table_cell_style)
        ]
    ]
    team_table = Table(team_data, colWidths=[130, 130, 130, 133])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 4))

    # Project Abstract
    story.append(Paragraph(
        "<b>Project Abstract &amp; HCI Scope:</b> Digital communication fraud in India—ranging from fake electricity disconnection alerts "
        "and suspicious bank KYC update SMS to fraudulent job offers and remote screen-sharing requests—disproportionately targets vulnerable "
        "regional populations who lack English technical literacy. This project conducts a rigorous contextual inquiry across 10 diverse "
        "in-person field interviews (spanning teachers, kirana shopkeepers, farmers, senior pensioners, and homemakers). By applying Nielsen's 10 "
        "Heuristics, Shneiderman's Golden Rules, and WCAG 2.2 accessibility standards, we identify critical research gaps and present a fully "
        "functional, multilingual (English, Marathi, Hindi) prototype with OCR screenshot analysis, explainable risk meter, and immediate "
        "emergency helpline integration (Dial 1930 / cybercrime.gov.in).",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Section 1: Identification of User Groups
    story.append(Paragraph("1. Identification of User Groups", h1_style))
    story.append(Paragraph(
        "To understand how everyday citizens across diverse communities perceive, evaluate, and react to scam messages and deceptive phone calls, "
        "we stratified the population into six representative demographic segments based on tech literacy, language habits, and economic activity:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # 3-Column User Groups Table (No Geographic Pockets column, perfectly reframed)
    user_groups_data = [
        [
            Paragraph("User Segment", table_header_style),
            Paragraph("Primary Scam Threats Experienced", table_header_style),
            Paragraph("Language &amp; Tech Behavioral Profile", table_header_style)
        ],
        [
            Paragraph("<b>Senior Citizens &amp; Pensioners</b>", table_cell_bold),
            Paragraph("Fake electricity bill cuts, pension life certificate SMS, digital arrest threats, bank KYC suspension notices.", table_cell_style),
            Paragraph("Prefer Marathi. High anxiety regarding authority; rely on adult children for verification; struggle with small fonts.", table_cell_style)
        ],
        [
            Paragraph("<b>Primary &amp; High School Teachers</b>", table_cell_bold),
            Paragraph("Principal/Education officer impersonation, fake investment schemes, unverified teacher welfare links.", table_cell_style),
            Paragraph("Bilingual (Marathi/English). Active on WhatsApp groups; susceptible to social engineering from colleagues.", table_cell_style)
        ],
        [
            Paragraph("<b>Small Kirana &amp; Retail Merchants</b>", table_cell_bold),
            Paragraph("Fake UPI payment confirmation screenshots, soundbox spoofing, reverse QR code 'receive money' fraud.", table_cell_style),
            Paragraph("Heavy daily UPI users (PhonePe/GPay). High distraction during rush hours; need instant 2-second verification.", table_cell_style)
        ],
        [
            Paragraph("<b>Peri-Urban Farmers &amp; Dairies</b>", table_cell_bold),
            Paragraph("PM-Kisan subsidy fake links, solar pump subsidy frauds, fraudulent agricultural loan apps.", table_cell_style),
            Paragraph("Exclusively Marathi script. Low digital literacy; highly vulnerable to financial promises in Marathi.", table_cell_style)
        ],
        [
            Paragraph("<b>Homemakers</b>", table_cell_bold),
            Paragraph("Part-time YouTube 'like &amp; earn' tasks on Telegram, courier/customs gift parcel scams, lottery alerts.", table_cell_style),
            Paragraph("Heavy smartphone users for social media &amp; family communication; hesitant to report fraud due to family stigma.", table_cell_style)
        ],
        [
            Paragraph("<b>College Students &amp; Gig Workers</b>", table_cell_bold),
            Paragraph("Work-from-home data entry traps, fake internship offer letters, traffic e-challan SMS, instant loan apps.", table_cell_style),
            Paragraph("Fluent in English &amp; mobile UI, but overconfident; prone to hasty impulse clicks on lucrative offers.", table_cell_style)
        ]
    ]
    user_groups_table = Table(user_groups_data, colWidths=[110, 208, 205])
    user_groups_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(user_groups_table)

    # =========================================================================
    # PAGE 2: CONTEXTUAL INQUIRY PROTOCOL & INTERVIEWS #1 - #3
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Contextual Inquiry: 10 In-Person Field Interviews", h1_style))
    story.append(Paragraph(
        "<b>Field Methodology:</b> In-person contextual inquiry interviews were conducted across diverse residential, commercial, and agricultural "
        "communities. Visual consent was established, and interviewees demonstrated their recent SMS inboxes, WhatsApp chats, and call logs. "
        "A standardized 10-question questionnaire was administered in their language of choice (Marathi, Hindi, or English). "
        "Original photographic evidence and observation records are presented in the subsequent dedicated evidence section.",
        body_style
    ))
    story.append(Spacer(1, 2))

    # Standardized 10-Question Questionnaire Protocol Table (3-Column compact layout matching original)
    story.append(Paragraph("Standardized 10-Question Questionnaire Protocol", h2_style))
    q_data = [
        [Paragraph("Q#", table_header_style), Paragraph("Research Focus", table_header_style), Paragraph("Question Administered to Users", table_header_style)],
        [Paragraph("Q1", table_cell_bold), Paragraph("Frequency", table_cell_style), Paragraph("How often do you receive unsolicited messages, links, or phone calls claiming banking issues, electricity cuts, or prizes?", table_cell_style)],
        [Paragraph("Q2", table_cell_bold), Paragraph("Language", table_cell_style), Paragraph("In what language are these messages written, and can you easily understand technical security terms in English?", table_cell_style)],
        [Paragraph("Q3", table_cell_bold), Paragraph("Exposure", table_cell_style), Paragraph("Have you or someone close to you ever clicked a fraudulent link, lost money, or received a threatening phone call?", table_cell_style)],
        [Paragraph("Q4", table_cell_bold), Paragraph("Heuristic", table_cell_style), Paragraph("When you suspect a message might be fake, what specific signs or clues do you check to make your decision?", table_cell_style)],
        [Paragraph("Q5", table_cell_bold), Paragraph("Social Support", table_cell_style), Paragraph("Whom do you ask for assistance when you feel confused or uncertain about a message?", table_cell_style)],
        [Paragraph("Q6", table_cell_bold), Paragraph("Emotional State", table_cell_style), Paragraph("What emotions do you experience when a message claims your account or power will be blocked tonight?", table_cell_style)],
        [Paragraph("Q7", table_cell_bold), Paragraph("Tool Awareness", table_cell_style), Paragraph("Have you ever used any website, software, or tool to verify whether a link or phone number is safe?", table_cell_style)],
        [Paragraph("Q8", table_cell_bold), Paragraph("Input Modality", table_cell_style), Paragraph("If a safety helper existed, would you prefer typing text, pasting a link, uploading a screenshot, or voice dictation?", table_cell_style)],
        [Paragraph("Q9", table_cell_bold), Paragraph("Explainability", table_cell_style), Paragraph("What kind of explanation helps you more: a technical score (e.g., 85% risk) or simple Marathi/Hindi instructions on what to do?", table_cell_style)],
        [Paragraph("Q10", table_cell_bold), Paragraph("Reporting", table_cell_style), Paragraph("Are you aware of the official National Cybercrime Helpline number (1930) or the cybercrime.gov.in reporting portal?", table_cell_style)]
    ]
    q_table = Table(q_data, colWidths=[30, 95, 398])
    q_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 1.8),
    ]))
    story.append(q_table)
    story.append(Spacer(1, 3))

    # Detailed Field Interviews (Clean reframed without location or device)
    story.append(Paragraph("Detailed Field Interview Findings (10 Field Respondents)", h2_style))

    interviews = [
        {
            "num": "1",
            "name": "Smt. Sunita Kulkarni",
            "age": "62",
            "occ": "Retired Primary School Teacher",
            "lang": "Marathi (Primary), Basic English",
            "scam": "Received an urgent SMS: 'Dear consumer, your electricity power will be disconnected at 9:30 PM by Mahavitaran officer. Call 9823xxxxxx'. Almost called because her husband was bedridden and needed medical equipment powered.",
            "obs": "User demonstrated smartphone navigation; struggled with small tap targets and deciphering English URL query parameters.",
            "q_ans": "Q1: 3-4 times a week. Q2: Broken English mixed with Marathi. Cannot read technical terms like 'phishing'. Q4: Checks if sender looks official. Q5: Consults her adult son for technical assistance. Q6: Extreme anxiety & panic. Q7: Never used any tool. Q8: 'Uploading a screenshot is easiest.' Q9: Strongly wants Marathi advice: 'Don't pay, bill is paid.' Q10: Unaware of 1930.",
            "hci_note": "Requires large fonts, high contrast, zero technical jargon, and screenshot OCR so she doesn't have to copy-paste URLs."
        },
        {
            "num": "2",
            "name": "Shri. Rameshwar Jadhav",
            "age": "48",
            "occ": "Sugarcane Farmer & Dairy Operator",
            "lang": "Marathi Only",
            "scam": "Received a WhatsApp message with photo of PM-Kisan scheme stating Rs. 6,000 subsidy released, click link to claim. Link asked for Aadhaar and bank OTP. Nephew intervened before he entered OTP.",
            "obs": "User holds phone in landscape mode occasionally; relies on voice notes on WhatsApp rather than typing Marathi keyboard.",
            "q_ans": "Q1: Daily on WhatsApp. Q2: Only reads Marathi Devanagari script. Q4: Cannot distinguish fake links; trusts forwarded govt logos. Q5: Village panchayat youth. Q6: Greed and hope, followed by fear of loss. Q7: No tools known. Q8: Screenshot upload or voice input. Q9: 'Tell me in Marathi if it is true or a cheat.' Q10: Never heard of 1930.",
            "hci_note": "Absolute necessity for pure Marathi UI, screenshot upload OCR, and explicit visual warning markers on fake government schemes."
        },
        {
            "num": "3",
            "name": "Shri. Prakash Shinde",
            "age": "39",
            "occ": "Kirana Merchant (General Store)",
            "lang": "Marathi, Hindi, Functional English",
            "scam": "Customer bought goods worth Rs. 850, showed fake payment success screenshot on phone, but no soundbox chime occurred. Customer claimed 'server issue' and fled. Also received reverse QR code fraud attempts.",
            "obs": "Interrupted multiple times by customers during inquiry; requires single-glance color indicators rather than reading paragraphs.",
            "q_ans": "Q1: Daily UPI queries. Q2: Hindi & Marathi. Q4: Always waits for soundbox notification or bank SMS alert. Q5: Fellow shopkeepers. Q6: Irritated & suspicious during rush hours. Q7: Truecaller only. Q8: 'Quick photo of message, app should tell me within 2 seconds.' Q9: Color-coded green/red badge. Q10: Vaguely heard of cyber police.",
            "hci_note": "Needs ultra-fast assessment (<2 seconds), prominent green/red visual color-coding, and plain explanation of reverse QR fraud."
        },
        {
            "num": "4",
            "name": "Smt. Mangal More",
            "age": "44",
            "occ": "Homemaker",
            "lang": "Marathi, Spoken Hindi",
            "scam": "Added to a Telegram group promising Rs. 150 for liking YouTube videos. Earned Rs. 450 initially, then asked to deposit Rs. 5,000 for VIP tasks. Lost Rs. 5,000 before realizing it was a Ponzi scam.",
            "obs": "Demonstrated extreme hesitation and shame when discussing financial loss; concealed incident from family.",
            "q_ans": "Q1: 2-3 scam messages weekly. Q2: Hindi & Marathi. Q4: Assumed initial payout proved legitimacy. Q5: Did not ask anyone due to fear of embarrassment. Q6: Initial excitement followed by deep distress and self-blame. Q7: None. Q8: Pasting text or screenshot. Q9: Reassuring message that fraud is not their fault. Q10: No awareness.",
            "hci_note": "Critical need for empathetic, non-judgmental risk communication; clear explanations that initial small payouts are classic bait tactics."
        },
        {
            "num": "5",
            "name": "Mr. Aniket Deshmukh",
            "age": "21",
            "occ": "B.E. Computer Engineering Student",
            "lang": "English, Marathi, Hindi",
            "scam": "Received an email masquerading as a campus placement cell requiring registration fee of Rs. 1,000 for an MNC interview drive. Domain was a spoofed variant of the college portal.",
            "obs": "Navigated effortlessly through web browsers; inspected SSL certificates manually once prompted.",
            "q_ans": "Q1: 5-10 phishing emails & spam calls weekly. Q2: Professional English. Q4: Checks sender domain and grammar. Q5: Tech-savvy peers and Reddit. Q6: Mild curiosity and annoyance. Q7: VirusTotal occasionally. Q8: Direct link paste or terminal query. Q9: Technical breakdown (SPF/DKIM/entropy). Q10: Fully aware of 1930 and portals.",
            "hci_note": "Supports progressive disclosure: show clean plain verdict first, but provide collapsible technical breakdown for advanced users."
        },
        {
            "num": "6",
            "name": "Shri. Dnyaneshwar Gaikwad",
            "age": "52",
            "occ": "Auto-Rickshaw Driver",
            "lang": "Marathi Only",
            "scam": "Received an SMS with traffic police e-challan alert: 'Pay fine Rs. 1,000 within 24 hours or vehicle license suspended'. APK download link disguised as official government mParivahan portal.",
            "obs": "Operating outdoors in bright sunlight; wears bifocal reading glasses; difficulty reading text on low-brightness screen.",
            "q_ans": "Q1: Receives challan and loan SMS weekly. Q2: Marathi only. Q4: Panic makes him ask passengers during transit operations. Q5: Fellow auto drivers at the stand. Q6: Severe terror of police action and license seizure. Q7: None. Q8: 'Read out the message to me' (Audio/TTS). Q9: Simple Marathi audio readout: 'Do not pay, this is a fake website.' Q10: Unaware of 1930.",
            "hci_note": "Major validation for Text-to-Speech (TTS) audio narration in Marathi, outdoor high-contrast themes, and anti-APK warnings."
        },
        {
            "num": "7",
            "name": "Ms. Priyanka Salunke",
            "age": "27",
            "occ": "IT Support Desk Analyst",
            "lang": "English, Marathi, Hindi",
            "scam": "Her elderly father received a call from someone posing as bank manager requesting urgent KYC update via AnyDesk app. Priyanka intervened mid-call when her father asked for OTP.",
            "obs": "Frequently assists elderly relatives remotely; acts as family 'cyber guardian'.",
            "q_ans": "Q1: Frequent spoof calls and parcel delivery scams. Q2: English, Hindi, Marathi. Q4: Verifies banking alerts through official banking apps directly. Q5: IT security colleagues. Q6: Protective anger on behalf of elderly parents. Q7: Truecaller, Google Safe Browsing. Q8: Quick screenshot forward from WhatsApp. Q9: Clear badge plus shareable summary to send back to parent. Q10: Aware of 1930.",
            "hci_note": "Identified the need for 'Share Warning with Family' button to empower tech-literate family guardians to protect elderly relatives."
        },
        {
            "num": "8",
            "name": "Shri. Vasantrao Joshi",
            "age": "71",
            "occ": "Retired State Govt Employee (Pensioner)",
            "lang": "Marathi, Good English",
            "scam": "Received phone call from an alleged 'CBI Officer from New Delhi' stating his Aadhaar was used in money laundering and he was under 'Digital Arrest'. Kept on Skype video call for 3 hours; saved when daughter arrived home.",
            "obs": "High cognitive fatigue after 15 minutes of mobile interaction; tremor in dominant hand makes precision tapping difficult.",
            "q_ans": "Q1: Several calls a month. Q2: Official Hindi and English. Q4: Authority intimidation overrides natural suspicion. Q5: Relies on daughter completely. Q6: Overwhelming terror, elevated blood pressure. Q7: None. Q8: Simple large questionnaire with Yes/No answers. Q9: Direct calm reassurance: 'Government agencies never arrest anyone over video call.' Q10: Vague awareness of police, terrified of approaching them.",
            "hci_note": "Justified the creation of the dedicated 10-Question Suspicious Phone Call Questionnaire with digital arrest warning."
        },
        {
            "num": "9",
            "name": "Smt. Rekha Kamble",
            "age": "36",
            "occ": "Primary School & Anganwadi Worker",
            "lang": "Marathi and Hindi",
            "scam": "Received SMS claiming a free smartphone and sewing machine under government women empowerment scheme, requiring Rs. 299 courier fee payment via a link. Link was a clone of a payment gateway.",
            "obs": "Active in several community self-help groups; receives numerous forwards containing unverified government scheme links.",
            "q_ans": "Q1: 4-5 times a week in community groups. Q2: Marathi. Q4: Asks the Anganwadi head. Q5: Female friends & Anganwadi supervisor. Q6: Curiosity and excitement. Q7: None. Q8: Upload screenshot from WhatsApp status or chat. Q9: Red danger badge with simple reason: 'Government never asks for courier fees via link.' Q10: Unaware of cybercrime portal.",
            "hci_note": "Reinforces that women community leaders need easily shareable verification cards to debunk viral misinformation in local groups."
        },
        {
            "num": "10",
            "name": "Mr. Sagar Patil",
            "age": "24",
            "occ": "Food Delivery Executive",
            "lang": "Marathi, Hindi, Conversational English",
            "scam": "Received a call claiming a customer wanted to pay an extra Rs. 500 tip via Google Pay, but sent a 'Pay' request instead of sending money. Sagar noticed the PIN screen and declined.",
            "obs": "Interacts with phone while wearing delivery helmet and gloves; needs large button targets and single-glance verdicts.",
            "q_ans": "Q1: Frequent fake customer calls and scam loan app SMS. Q2: Hindi & Marathi. Q4: Knows that receiving money never requires entering UPI PIN. Q5: Delivery partner communication groups. Q6: Wary and cautious. Q7: None. Q8: Screenshot or quick paste. Q9: Instant binary warning: 'Fraud / Safe'. Q10: Aware that cyber cell exists, but lacks exact procedure.",
            "hci_note": "Validates the core educational rule: 'Entering your UPI PIN always debits money, never credits it' (highlighted in ScamShield Learn Center)."
        }
    ]

    def make_interview_card(item):
        """Builds a clean, 2-column interview card with zero location or device references."""
        col1_elements = [
            Paragraph("<b>Real Scam Incident Encountered:</b>", card_field_title),
            Paragraph(item['scam'], card_field_body),
            Spacer(1, 2.5),
            Paragraph("<b>Contextual Inquiry Observation:</b>", card_field_title),
            Paragraph(item['obs'], card_field_body)
        ]

        col2_elements = [
            Paragraph("<b>Key Questionnaire Responses (Q1-Q10):</b>", card_field_title),
            Paragraph(item['q_ans'], card_field_body),
            Spacer(1, 2.5),
            Paragraph("<b>HCI &amp; Design Implication:</b>", card_field_title),
            Paragraph(item['hci_note'], card_field_body)
        ]

        # Clean header: Name, Age, Occ on left; Language on right. Zero location or device content.
        header_left = Paragraph(f"<b>Interview #{item['num']}: {item['name']}</b> ({item['age']} yrs, {item['occ']})", card_hdr_left)
        header_right = Paragraph(f"<b>Primary Language:</b> {item['lang']}", card_hdr_right)

        card_table = Table([
            [header_left, header_right],
            [col1_elements, col2_elements]
        ], colWidths=[260, 263])

        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('BACKGROUND', (0,1), (0,1), colors.white),
            ('BACKGROUND', (1,1), (1,1), colors.HexColor("#EFF6FF")),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 3.5),
        ]))
        return card_table

    # Add Interviews 1, 2, 3 to Page 2
    for item in interviews[:3]:
        story.append(KeepTogether(make_interview_card(item)))
        story.append(Spacer(1, 3))

    # =========================================================================
    # PAGE 3: INTERVIEWS #4, #5, #6, #7 (2-COLUMNS)
    # =========================================================================
    story.append(PageBreak())
    for item in interviews[3:7]:
        story.append(KeepTogether(make_interview_card(item)))
        story.append(Spacer(1, 6))

    # =========================================================================
    # PAGE 4: INTERVIEWS #8, #9, #10 & EMPIRICAL FIELD SYNTHESIS TABLE
    # =========================================================================
    story.append(PageBreak())
    for item in interviews[7:10]:
        story.append(KeepTogether(make_interview_card(item)))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 2))
    # Empirical Synthesis Table of 10 Interviews (Clean reframed without location references)
    story.append(Paragraph("Empirical Field Synthesis: Quantitative &amp; Qualitative Analysis (Field Study Cohort, N=10)", h2_style))
    synth_data = [
        [Paragraph("Empirical Metric / Dimension", table_header_style), Paragraph("Field Findings Across 10 Field Interviews", table_header_style), Paragraph("Direct ScamShield HCI Implementation", table_header_style)],
        [Paragraph("<b>Primary Language Literacy</b>", table_cell_bold), Paragraph("50% Marathi only, 30% Bilingual (Marathi/Hindi), 20% Multilingual. English technical jargon is widely misunderstood.", table_cell_style), Paragraph("Complete tri-lingual interface (EN/MR/HI) with localized Devanagari heuristics and native audio readout.", table_cell_style)],
        [Paragraph("<b>Predominant Scam Vectors</b>", table_cell_bold), Paragraph("40% electricity bill cut threats, 30% UPI reverse QR / fake screenshots, 20% fake govt subsidies, 10% coercive calls.", table_cell_style), Paragraph("Targeted pattern recognizers for utility billing, PhonePe/GPay spoofing, PM-Kisan, and Digital Arrest calls.", table_cell_style)],
        [Paragraph("<b>Emergency 1930 Awareness</b>", table_cell_bold), Paragraph("Only 20% knew of Helpline 1930. 80% felt helpless or feared approaching police stations after losing money.", table_cell_style), Paragraph("Dedicated Emergency Module with 1-click Dial 1930 and direct cybercrime.gov.in integration.", table_cell_style)],
        [Paragraph("<b>Preferred Input Modality</b>", table_cell_bold), Paragraph("70% prefer screenshot upload / OCR; 20% clipboard paste; only 10% isolate URLs. Voice dictation failed in noisy commercial markets.", table_cell_style), Paragraph("Dual-mode OCR screenshot analyzer and 1-click clipboard paste. Voice input was dropped based on ambient noise testing.", table_cell_style)],
        [Paragraph("<b>Emotional Response &amp; Panic</b>", table_cell_bold), Paragraph("80% of seniors &amp; homemakers experienced severe panic upon receiving disconnection/arrest threats; 0% could verify headers.", table_cell_style), Paragraph("Calibrated reassuring color badges (Green/Yellow/Red) with immediate plain-language regional action steps to eliminate panic.", table_cell_style)],
        [Paragraph("<b>Decision-Support Format</b>", table_cell_bold), Paragraph("90% found probabilistic scores confusing; demanded concrete 'What to do / What not to do' steps in regional languages.", table_cell_style), Paragraph("Two-part explainable cards: 'Why this score' + actionable prescriptive checklists.", table_cell_style)]
    ]
    synth_table = Table(synth_data, colWidths=[118, 201, 204])
    synth_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(KeepTogether(synth_table))

    # =========================================================================
    # PAGE 5: INTERVIEW PHOTOGRAPHS (CLEAN BLANK MOUNTING PAGE - NO BOXES)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("Interview Photographs", h1_style))
    story.append(Paragraph(
        "<b>Photographic Field Documentation &amp; Visual Consent Verification</b><br/>"
        "<i>Designated photographic documentation page for in-person contextual inquiry field interviews and visual consent verification. "
        "Original field photographs, contextual interview documentation, and signed participant consent records.</i>",
        body_style
    ))
    # Page 5 remains an elegant, clean, blank mounting page with NO blank boxes or frames.
    story.append(Spacer(1, 40))

    # =========================================================================
    # PAGE 6: SECTION 3: DETAILED USER PERSONAS (CLEAN REFRAMED)
    # (Page 6 from old PDF is completely deleted; old Page 7 now becomes Page 6!)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Detailed User Personas", h1_style))
    story.append(Paragraph(
        "Synthesizing field observations, behavioral tendencies, and questionnaire patterns, we constructed four primary personas representing "
        "distinct archetypes of digital vulnerability and technology adoption across regional demographic cohorts:",
        ParagraphStyle('P3Intro', parent=body_style, fontSize=7.8, leading=10.5)
    ))
    story.append(Spacer(1, 4))

    personas = [
        {
            "tag": "Persona 1: Sunita Kulkarni (The Anxious Pensioner) - Senior Citizen / Retired Educator",
            "quote": "\"I get terrified when an SMS says my light or bank will be cut. I don't understand English technical terms, and my son is busy at work.\"",
            "demo": "<b>Age:</b> 62 | <b>Household Context:</b> Semi-Urban Residential Household | <b>Education:</b> B.A., D.Ed. | <b>Language:</b> Marathi (Fluent), English (Basic)",
            "goals": "Safely manage daily pension, pay electricity &amp; utility bills online without falling victim to fraud or losing life savings.",
            "pains": "Fear of authority, small screen fonts, fear of clicking the wrong button, inability to parse disguised phishing URLs.",
            "hci": "High-contrast UI, Devanagari Marathi script, Screenshot OCR so she doesn't type URLs, Text-to-Speech audio readout."
        },
        {
            "tag": "Persona 2: Rameshwar Jadhav (The Semi-Literate Rural Farmer) - Peri-Urban Farmer & Dairy Operator",
            "quote": "\"If a message has a government emblem and offers farm subsidy, I believe it. But I cannot read English URLs.\"",
            "demo": "<b>Age:</b> 48 | <b>Regional Context:</b> Agrarian & Semi-Rural Community | <b>Education:</b> 8th Standard | <b>Language:</b> Marathi Only",
            "goals": "Access agricultural schemes, receive dairy payments via PhonePe, protect farm income from cyber syndicates.",
            "pains": "Total inability to read English; easily misled by official-looking government graphics; low typing speed.",
            "hci": "Screenshot OCR, prominent warning icons (Shield vs Warning), simple Marathi affirmative actions ('Do not click')."
        },
        {
            "tag": "Persona 3: Prakash Shinde (The Busy Kirana Merchant) - Small Business Owner / Retailer",
            "quote": "\"During evening rush, customers flash fake payment screens. I need an instant 2-second check before they walk out.\"",
            "demo": "<b>Age:</b> 39 | <b>Commerce Context:</b> High-Volume Commercial Retail Corridor | <b>Education:</b> 12th Commerce | <b>Language:</b> Marathi, Hindi, Functional English",
            "goals": "Prevent revenue loss from fake payment screenshots, reverse QR frauds, and fake supplier banking links.",
            "pains": "Extreme time pressure during store hours, cognitive distraction, lack of formal cybersecurity training.",
            "hci": "Sub-2-second evaluation response, clear color-coded risk meter (Green/Yellow/Red), offline awareness cards."
        },
        {
            "tag": "Persona 4: Aniket Deshmukh (The Overconfident Digital Native) - Engineering Student / Young Professional",
            "quote": "\"I thought I knew everything about phishing until I almost gave away my debit card CVV for a campus stipend registration.\"",
            "demo": "<b>Age:</b> 21 | <b>Academic Context:</b> University Engineering Campus | <b>Education:</b> B.E. Ongoing | <b>Language:</b> English, Marathi, Hindi",
            "goals": "Find internships, work-from-home gigs, and gadget deals without leaking credentials or malware.",
            "pains": "Sophisticated clone portals, urgency triggers disguised as MNC recruiters, FOMO (Fear Of Missing Out).",
            "hci": "Progressive disclosure: instant plain verdict upfront with expandable heuristic breakdowns and 'Share with Family' button."
        }
    ]

    p_card_title = ParagraphStyle('PCT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.0, leading=10.2, textColor=colors.white)
    p_quote_style = ParagraphStyle('PQ', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.2, leading=9.2, textColor=colors.HexColor("#1E3A8A"))
    p_body_style = ParagraphStyle('PB', parent=styles['Normal'], fontName='Helvetica', fontSize=7.0, leading=9.0, textColor=dark_neutral)

    for p in personas:
        p_data = [
            [Paragraph(f"<b>{p['tag']}</b>", p_card_title)],
            [Paragraph(p['quote'], p_quote_style)],
            [Paragraph(f"<b>Demographics:</b> {p['demo']}", p_body_style)],
            [Paragraph(f"<b>Goals &amp; Motivations:</b> {p['goals']}", p_body_style)],
            [Paragraph(f"<b>Frustrations &amp; Pains:</b> {p['pains']}", p_body_style)],
            [Paragraph(f"<b>HCI Requirements:</b> {p['hci']}", p_body_style)],
        ]
        p_table = Table(p_data, colWidths=[523])
        p_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#EFF6FF")),
            ('BACKGROUND', (0,2), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 2.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(KeepTogether(p_table))
        story.append(Spacer(1, 4))

    # =========================================================================
    # PAGE 7: SECTION 4 & SECTION 5: LITERATURE REVIEW & RESEARCH GAPS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Explore Related Work Literature (Minimum 5 Papers)", h1_style))
    story.append(Paragraph(
        "A rigorous review of five foundational peer-reviewed papers across HCI, cybersecurity warning design, and phishing detection "
        "was conducted to benchmark current state-of-the-art systems and identify critical gaps:",
        body_style
    ))
    story.append(Spacer(1, 2))

    lit_data = [
        [
            Paragraph("Paper Citation &amp; Focus", table_header_style),
            Paragraph("Core Methodology", table_header_style),
            Paragraph("Key Findings &amp; Reusable Insights", table_header_style),
            Paragraph("Critical Limitations &amp;<br/>Unaddressed Gaps", table_header_style)
        ],
        [
            Paragraph("<b>[1] Sheng et al. (2010)</b><br/>'Who Falls for Phish? A Demographic Analysis of Phishing Susceptibility'<br/><i>ACM CHI Conference</i>", table_cell_style),
            Paragraph("Role-play phishing experiment with 1,001 participants measuring age, gender, education, and technical background.", table_cell_style),
            Paragraph("Women, younger users (18-25), and elderly (60+) were significantly more susceptible. Contextual cues are far more effective than abstract warnings.", table_cell_style),
            Paragraph("Conducted in North America; assumed high English literacy. Ignored multilingual and regional script nuances prevalent in India.", table_cell_style)
        ],
        [
            Paragraph("<b>[2] Egelman &amp; Peer (2015)</b><br/>'Scaling the Security Wall: Measuring Security Attitudes &amp; Behaviors'<br/><i>USENIX SOUPS</i>", table_cell_style),
            Paragraph("Psychometric scale validation (SA-6) evaluating cognitive friction, habituation, and warning fatigue in end users.", table_cell_style),
            Paragraph("Users habitually bypass security dialogs when they are intrusive, verbose, or lack immediate alternative safe actions.", table_cell_style),
            Paragraph("Focused on desktop browser popups; does not address mobile messaging apps (WhatsApp/SMS) where 85%+ of Indian scams originate.", table_cell_style)
        ],
        [
            Paragraph("<b>[3] Alsharnouby et al. (2015)</b><br/>'Phishing Detection with Eye-Tracking: Do Users Look at the Address Bar?'<br/><i>Computers &amp; Security</i>", table_cell_style),
            Paragraph("Eye-tracking laboratory study with 60 participants browsing legitimate and spoofed financial web pages.", table_cell_style),
            Paragraph("Over 91% of non-technical participants never fixate on the URL address bar or SSL lock, relying solely on page logos and visual brand styling.", table_cell_style),
            Paragraph("Demonstrates that users cannot be expected to manually inspect URLs; automated screenshot OCR and domain decomposition are essential.", table_cell_style)
        ],
        [
            Paragraph("<b>[4] Gupta et al. (2018)</b><br/>'Defending Against Phishing Attacks: Taxonomy of Methods &amp; Directions'<br/><i>Telecommunication Systems</i>", table_cell_style),
            Paragraph("Systematic taxonomy comparing heuristic rule-based systems, blacklists, machine learning classifiers, and visual similarity.", table_cell_style),
            Paragraph("Hybrid architectures combining heuristic feature extraction with lightweight ML yield the highest accuracy and lowest false-positive rates.", table_cell_style),
            Paragraph("Blacklists fail completely against zero-day short-lived URLs (lifespan &lt; 4 hours). Hybrid heuristic engines are essential for immediate verdict.", table_cell_style)
        ],
        [
            Paragraph("<b>[5] Biddle et al. (2020)</b><br/>'Towards Understandable Cybersecurity Warnings: Designing for Actionability'<br/><i>HCI-Sec</i>", table_cell_style),
            Paragraph("User experience evaluation of 12 cybersecurity tools assessing comprehension of risk scores and post-verdict user actions.", table_cell_style),
            Paragraph("Probabilistic scores (e.g., 'Risk: 78%') induce cognitive paralysis. Effective warnings must give direct prescriptive action checklists ('Do this, Don't do that').", table_cell_style),
            Paragraph("Did not incorporate emergency legal/financial escalation pathways (e.g., how to contact bank or national cyber police during critical golden hours).", table_cell_style)
        ]
    ]
    lit_table = Table(lit_data, colWidths=[120, 120, 148, 135])
    lit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(KeepTogether(lit_table))
    story.append(Spacer(1, 4))

    # Section 5: Identification of Research Gaps
    story.append(Paragraph("5. Identification of Research Gaps &amp; ScamShield Novelty", h1_style))
    story.append(Paragraph(
        "Correlating our empirical field interviews with academic literature revealed five glaring research and engineering gaps:",
        body_style
    ))
    story.append(Spacer(1, 2))

    gaps_data = [
        [
            Paragraph("Identified Gap", table_header_style),
            Paragraph("Current State in Existing Tools", table_header_style),
            Paragraph("Consequence on Vulnerable Regional Users", table_header_style),
            Paragraph("How ScamShield Solves It", table_header_style)
        ],
        [
            Paragraph("<b>Gap 1: Linguistic Exclusion</b>", table_cell_bold),
            Paragraph("Tools like VirusTotal, Chrome Safe Browsing operate exclusively in English.", table_cell_style),
            Paragraph("Farmers, homemakers, and senior citizens across non-English speaking communities cannot understand warnings or explanations.", table_cell_style),
            Paragraph("Full tri-lingual support (English, Marathi, Hindi) across UI, heuristics, reasons, and actions.", table_cell_style)
        ],
        [
            Paragraph("<b>Gap 2: Jargon vs Actionability</b>", table_cell_bold),
            Paragraph("Display abstract heuristic numbers, probability graphs, or CVE codes.", table_cell_style),
            Paragraph("Users experience cognitive overload, panic, or dismiss warnings entirely.", table_cell_style),
            Paragraph("Plain-language verdicts with a two-part structured checklist: 'Why is this dangerous' &amp; 'What to do now'.", table_cell_style)
        ],
        [
            Paragraph("<b>Gap 3: Input Friction on Mobile</b>", table_cell_bold),
            Paragraph("Tools require manually copying and pasting web links into a browser.", table_cell_style),
            Paragraph("Elderly and non-technical users cannot isolate URLs from SMS or WhatsApp chats.", table_cell_style),
            Paragraph("Dual-mode OCR Screenshot upload (drag/drop) and 1-click clipboard paste.", table_cell_style)
        ],
        [
            Paragraph("<b>Gap 4: Lack of Phone Call Analysis</b>", table_cell_bold),
            Paragraph("Scam tools only check URLs or email headers; ignore social engineering phone calls.", table_cell_style),
            Paragraph("Digital arrest, CBI impersonation, and AnyDesk pension scams bypass link checkers.", table_cell_style),
            Paragraph("10-question phone call interactive risk assessor targeting coercive urgency and remote access tricks.", table_cell_style)
        ],
        [
            Paragraph("<b>Gap 5: Disconnect from Law Enforcement</b>", table_cell_bold),
            Paragraph("Tools provide a score but abandon the user if they have already transferred money.", table_cell_style),
            Paragraph("Victims miss the 24-hour 'Golden Hour' to freeze money via Indian Cybercrime Helpline.", table_cell_style),
            Paragraph("Dedicated Emergency Report module with 1-click Dial 1930 and direct cybercrime.gov.in integration.", table_cell_style)
        ]
    ]
    gaps_table = Table(gaps_data, colWidths=[105, 125, 143, 150])
    gaps_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(KeepTogether(gaps_table))

    # =========================================================================
    # PAGE 8: SECTION 6: WORKING PROTOTYPE ARCHITECTURE & WIREFRAMES
    # (High-resolution wireframe blueprints preserved with verification table)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Working Prototype Architecture &amp; Wireframes", h1_style))
    story.append(Paragraph(
        "<b>System Architecture Overview:</b> ScamShield is built on a responsive Flask/Python architecture containerized with Docker. "
        "The backend combines a high-precision Heuristic Rule Engine (Devanagari + English regex for OTP theft, financial demands, urgency, prizes), "
        "tri-modal Machine Learning models (FeatureUnion Word+Char-wb Logistic Regression for SMS [99.19% acc], Subject-Boosted Logistic Regression for Email [98.22% acc], "
        "and 22-feature Random Forest on 40,000 samples with Shannon entropy for URLs [99.05% acc]), and an OCR vision pipeline (Tesseract + OpenCV) "
        "with client-side privacy auto-masking (Aadhaar, PAN, UPI, cards). Below are the screen wireframe blueprints and empirical test results:",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("Information Architecture &amp; Screen Wireframe Blueprints", h2_style))
    story.append(Paragraph(
        "<i>Figure 8. Seven low-fidelity wireframe blueprints: home dashboard, SMS/WhatsApp checker, URL/QR checker, email checker, "
        "phone-call questionnaire, scam assessment result, and scam-awareness learning center.</i>",
        ParagraphStyle('FigCap', parent=body_style, fontSize=7.0, leading=9.0, textColor=colors.HexColor("#475569"))
    ))
    story.append(Spacer(1, 3))

    if os.path.exists("p9_wireframe.png"):
        story.append(Image("p9_wireframe.png", width=519, height=315))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Prototype Verification &amp; Engineering Test Results", h2_style))
    proto_verif_data = [
        [
            Paragraph("Module Tested", table_header_style),
            Paragraph("Test Scope &amp; Target", table_header_style),
            Paragraph("Sample Input Evaluated", table_header_style),
            Paragraph("Outcome", table_header_style)
        ],
        [
            Paragraph("<b>Privacy Auto-Masking</b>", table_cell_bold),
            Paragraph("Credit cards, CVVs, OTPs", table_cell_style),
            Paragraph("Sample message containing card, CVV, and OTP fields", table_cell_style),
            Paragraph("<b>PASS</b> - sensitive values masked before transmission", table_cell_style)
        ],
        [
            Paragraph("<b>Regional Heuristics</b>", table_cell_bold),
            Paragraph("Marathi electricity scam", table_cell_style),
            Paragraph("Marathi electricity-disconnection alert", table_cell_style),
            Paragraph("<b>PASS</b> - high-risk score and localized action checklist", table_cell_style)
        ],
        [
            Paragraph("<b>OCR Screenshot Engine</b>", table_cell_bold),
            Paragraph("SMS image screenshot", table_cell_style),
            Paragraph("Uploaded bank KYC suspension notice", table_cell_style),
            Paragraph("<b>PASS</b> - text extracted and suspicious URL identified", table_cell_style)
        ],
        [
            Paragraph("<b>Data Portability</b>", table_cell_bold),
            Paragraph("CSV session export", table_cell_style),
            Paragraph("History export route", table_cell_style),
            Paragraph("<b>PASS</b> - valid CSV with timestamps and verdicts", table_cell_style)
        ],
        [
            Paragraph("<b>Continuous Evaluation</b>", table_cell_bold),
            Paragraph("Automated test suite", table_cell_style),
            Paragraph("56 unit and integration test cases (as stated in assignment)", table_cell_style),
            Paragraph("<b>PASS</b> - 56/56; SMS 99.19%, URL 99.05% (assignment-reported metrics)", table_cell_style)
        ]
    ]
    proto_verif_table = Table(proto_verif_data, colWidths=[110, 115, 160, 138])
    proto_verif_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(KeepTogether(proto_verif_table))

    # =========================================================================
    # PAGE 9: SECTION 7: ACADEMIC PROJECT POSTER PRESENTATION LAYOUT
    # (High-resolution academic poster presentation layout preserved)
    # =========================================================================
    story.append(PageBreak())
    poster_title_style = ParagraphStyle(
        'PosterTitleStyle',
        parent=h1_style,
        spaceBefore=0,
        spaceAfter=2,
        keepWithNext=True
    )
    story.append(Paragraph("7. Academic Project Poster Presentation Layout", poster_title_style))

    if os.path.exists("p10_poster.png"):
        story.append(Image("p10_poster.png", width=425, height=700))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS! Cleanly generated '{filename}'.")

if __name__ == "__main__":
    build_submission_pdf("Submission PDF.pdf")
