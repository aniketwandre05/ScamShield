"""
build_full_hci_docx.py
Generates ScamShield_HCI_Master_Evaluation_Guide.docx with complete academic depth,
high-resolution embedded wireframes, tables, callouts, and 25 Viva Voce answers.
"""

import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_doc():
    doc = docx.Document()
    
    # 1 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer setup
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("ScamShield — Human-Computer Interaction (HCI) Master Evaluation Guide")
        format_run(hrun, font_name="Segoe UI", size=8.5, italic=True, color_rgb=(0x71, 0x80, 0x96))
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("ScamShield HCI Project Viva Voce & Laboratory Evaluation Dossier  |  Department of Computer Engineering")
        format_run(frun, font_name="Segoe UI", size=8.5, color_rgb=(0x71, 0x80, 0x96))

    return doc

def format_run(run, font_name="Segoe UI", size=10.0, bold=False, italic=False, color_rgb=(0x2D, 0x37, 0x48)):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = RGBColor(*color_rgb)

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    for child in list(tc_pr):
        if child.tag.endswith('shd'):
            tc_pr.remove(child)
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    tc_pr.append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CBD5E0", size="4"):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    border_dict = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_val in border_dict.items():
        if b_val != "none":
            b_el = OxmlElement(f'w:{b_name}')
            b_el.set(qn('w:val'), b_val)
            b_el.set(qn('w:sz'), size)
            b_el.set(qn('w:space'), '0')
            b_el.set(qn('w:color'), color)
            tc_borders.append(b_el)
        else:
            b_el = OxmlElement(f'w:{b_name}')
            b_el.set(qn('w:val'), 'none')
            tc_borders.append(b_el)
    tc_pr.append(tc_borders)

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(20)
    h.paragraph_format.space_after = Pt(8)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    format_run(run, font_name="Segoe UI Semibold", size=15.5, bold=True, color_rgb=(0x1B, 0x36, 0x5D))
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    format_run(run, font_name="Segoe UI Semibold", size=13, bold=True, color_rgb=(0x2C, 0x52, 0x82))
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    format_run(run, font_name="Segoe UI Semibold", size=11, bold=True, color_rgb=(0x2B, 0x6C, 0xB0))
    return h

def add_body_p(doc, text="", space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        format_run(run, font_name="Segoe UI", size=10, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, font_name="Segoe UI", size=10, bold=True, color_rgb=(0x1A, 0x20, 0x2C))
    
    r_body = p.add_run(text)
    format_run(r_body, font_name="Segoe UI", size=10, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_callout(doc, text, title=None, border_color="2B6CB0", bg_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=140)
    set_cell_borders(cell, left="single", color=border_color, size="24")
    cell.width = Inches(6.5)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15

    if title:
        run_title = p.add_run(f"📌 {title}\n")
        format_run(run_title, font_name="Segoe UI Semibold", size=10, bold=True, color_rgb=(0x1B, 0x36, 0x5D))

    run_text = p.add_run(text)
    format_run(run_text, font_name="Segoe UI", size=9.5, color_rgb=(0x2D, 0x37, 0x48))

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def add_viva_qa(doc, q_num, question, answer):
    qp = doc.add_paragraph()
    qp.paragraph_format.space_before = Pt(12)
    qp.paragraph_format.space_after = Pt(4)
    qp.paragraph_format.keep_with_next = True

    q_badge = qp.add_run(f"Q{q_num}: ")
    format_run(q_badge, font_name="Segoe UI Semibold", size=10.5, bold=True, color_rgb=(0x1B, 0x36, 0x5D))
    
    q_text = qp.add_run(f'"{question}"')
    format_run(q_text, font_name="Segoe UI Semibold", size=10.5, bold=True, color_rgb=(0x2D, 0x37, 0x48))

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F7FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=140)
    set_cell_borders(cell, left="single", color="3182CE", size="18")
    cell.width = Inches(6.5)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15

    ans_title = p.add_run("🎓 Flawless Academic Model Answer:\n")
    format_run(ans_title, font_name="Segoe UI Semibold", size=9.5, bold=True, color_rgb=(0x2C, 0x52, 0x82))

    ans_body = p.add_run(answer)
    format_run(ans_body, font_name="Segoe UI", size=9.5, color_rgb=(0x1A, 0x20, 0x2C))

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def build_cover_page(doc):
    # Top spacing
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(36)
    tp.paragraph_format.space_after = Pt(12)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("SCAMSHIELD")
    format_run(r_title, font_name="Segoe UI", size=32, bold=True, color_rgb=(0x1B, 0x36, 0x5D))

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("Complete End-to-End Human-Computer Interaction (HCI) Master Evaluation Guide & Oral Viva Voce Defense Dossier")
    format_run(r_sub, font_name="Segoe UI", size=14, bold=False, color_rgb=(0x4A, 0x55, 0x68))

    # Accent decorative rule
    tbl_line = doc.add_table(rows=1, cols=1)
    tbl_line.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl_line.cell(0, 0)
    set_cell_background(c, "3182CE")
    c.width = Inches(6.5)
    tbl_line.rows[0].height = Pt(4)

    # Overview text
    add_body_p(doc, space_after=18)
    p_desc = add_body_p(doc, space_after=24)
    r_desc = p_desc.add_run(
        "A rigorous, academic-grade specification documenting every user interface, interactive micro-interaction, "
        "multimodal input pipeline, accessibility override, cognitive ergonomic law, and heuristic evaluation criterion "
        "implemented within the ScamShield platform. Cross-referenced from 0 to End across Jakob Nielsen's 10 Usability Heuristics, "
        "Ben Shneiderman's 8 Golden Rules, Don Norman's Interaction Design Principles, WCAG 2.2 Level AA/AAA, ISO 9241-110, "
        "and Explainable AI (XAI) Trust Calibration."
    )
    format_run(r_desc, font_name="Segoe UI", size=10.5, italic=False, color_rgb=(0x2D, 0x37, 0x48))

    # Metadata Box Table
    meta_tbl = doc.add_table(rows=7, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(2.2), Inches(4.3)]
    
    meta_data = [
        ("Project Name", "ScamShield: Multimodal Scam & Phishing Detection Platform"),
        ("Evaluation Topic", "Human-Computer Interaction (HCI) Laboratory Viva Voce"),
        ("Theoretical Scope", "Nielsen's 10 Heuristics, Shneiderman's 8 Rules, Norman's Principles, Cognitive Laws"),
        ("Accessibility Standards", "WCAG 2.2 Level AA/AAA, ISO 9241-110 Dialogue Principles, Section 508"),
        ("Multilingual Capabilities", "Trilingual Engine: English, Marathi (मराठी), Hindi (हिन्दी)"),
        ("System Architecture", "Python 3.14, Flask, scikit-learn ML, Tesseract OCR, pyzbar QR Engine"),
        ("Dossier Status", "Production Final — 100% Automated Test Pass (77/77 Tests, 28/28 Workflows)")
    ]

    for row_idx, (label, val) in enumerate(meta_data):
        row = meta_tbl.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = col_widths[0], col_widths[1]
        
        bg_col = "F0F4F8" if row_idx % 2 == 0 else "FFFFFF"
        set_cell_background(c0, bg_col)
        set_cell_background(c1, bg_col)
        set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
        set_cell_borders(c0, top="single", bottom="single", left="none", right="none", color="CBD5E0", size="4")
        set_cell_borders(c1, top="single", bottom="single", left="none", right="none", color="CBD5E0", size="4")

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        format_run(r0, font_name="Segoe UI Semibold", size=9.5, bold=True, color_rgb=(0x1B, 0x36, 0x5D))

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        format_run(r1, font_name="Segoe UI", size=9.5, color_rgb=(0x2D, 0x37, 0x48))

    doc.add_page_break()

def build_executive_summary(doc):
    add_heading_1(doc, "Executive Summary & System Philosophy")
    
    add_body_p(doc, 
        "ScamShield is an open, human-centered cyber-defense platform architected specifically to shield vulnerable digital citizens—"
        "including senior citizens, first-time internet users, and vernacular language speakers—from sophisticated multimodal fraud. "
        "Modern cybercrime rarely relies on brute-force technical penetration; rather, it exploits cognitive blind spots, acute financial panic, "
        "authority intimidation, and urgency cues (e.g., electricity disconnection threats, frozen bank accounts, quishing QR code traps)."
    )

    add_callout(doc,
        "Human-Computer Interaction (HCI) is not merely visual styling; it is the structural cognitive safeguard between a panicked user "
        "and a catastrophic financial loss. In high-stress scenarios, human working memory degrades to fewer than 4 chunks, motor coordination "
        "is impaired, and panic induces severe tunnel vision. ScamShield's interface is engineered specifically to eliminate friction, "
        "counteract manipulation biases, and provide calm, authoritative psychological closure.",
        title="Core HCI Design Philosophy"
    )

    add_heading_2(doc, "The Five HCI Pillars of ScamShield")
    
    pillars = [
        ("1. Zero Cognitive Frustration & Hick-Hyman Triage", 
         "The landing interface eliminates menu hierarchies by structuring all threats into exactly 4 primary channels (SMS, Email, URL/QR, Phone). Users select their channel in less than 2 seconds with zero navigation fatigue."),
        
        ("2. Multimodal Input Affordances (Text vs. Screenshot OCR & QR)", 
         "Recognizing that elderly or non-tech-savvy users struggle to copy-paste URLs or retype SMS messages, ScamShield accepts raw screenshots. Our OpenCV pipeline automatically detects and decodes QR codes ('Quishing') while Tesseract extracts text patterns, democratizing cybersecurity for users who cannot type."),
        
        ("3. Calibrated Trust & Explainable AI (XAI)", 
         "Unlike black-box systems that spit out arbitrary threat scores, ScamShield provides multi-layered feature attribution. Suspicious keywords are highlighted in context (<mark>), specific rule triggers are explained in plain English, Hindi, and Marathi, and benign content is classified as 'Potentially Safe' rather than '100% Safe' to prevent automation complacency."),
        
        ("4. WCAG 2.2 Redundant Non-Color-Alone Risk Encoding", 
         "To ensure absolute accessibility for color-blind users (Deuteranopia, Protanopia) and monochromatic displays, risk states are never communicated via color alone. High, Medium, and Low risk levels are multi-coded across numerical scores, plain-language text badges, distinct iconography, and geometric border patterns (Solid, Dashed, Double-border)."),
        
        ("5. Resilient Error Recovery & Zero Dead-End Architecture", 
         "Error screens eliminate blame and technical HTTP codes. Every exception provides empathetic plain-language diagnoses, dynamic return paths to the prior form, and a persistent 4-channel recovery navigation bar ensuring the user is never stranded.")
    ]

    for p_title, p_desc in pillars:
        add_bullet_p(doc, f"{p_title}: ", p_desc)

def build_chapter_1(doc):
    add_heading_1(doc, "CHAPTER 1: Master HCI Frameworks & Theoretical Foundations")
    
    add_body_p(doc, 
        "This chapter establishes the rigorous academic and theoretical foundations that govern every user interface decision across ScamShield. "
        "It provides the precise theoretical justifications expected by academic evaluators, university professors, and usability auditors."
    )

    # 1.1 Nielsen's 10 Usability Heuristics
    add_heading_2(doc, "1.1 Jakob Nielsen's 10 Usability Heuristics in ScamShield")
    
    heuristics = [
        ("H1: Visibility of System Status", 
         "The system always keeps users informed about what is happening through appropriate feedback within reasonable time. In ScamShield, when a user submits content, an immediate full-screen loading overlay (#loading-overlay) activates with a pulsating spinner and plain-language micro-copy ('Inspecting text patterns, urgency signals, and security risks...'). During multi-step phone surveys, a dynamic progress bar fills proportionally (0% to 100%) with real-time percentage text."),
        
        ("H2: Match Between System and the Real World", 
         "The system speaks the user's language with words, phrases, and concepts familiar to the user rather than system-oriented terms. ScamShield eliminates internal ML jargon like 'TF-IDF Vectorizer', 'Multinomial Naive Bayes', and 'Cosine Similarity'. Instead, it presents verdicts using plain concepts like 'Suspicious message', 'Check URL', and 'Safe'. Crucially, the entire interface is localized into Hindi and Marathi via translations.py, aligning with local mental models."),
        
        ("H3: User Control and Freedom", 
         "Users often choose system functions by mistake and need a clearly marked 'emergency exit' to leave the unwanted state. ScamShield implements universal breadcrumbs ('← Back to Scanner'), an accessible Skip-to-Content anchor (#main-content), and a dedicated cancel button in every modal dialog. The Scan History table features a two-step confirmation modal with keyboard Escape dismissal, protecting users from accidental data erasure."),
        
        ("H4: Consistency and Standards", 
         "Users should not have to wonder whether different words, situations, or actions mean the same thing. ScamShield follows strict external web conventions: the primary brand logo resides at top-left linking to Home, navigation links occupy the top-right, and utility controls (Theme, Language, Font Size) are anchored in a dedicated utility bar. Across all 4 scanners, the primary CTA is consistently styled with .btn-primary and anchored at the bottom of the input card."),
        
        ("H5: Error Prevention", 
         "A careful design that prevents a problem from occurring in the first place is far superior to good error messages. ScamShield validates inputs on two tiers: client-side HTML5 constraints (required, accept='.png,.jpg,.jpeg') prevent empty or binary file submissions, while server-side normalizers in app.py sanitize malformed URLs (e.g., prepending https:// if missing) rather than crashing with a 400 Bad Request."),
        
        ("H6: Recognition Rather Than Recall", 
         "Minimize the user's memory load by making objects, actions, and options visible. The user should not have to remember information from one part of the dialogue to another. ScamShield provides preset clickable sample chips ('Electricity Bill Scam', 'Legitimate Bank Alert', 'Safe University URL') on every input screen. Novice users can test realistic threat patterns without recalling or searching for live malicious messages."),
        
        ("H7: Flexibility and Efficiency of Use", 
         "Accelerators—unseen by the novice user—often speed up the interaction for the expert user. ScamShield provides keyboard hotkeys ([1] for SMS, [2] for Email, [3] for URL/QR, [4] for Phone) on the dashboard. It also features one-click clipboard 'Paste' and 'Clear' buttons, drag-and-drop file zones, and direct CSV audit downloads for cybercrime reporting."),
        
        ("H8: Aesthetic and Minimalist Design", 
         "Dialogues should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with the relevant units of information. ScamShield uses a clean, high-contrast greyscale/slate visual palette, generous whitespace, clear typographic hierarchy, and zero redundant text or duplicate emoji decorations. Result screens utilize an accordion to tuck away secondary telemetry until requested."),
        
        ("H9: Help Users Recognize, Diagnose, and Recover from Errors", 
         "Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution. When a user uploads a blurry image that Tesseract OCR cannot parse, ScamShield displays an empathetic banner: 'Could Not Read Screenshot... The text in this image was too blurry or obscured to extract. Please paste the text directly or upload a higher-resolution image', paired with a '🔄 Try Again' shortcut."),
        
        ("H10: Help and Documentation", 
         "Even though it is better if the system can be used without documentation, it may be necessary to provide help. ScamShield features a dedicated Scam Awareness & Learning Center (/learn) containing threat taxonomies, an interactive safety quiz, and direct guidance on reporting fraud to India's National Cybercrime Helpline (1930).")
    ]

    for h_name, h_desc in heuristics:
        add_bullet_p(doc, f"{h_name}: ", h_desc)

    # 1.2 Shneiderman's 8 Golden Rules
    add_heading_2(doc, "1.2 Ben Shneiderman's 8 Golden Rules of Interface Design")
    
    rules = [
        ("Rule 1: Strive for Consistency", "Identical terminology, color palettes, button hierarchies, and card layouts across all modules."),
        ("Rule 2: Cater to Universal Usability", "Trilingual engine, font resizer (A-, A, A+), OpenDyslexic font, High Contrast mode, and keyboard shortcuts."),
        ("Rule 3: Offer Informative Feedback", "Analyzing spinner on submission, interactive hover states, dynamic progress bars, and toast alert confirmations."),
        ("Rule 4: Design Dialogs to Yield Closure", "Clear, conclusive Task Closure Banner at the top of results announcing 'Scan Complete' and removing ambiguity."),
        ("Rule 5: Prevent Errors", "File MIME filtering, schema auto-normalization, and destructive action modals."),
        ("Rule 6: Permit Easy Reversal of Actions", "Modal cancellation, clear input buttons, and frictionless 'Back to Scanner' breadcrumbs."),
        ("Rule 7: Support Internal Locus of Control", "Users initiate all scans, toggle options freely, control speech playback, and export or delete their history at will."),
        ("Rule 8: Reduce Short-Term Memory Load", "Phone questionnaire chunked into 5 questions per section; preset sample chips eliminate the need to memorize scam patterns.")
    ]

    for r_title, r_desc in rules:
        add_bullet_p(doc, f"{r_title}: ", r_desc)

    # 1.3 Don Norman's Interaction Design Principles
    add_heading_2(doc, "1.3 Don Norman's Design Principles & Cognitive Engineering")
    
    norman_points = [
        ("Affordances & Signifiers", 
         "An affordance is what an object can do; a signifier is the perceptible signal indicating that affordance. In ScamShield, buttons have drop shadows and distinct borders indicating clickability; dashed border upload zones visually signify drag-and-drop targets; the font size buttons [A-] [A] [A+] explicitly signify typography scaling."),
        
        ("Natural Mapping", 
         "Controls are mapped logically to user expectations. The font scaler places reduction [A-] on the left, normal [A] in the middle, and enlargement [A+] on the right, matching spatial mental models. In the Phone survey, 'Yes' and 'No' radio buttons follow standard spatial order."),
        
        ("Feedback Loops", 
         "Every user interaction triggers an immediate sensory acknowledgement: hovering elevates cards, clicking buttons switches active states, copying links displays a floating toast confirmation, and clicking 'Read Aloud' changes the icon to a pulsating stop indicator."),
        
        ("Physical & Semantic Constraints", 
         "File inputs are constrained strictly to image MIME types (.png, .jpg, .jpeg, .webp), preventing invalid file uploads. Input textareas enforce a 5,000-character upper bound to prevent buffer degradation."),
        
        ("Conceptual Models (System Image vs. Mental Model)", 
         "The user's mental model assumes a cybersecurity scanner inspects incoming messages for threats. ScamShield's system image matches this model exactly: input message → analyzing overlay → gauge score → explanation → immediate directive.")
    ]

    for np_title, np_desc in norman_points:
        add_bullet_p(doc, f"{np_title}: ", np_desc)

    # 1.4 Cognitive Psychology & Ergonomic Laws
    add_heading_2(doc, "1.4 Cognitive Psychology & Ergonomic Laws")
    
    cog_laws = [
        ("Fitts's Law: T = a + b * log2(2D / W)", 
         "The time to acquire a target is a function of distance (D) and target width (W). In ScamShield, all interactive tap targets strictly exceed the 44px x 44px WCAG minimum. On mobile viewports, the primary 'Check Safety' button expands to 100% container width, maximizing W so thumb acquisition time approaches zero."),
        
        ("Hick-Hyman Law: T = b * log2(n + 1)", 
         "Cognitive decision time increases logarithmically with the number of choices (n). On the Home dashboard, ScamShield restricts primary triage to exactly n = 4 mutually exclusive threat channels, reducing cognitive deliberation time to ~2 bits. In the phone questionnaire, complex fraud indicators are broken down into binary Yes/No choices (n = 2)."),
        
        ("Miller's Law: 7 +/- 2 Working Memory Chunks", 
         "Human short-term memory can retain only 5 to 9 information chunks. When a user has just experienced an extortion phone call, cognitive capacity is severely impaired. ScamShield chunks its 10-question survey into Part 1 (5 banking questions) and Part 2 (5 impersonation questions), preventing cognitive overload."),
        
        ("Jakob's Law of Internet User Experience", 
         "Users spend most of their time on other sites, so they expect your site to work like all other sites. ScamShield adopts standard top-bar navigation, familiar hamburger menus on mobile, standard search/input cards, and recognizable footer copyright and contact links."),
        
        ("Gestalt Principles of Visual Perception", 
         "• Proximity: Form fields and their descriptive labels are grouped closely together.\n"
         "• Similarity: All primary action buttons share identical deep blue styling and border radii.\n"
         "• Enclosure / Common Region: Distinct card containers enclose each functional module.\n"
         "• Continuity: Stepped indicators and progress bars guide the user's eye sequentially from input to verdict.")
    ]

    for cl_title, cl_desc in cog_laws:
        add_bullet_p(doc, f"{cl_title}: ", cl_desc)

    # 1.5 Accessibility Standards: WCAG 2.2 & ISO 9241
    add_heading_2(doc, "1.5 Accessibility & Ergonomics Standards: WCAG 2.2 & ISO 9241-110")
    
    add_body_p(doc, 
        "ScamShield achieves compliance across the highest international accessibility and ergonomics standards:"
    )

    wcag_points = [
        ("WCAG 2.2 Guideline 1.4.1 (Use of Color - Level A)", 
         "Color is never used as the sole visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element. High Risk combines Red + 🚨 Icon + Score Number + 'Potential Scam' Text Badge + Heavy Double Border. A color-blind user can interpret the verdict with 100% accuracy."),
        
        ("WCAG 2.2 Guideline 1.4.3 (Contrast Minimum - Level AA)", 
         "Text has a contrast ratio of at least 4.5:1 against its background. In High Contrast Mode, contrast exceeds 7:1 (Level AAA)."),
        
        ("WCAG 2.2 Guideline 1.4.4 (Resize Text - Level AA)", 
         "Text can be resized up to 200% without loss of content or functionality. ScamShield provides dedicated [A-] [A] [A+] buttons scaling the root --font-scale variable from 0.88x to 1.35x."),
        
        ("WCAG 2.2 Guideline 2.1.1 (Keyboard Navigable - Level A)", 
         "All functionality is operable through a keyboard interface without requiring specific timings for individual keystrokes. Features visible :focus-visible rings and a Skip-to-Content link (#main-content)."),
        
        ("WCAG 2.2 Guideline 2.5.8 (Target Size - Level AA)", 
         "Interactive targets have an area of at least 24x24 CSS pixels, and ScamShield strictly enforces a minimum touch target of 44x44 CSS pixels across all buttons and inputs."),
        
        ("ISO 9241-110 Dialogue Principles", 
         "• Suitability for the Task: Focuses strictly on fraud detection without extraneous distractions.\n"
         "• Self-Descriptiveness: Labels, placeholders, and tooltips explain input requirements.\n"
         "• Conformity with User Expectations: Standardized card layouts and conventions.\n"
         "• Error Tolerance: Graceful handling of empty or blurry inputs.\n"
         "• Suitability for Individualisation: Font scaler, theme toggle, OpenDyslexic font, and trilingual switching.")
    ]

    for wp_title, wp_desc in wcag_points:
        add_bullet_p(doc, f"{wp_title}: ", wp_desc)

    # 1.6 AI-Specific HCI: Calibrated Trust & XAI
    add_heading_2(doc, "1.6 AI-Specific HCI: Calibrated Trust & Explainable AI (XAI)")
    
    add_body_p(doc, 
        "In algorithmic cybersecurity, Human-AI Interaction requires deliberate calibration of trust. "
        "If users blindly trust the system, a single false negative can result in stolen life savings (Automation Bias / Complacency). "
        "Conversely, if the system triggers excessive false positives or acts as an opaque black box, users abandon it entirely (Algorithmic Distrust)."
    )

    add_callout(doc,
        "ScamShield calibrates user trust through three concrete mechanisms:\n"
        "1. Nuanced Verdict Terminology: Benign content is labeled 'Potentially Safe' rather than '100% Guaranteed Safe', nudging users to retain healthy skepticism.\n"
        "2. Transparent Feature Attribution: Suspicious keywords are highlighted in context (<mark>), and rule-based triggers explain why a score was assigned.\n"
        "3. Human-in-the-Loop Feedback: A 'Was this assessment helpful?' widget empowers users to rate system accuracy, fostering collaborative oversight.",
        title="Trust Calibration Architecture"
    )

def build_chapter_2(doc):
    add_heading_1(doc, "CHAPTER 2: End-to-End Component Audit (From 0 to End)")
    
    add_body_p(doc, 
        "This chapter audits every screen and component in ScamShield based strictly on the production codebase. "
        "Each section includes route specifications, input modalities, an embedded high-resolution wireframe schematic "
        "(showing Mobile 390px and Desktop 1280px viewports side-by-side), HCI principles applied, and key cognitive safeguards."
    )

    screens = [
        {
            "num": "1",
            "title": "Global Application Shell & Navigation",
            "route": "templates/base.html",
            "template": "All pages (Jinja2 Template Inheritance)",
            "modalities": "Mouse, Keyboard, Touch, Screen Readers",
            "image": "wireframes/images/00_master_gallery.png",
            "hci_terms": [
                ("ISO 9241-110 Individualisation", "Dedicated utility bar offering trilingual switching (EN/MR/HI), font scaling ([A-] [A] [A+]), dark mode, high contrast, and OpenDyslexic font."),
                ("WCAG 2.4.1 Bypass Blocks", "Hidden Skip-to-Content link (#main-content) visible on keyboard focus."),
                ("Jakob's Law", "Standard top-left brand anchor, top-right navigation links, and unified footer layout.")
            ],
            "ux_details": [
                ("Universal State Persistence", "All visual preferences (theme, language, font scale) are persisted across sessions via browser localStorage."),
                ("Polite ARIA Live Region", "A dedicated live region (#aria-live-status) announces dynamic status updates to screen readers."),
                ("Zero Duplicate Text & Emojis", "Strict typographic integrity eliminates confusing visual noise.")
            ]
        },
        {
            "num": "2",
            "title": "Screen 01: Home Dashboard",
            "route": "/ (app.py: index)",
            "template": "templates/index.html",
            "modalities": "Clickable Cards, Keyboard Hotkeys [1]-[4]",
            "image": "wireframes/images/01_home_dashboard.png",
            "hci_terms": [
                ("Hick-Hyman Law", "Limits decision complexity to exactly n = 4 primary threat channels: SMS, Email, URL/QR, and Phone."),
                ("Fitts's Law", "The entire card surface is wrapped in an anchor tag, creating massive touch targets exceeding 280px x 180px."),
                ("Shneiderman Rule #2 (Accelerators)", "Keyboard users can press hotkeys [1] through [4] to jump directly into checkers."),
                ("Nielsen Heuristic #10 (Help)", "Dismissible onboarding banner guides first-time users on how to paste or upload content.")
            ],
            "ux_details": [
                ("High-Affordance Iconography", "Each card features a prominent channel icon ([icon: SMS], [icon: Email], [icon: URL], [icon: Phone])."),
                ("Quick Stat Counters", "Real-time summary badges communicate system activity and active protection coverage.")
            ]
        },
        {
            "num": "3",
            "title": "Screen 02: Check SMS / WhatsApp",
            "route": "/analyze/sms (GET/POST)",
            "template": "templates/sms.html",
            "modalities": "Text Paste, Screenshot Upload (Tesseract OCR)",
            "image": "wireframes/images/02_check_sms.png",
            "hci_terms": [
                ("Norman's Signifiers", "Dual-modal tabs cleanly distinguish between manual text entry and screenshot OCR."),
                ("Nielsen Heuristic #6 (Recognition over Recall)", "Pre-filled sample chips ('Electricity Bill Disconnection', 'Safe Bank OTP') allow instant testing without live scam text."),
                ("Nielsen Heuristic #7 (Flexibility)", "One-tap 'Paste from Clipboard' and 'Clear' buttons streamline mobile text handling."),
                ("Privacy by Design", "Client-side disclaimer reassures users that phone numbers and OTPs are masked prior to inference.")
            ],
            "ux_details": [
                ("Drag-and-Drop Dropzone", "Dashed border dropzone with visual hover feedback simplifies screenshot uploading."),
                ("Real-Time Character Counter", "Prevents input overflow and ensures users remain within NLP model constraints.")
            ]
        },
        {
            "num": "4",
            "title": "Screen 03: Check Email Phishing",
            "route": "/analyze/email (GET/POST)",
            "template": "templates/email.html",
            "modalities": "Sender Header, Subject, Body Text, Screenshot OCR",
            "image": "wireframes/images/03_check_email.png",
            "hci_terms": [
                ("Norman's Conceptual Models", "Multi-field input architecture mirrors real email clients (From, Subject, Body) to match user mental models."),
                ("Error Prevention (Nielsen #5)", "Validates email address syntax on the sender field and enforces required body content."),
                ("Preset Demo Chips", "Realistic phishing scenarios ('Urgent Payroll Update', 'Safe Shipping Notice') demonstrate spoofing cues.")
            ],
            "ux_details": [
                ("Spoofed Header Inspection", "Engine correlates sender domain with body text to detect display name impersonation."),
                ("Progressive Form Layout", "Optional fields are clearly labeled, keeping the primary focus on the email body.")
            ]
        },
        {
            "num": "5",
            "title": "Screen 04: Check Website URL & QR Code ('Quishing')",
            "route": "/analyze/url (GET/POST)",
            "template": "templates/url.html",
            "modalities": "Text URL, QR Code Image (OpenCV / pyzbar), Screenshot OCR",
            "image": "wireframes/images/04_check_url_qr.png",
            "hci_terms": [
                ("Multimodal Affordance", "Eliminates tedious and error-prone typing of obscure phishing URLs by decoding QR code screenshots automatically."),
                ("Error Tolerance (ISO 9241-110)", "Server normalizes raw domain inputs (e.g., example.com) by prepending https:// automatically."),
                ("Quishing Risk Awareness", "Educates users on physical attack vectors such as fraudulent QR stickers pasted over parking meters or restaurant menus.")
            ],
            "ux_details": [
                ("Real-Time Domain Extraction", "Displays parsed hostname, IP address detection, and top-level domain (TLD) risk telemetry."),
                ("QR Matrix Validation", "Informs the user immediately whether the QR code was successfully extracted and decoded.")
            ]
        },
        {
            "num": "6",
            "title": "Screen 05: Phone Call Fraud Questionnaire",
            "route": "/analyze/phone (GET/POST)",
            "template": "templates/phone.html",
            "modalities": "Interactive Radio Buttons, Dynamic Progress Stepper",
            "image": "wireframes/images/05_check_phone.png",
            "hci_terms": [
                ("Miller's Law (7 +/- 2 Chunks)", "10 questions are structured into two 5-question cognitive chunks (Part 1: Banking & OTPs; Part 2: Impersonation & Panic)."),
                ("Nielsen Heuristic #1 (Visibility of Status)", "A dynamic visual progress bar fills smoothly with real-time percentage updates as answers are selected."),
                ("Hick-Hyman Law", "Binary Yes/No radio buttons minimize choice deliberation for stressed victims.")
            ],
            "ux_details": [
                ("Persistent Sticky Actions", "Submit and Reset buttons remain accessible at the base of the questionnaire."),
                ("Dynamic Threat Counter", "Accumulates affirmative risk markers in real-time to preview threat severity.")
            ]
        },
        {
            "num": "7",
            "title": "Screens 06-08: Risk Assessment Engine (High / Med / Low)",
            "route": "Rendered via result.html across all analyzer routes",
            "template": "templates/result.html",
            "modalities": "Visual Gauge, Audio Speech (TTS), Accordion Telemetry",
            "image": "wireframes/images/06_result_high_risk.png",
            "hci_terms": [
                ("Shneiderman Rule #4 (Design for Closure)", "Prominent top closure banner announces 'Scan Complete', delivering psychological relief."),
                ("WCAG 2.2 Guideline 1.4.1 (Non-Color-Alone)", "High Risk uses Red + 🚨 + Score + 'Potential Scam' Text + Heavy Double Border; Medium uses Dashed; Low uses Solid."),
                ("Progressive Disclosure", "Verdict and Top Directive are shown first; detailed feature attribution is tucked into an expandable accordion."),
                ("Explainable AI (XAI)", "Suspicious keywords are highlighted in context (<mark>), accompanied by concrete rule explanations.")
            ],
            "ux_details": [
                ("Web Speech Narration (TTS)", "Allows illiterate, visually impaired, or panicked users to hear the safety verdict read aloud."),
                ("Actionable Directives", "Clear separation between strict prohibitions ('Do NOT click links') and recommended verifications ('Call bank directly').")
            ]
        },
        {
            "num": "8",
            "title": "Screen 09: Scan History & Audit Trail",
            "route": "/history (GET)",
            "template": "templates/history.html",
            "modalities": "Search Filter, Risk Filter, CSV Export, Print Dossier",
            "image": "wireframes/images/09_scan_history.png",
            "hci_terms": [
                ("Nielsen Heuristic #5 (Error Prevention)", "Clearing history triggers a two-step modal confirmation dialog with focus trapped on 'Cancel'."),
                ("External Scaffolding", "One-click 'Export CSV' and 'Print Report' allow victims to generate physical evidence for police and bank filings."),
                ("Empathetic Empty State", "When no scans exist, a clean empty-box illustration guides the user back to the Home dashboard.")
            ],
            "ux_details": [
                ("Client-Side Instant Search", "Filters past scans instantly by keyword, date, or channel without reloading the page."),
                ("Privacy by Design", "History is stored in secure session storage and never transmitted to third parties.")
            ]
        },
        {
            "num": "9",
            "title": "Screen 10: Scam Awareness & Learning Center",
            "route": "/learn (GET)",
            "template": "templates/learn.html",
            "modalities": "Interactive Formative Quiz, Threat Taxonomy Cards",
            "image": "wireframes/images/10_learning_center.png",
            "hci_terms": [
                ("Active Retrieval Practice", "Interactive 3-question formative quiz reinforces cognitive pattern recognition for common fraud vectors."),
                ("Immediate Pedagogical Feedback", "Selecting an answer reveals instant explanations detailing why the choice is right or wrong."),
                ("Cognitive Scaffolding", "Scam taxonomy categorizes fraud into Banking, Quishing, Utility, and Lottery scams.")
            ],
            "ux_details": [
                ("Score Gamification", "Celebratory completion banner encourages digital literacy development."),
                ("Visual Red Flag Callouts", "Highlights the psychological weapons used by scammers: Fear, Urgency, Authority, and Greed.")
            ]
        },
        {
            "num": "10",
            "title": "Screen 11: Community Reporting & Emergency Helplines",
            "route": "/report (GET/POST)",
            "template": "templates/report.html",
            "modalities": "Click-to-Call Dialing, Structured Incident Form",
            "image": "wireframes/images/11_report_helplines.png",
            "hci_terms": [
                ("Emergency Triage (Fitts's Law)", "Top card features an oversized click-to-call button for India's 1930 National Cybercrime Helpline."),
                ("Golden Hour Preservation", "Plain language emphasizes the critical first 2 hours to freeze stolen funds in banking switches."),
                ("Structured Form Inputs", "Step-by-step incident form captures channel, transaction IDs, and fraudulent phone numbers without overwhelming the victim.")
            ],
            "ux_details": [
                ("Direct Link to cybercrime.gov.in", "Provides official institutional pathways for legal FIR filing."),
                ("Emotional Reassurance", "Empathetic copy calms victim distress and reduces self-blame stigma.")
            ]
        },
        {
            "num": "11",
            "title": "Screen 12: Zero Dead-End Error Recovery",
            "route": "Triggered on 404, 400, 413, 500 error conditions",
            "template": "templates/error.html",
            "modalities": "Navigation Chips, Return Shortcut",
            "image": "wireframes/images/12_error_recovery.png",
            "hci_terms": [
                ("Nielsen Heuristic #9 (Recover from Errors)", "Replaces cryptic HTTP error codes with polite, plain-language diagnostic descriptions."),
                ("Shneiderman Rule #6 (Easy Reversal)", "Provides a direct '🔄 Try Again' link returning straight to the specific scanner where the error occurred."),
                ("Zero Dead-End Architecture", "Embeds a persistent 4-channel navigation bar so users can pivot to other scanning tasks without restarting.")
            ],
            "ux_details": [
                ("Non-Blaming Language", "Frame errors as system limitations ('Could Not Read Image') rather than user failures ('You uploaded a bad file')."),
                ("High-Affordance CTAs", "Primary 'Back to Home' button provides an unmistakable emergency exit.")
            ]
        },
        {
            "num": "12",
            "title": "Screen 13: UI Modals, Overlays & Microinteractions",
            "route": "Global UI State Components",
            "template": "base.html, history.html, main.js",
            "modalities": "Loading Overlay, Focus-Trapped Modals, Floating Toasts",
            "image": "wireframes/images/13_ui_overlays.png",
            "hci_terms": [
                ("Nielsen Heuristic #1 (Visibility of Status)", "Full-screen analyzing overlay locks the screen and displays progress micro-copy during OCR inference."),
                ("Nielsen Heuristic #5 (Error Prevention)", "Modal focus trap confines keyboard Tab navigation within the active confirmation dialog."),
                ("Informative Feedback (Shneiderman #3)", "Non-intrusive toast notifications slide in to confirm actions ('URL copied to clipboard').")
            ],
            "ux_details": [
                ("Keyboard Escape Dismissal", "All modal dialogs close immediately upon pressing the Escape key."),
                ("Background Backdrop Blur", "Semi-transparent backdrop obscures underlying content to focus cognitive attention.")
            ]
        },
        {
            "num": "13",
            "title": "Screen 14: System User-Flow Architecture",
            "route": "Entire Application User Journey",
            "template": "End-to-End System Navigation",
            "modalities": "Navigation Graph, State Transitions, Error Recovery Paths",
            "image": "wireframes/images/14_user_flow_map.png",
            "hci_terms": [
                ("Conceptual Integrity", "Unified user mental model across all 4 entry channels leading to a standardized result gauge."),
                ("Branching Error Recovery", "All failure states funnel smoothly through unified error handlers with zero cognitive dead-ends."),
                ("Cyclical Evaluation", "Results offer direct pathways to History, Reporting, Learning, or New Scans.")
            ],
            "ux_details": [
                ("Shallow Navigation Hierarchy", "Maximum depth from Home to any final verdict is strictly 2 clicks."),
                ("Unified Result Architecture", "A single, highly versatile template (result.html) handles verdicts for SMS, Email, URL, QR, and Phone.")
            ]
        }
    ]

    for s in screens:
        add_heading_2(doc, f"2.{s['num']} {s['title']}")
        
        meta_p = add_body_p(doc, space_after=4)
        r_meta = meta_p.add_run(f"Route: {s['route']}  |  Template: {s['template']}  |  Input Modalities: {s['modalities']}")
        format_run(r_meta, font_name="Consolas", size=9, color_rgb=(0x4A, 0x55, 0x68))

        # Embed Image
        if os.path.exists(s["image"]):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(6)
            img_p.paragraph_format.space_after = Pt(4)
            r_img = img_p.add_run()
            r_img.add_picture(s["image"], width=Inches(6.2))
            
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_after = Pt(8)
            r_cap = cap_p.add_run(f"Figure 2.{s['num']}: Low-Fidelity Wireframe for {s['title']} (Mobile 390px & Desktop 1280px)")
            format_run(r_cap, font_name="Segoe UI", size=8.5, italic=True, color_rgb=(0x71, 0x80, 0x96))

        add_heading_3(doc, "Human-Computer Interaction (HCI) Principles Applied:")
        for term, desc in s["hci_terms"]:
            add_bullet_p(doc, f"• {term}: ", desc)

        add_heading_3(doc, "Key UX Decisions & Cognitive Safeguards:")
        for dec, rat in s["ux_details"]:
            add_bullet_p(doc, f"✓ {dec}: ", rat)

def build_chapter_3(doc):
    add_heading_1(doc, "CHAPTER 3: Complete HCI Term & Feature Cross-Reference Matrix")
    
    add_body_p(doc, 
        "This lookup matrix maps every user-facing feature, control, and algorithmic safeguard across ScamShield "
        "to its foundational HCI discipline, exact source code file and line number, and cognitive human rationale."
    )

    tbl = doc.add_table(rows=28, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(1.5), Inches(1.5), Inches(1.3), Inches(2.2)]

    # Headers
    headers = ["ScamShield Feature", "Primary HCI Principle", "Source Reference", "Cognitive / Human Rationale"]
    hdr_row = tbl.rows[0]
    for idx, text in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = col_w[idx]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color="CBD5E0", size="4")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        format_run(r, font_name="Segoe UI Semibold", size=9, bold=True, color_rgb=(0xFF, 0xFF, 0xFF))

    matrix_data = [
        ("[A-] [A] [A+] Font Scaler", "ISO 9241-110 Individualisation / WCAG 1.4.4", "static/js/main.js:505", "Accommodates seniors with presbyopia without requiring browser zoom knowledge."),
        ("Trilingual Toggle (EN/MR/HI)", "Universal Design / Real-World Match", "translations.py, app.py:182", "Overcomes linguistic barriers for vernacular users in Maharashtra and India."),
        ("Number Hotkeys [1]–[4]", "Shneiderman Rule #2 Shortcuts", "static/js/main.js:566", "Reduces motor effort for frequent, power, and motor-impaired users."),
        ("Dismissible Onboarding Banner", "Nielsen Heuristic #10 Help / Onboarding", "templates/index.html:6", "Decreases cognitive friction for novices; stores dismissed state in localStorage."),
        ("4 Scanner Cards on Home", "Hick-Hyman Law & Fitts's Law", "templates/index.html:31", "Logarithmic choice reduction (T = b log2(n+1)); large targets (>= 44px)."),
        ("Dual-Modal Tabs (Text vs Image)", "Norman's Signifiers & Multimodality", "templates/sms.html:29", "Explicit visual signifiers distinguish typing/pasting from OCR image processing."),
        ("Sensitive Data Auto-Masking", "Ethical AI & Privacy by Design", "risk/privacy.py:14", "Pre-emptively sanitizes credit cards, OTPs, and passwords via regex before ML scoring."),
        ("Preset Demo Example Chips", "Nielsen Heuristic #6 Recognition", "templates/sms.html:70", "Users recognize typical fraud patterns rather than needing to recall live scam text."),
        ("Quishing (QR Code Decoding)", "Multimodal Affordance", "ocr/qr_detector.py", "Eliminates tedious, error-prone manual typing of obscure shortened phishing URLs."),
        ("Phone Survey 5-Item Chunks", "Miller's Law (7 +/- 2 Working Memory)", "templates/phone.html:34", "Prevents cognitive overload by grouping 10 questions into two 5-item mental chunks."),
        ("Survey Live Progress Bar", "Nielsen Heuristic #1 Visibility of Status", "templates/phone.html:23", "Real-time visual progress fill and percentage text eliminate ambiguity."),
        ("Analyzing Loading Overlay", "Nielsen Heuristic #1 Visibility of Status", "templates/base.html:79", "Informs user that fraud inference is running; prevents double form submissions."),
        ("Task Closure Banner", "Shneiderman Rule #4 Design for Closure", "templates/result.html:8", "Psychological relief: explicitly communicates that assessment is finalized."),
        ("Multi-Coded Risk Gauge", "WCAG 2.2 Guideline 1.4.1 Non-Color-Alone", "templates/result.html:23", "Combines Score + Color + Icon + Explicit Text Badge + Distinct Border Styles."),
        ("Top Immediate Safety Directive", "Cognitive Triage & Hick-Hyman Law", "templates/result.html:47", "Isolates single most critical immediate behavior ('Do NOT click, block sender')."),
        ("Audio Read Aloud (TTS)", "WCAG 2.2 Multimodal Audio Accessibility", "static/js/main.js:227", "Speech synthesis narrates findings for visually impaired or low-literacy users."),
        ("Progressive Disclosure Accordion", "Hick-Hyman & Progressive Disclosure", "templates/result.html:74", "Keeps initial verdict clean; enables deep verification of reasons on demand."),
        ("Keyword Highlighting (<mark>)", "Visual Saliency & Explainable AI (XAI)", "risk/privacy.py:48", "Visually isolates threat keywords (URGENT, blocked) for transparent attribution."),
        ("Action Checklist (action-dont)", "Actionable Heuristics & Gestalt", "templates/result.html:104", "Distinguishes affirmative actions from prohibitions with distinct styling."),
        ("'Was this helpful?' Widget", "Closed-Loop Feedback & Human-in-the-Loop", "templates/result.html:118", "Calibrates AI performance against real-world human perception."),
        ("Calibrated Trust Disclaimer", "AI Ethics & Calibrated Trust", "templates/result.html:130", "Mitigates over-reliance by acknowledging system limitations and false negatives."),
        ("Clear History Modal Dialog", "Nielsen Heuristic #5 Error Prevention", "templates/history.html:24", "Modal focus trap prevents accidental deletion of user scan records."),
        ("CSV & Print Report Actions", "Institutional Scaffolding", "templates/history.html:18", "Enables victims to produce structured evidence logs for cyber police and banks."),
        ("Empathetic Empty State", "Nielsen Heuristic #9 Recovery", "templates/history.html:87", "Avoids a blank screen; illustrates an empty mailbox with a direct 'Go Home' CTA."),
        ("Interactive Quiz Feedback", "Active Retrieval Practice", "templates/learn.html:71", "Tests intuition and provides immediate pedagogical explanations for mistakes."),
        ("Emergency Dial 1930 Callout", "Fitts's Law & Emergency Triage", "templates/report.html:18", "Prominent click-to-call button enables rapid dialing within the golden hour."),
        ("Error Recovery Shortcut Chips", "Zero Dead-End Architecture", "templates/error.html:25", "Provides 4 alternate pathways so users are never stranded on broken pages.")
    ]

    for row_idx, data in enumerate(matrix_data):
        row = tbl.rows[row_idx + 1]
        bg_col = "F7FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx in range(4):
            cell = row.cells[col_idx]
            cell.width = col_w[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color="E2E8F0", size="4")
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            
            text_val = data[col_idx]
            r = p.add_run(text_val)
            is_bold = (col_idx == 0)
            f_name = "Consolas" if col_idx == 2 else "Segoe UI"
            f_size = 8.5 if col_idx == 2 else 9
            format_run(r, font_name=f_name, size=f_size, bold=is_bold, color_rgb=(0x2D, 0x37, 0x48))

def build_chapter_4(doc):
    add_heading_1(doc, "CHAPTER 4: Viva Voce Defense Guide (Top 25 Professor Questions & Flawless Model Answers)")
    
    add_body_p(doc, 
        "This chapter equips the presenter with 25 authoritative, academically rigorous model answers designed "
        "to satisfy senior professors, external examiners, and HCI lab evaluators. Organized into 5 specialized categories."
    )

    # Category A: Usability & Heuristic Evaluation
    add_heading_2(doc, "Category A: Core Usability & Heuristic Evaluation")
    
    cat_a_qas = [
        (1, "Why did you build an analyzing loading overlay when modern Python ML inference takes less than 100 milliseconds?",
         "Sir/Ma'am, that design decision is rooted in Nielsen's First Usability Heuristic: Visibility of System Status and the psychology of perceived performance.\n\n"
         "When users submit an image or message under severe financial stress, instantaneous transitions often feel artificial or induce anxiety that the system did not perform a real analysis. The loading overlay accomplishes three critical HCI goals:\n"
         "1. Immediate Feedback: Confirms the system has received the request and is processing.\n"
         "2. Error Prevention: Disables repeated clicks and duplicate form submissions.\n"
         "3. Transparency: Plain-language micro-copy ('Inspecting text patterns, urgency signals, and security risks...') constructs a clear conceptual model of the ML pipeline."),
        
        (2, "What is Fitts's Law, and cite three exact places in your codebase where you mathematically applied it?",
         "Fitts's Law states that the time to rapidly move to a target area is a function of distance (D) and target width (W): T = a + b * log2(2D / W).\n\n"
         "In ScamShield, we applied this in three distinct areas:\n"
         "1. Target Size (W): Every interactive button, chip, and input strictly satisfies WCAG 2.2 Success Criterion 2.5.8 by enforcing a minimum bounding box of 44px x 44px, drastically reducing motor miss-clicks.\n"
         "2. Full-Width Primary CTAs: On mobile viewports, the primary 'Check Safety' button spans 100% container width, maximizing W so thumb acquisition time approaches the minimum theoretical threshold.\n"
         "3. Clickable Card Affordances: On the Home dashboard (templates/index.html), the entire card is wrapped in the anchor tag (<a class='option-card'>), making the target area massive rather than restricting the clickable area to just the text link."),
        
        (3, "What is Hick-Hyman Law, and how did you resolve decision fatigue on your landing page?",
         "Hick-Hyman Law mathematically models cognitive choice reaction time as T = b * log2(n + 1), where n is the number of equiprobable choices.\n\n"
         "Rather than exposing users to complex technical navigation menus or dense parameter configurations, our Home dashboard limits the primary triage decision to exactly n = 4 mutually exclusive threat channels: SMS, Email, URL/QR, and Phone. This limits decision time to roughly 2 bits of cognitive processing. Furthermore, our Phone questionnaire reduces each question to binary Yes/No choices (n = 2), cutting deliberation time to the absolute minimum for panicked victims."),
        
        (4, "Why did you split the phone questionnaire into two parts instead of showing all 10 questions on one page?",
         "That directly implements Miller’s Law, which states that human working memory capacity can hold 7 +/- 2 cognitive chunks at any given moment.\n\n"
         "When a victim has just received an extortion call, their cognitive bandwidth is severely degraded by acute stress. An unchunked list of 10 legalistic questions triggers task abandonment. By grouping the questionnaire into Part 1 (5 questions on Passwords & Banking) and Part 2 (5 questions on Caller Impersonation & Panic), we keep cognitive load well within the 5-item working memory threshold. We also pair this with a dynamic progress bar for continuous closure feedback."),
        
        (5, "What is Progressive Disclosure, and where is it in your application?",
         "Progressive Disclosure is an HCI interaction technique that sequences information and actions across several steps or layers to reduce initial cognitive overload.\n\n"
         "On our Result screen (templates/result.html), we present the Primary Level first: the Task Closure Banner, the Risk Meter, the Plain-Language Verdict, and the Top Safety Directive. The Secondary Level—which includes the highlighted keyword snippet, the heuristic attribution breakdown, the action checklist, the feedback widget, and the regulatory disclaimer—is housed within an expandable accordion (#result-details-content). Stressed users get immediate safety directives in 3 seconds, while analytical users can expand the details to inspect the underlying machine learning reasons on demand.")
    ]

    for qnum, qtext, qans in cat_a_qas:
        add_viva_qa(doc, qnum, qtext, qans)

    # Category B: Accessibility, Inclusivity & Ergonomics
    add_heading_2(doc, "Category B: Accessibility, Inclusivity & Ergonomics")
    
    cat_b_qas = [
        (6, "Why is displaying a red gauge or red text alone considered a severe HCI violation for risk assessment?",
         "Relying on color alone directly violates WCAG 2.2 Guideline 1.4.1 (Use of Color). Approximately 8% of men and 0.5% of women suffer from color-vision deficiency (such as Deuteranopia or Protanopia), meaning a red gauge and a green gauge can appear virtually identical.\n\n"
         "In ScamShield, we implemented redundant, multi-coded risk encoding:\n"
         "1. Numerical Value: Explicit numerical score (e.g. 85 / 100).\n"
         "2. Textual Badge: Unambiguous string label (Potential Scam (High Risk)).\n"
         "3. Iconography: Distinct symbolic signifiers (🛡️ for Safe, ⚠️ for Suspicious, 🚨 for Scam).\n"
         "4. Low-Fidelity Border Styling: Solid borders for Safe, Dashed borders for Medium, and Heavy Double borders for High Risk.\n"
         "A color-blind user or a user on a monochromatic e-ink display can determine the risk level with 100% accuracy without perceiving color."),
        
        (7, "Why did you build custom font scaling buttons ([A-] [A] [A+]) instead of letting users zoom with Ctrl + Plus?",
         "This implements the principle of Individualisation from ISO 9241-110 and universal accessibility.\n\n"
         "Our primary persona research revealed that elderly users frequently suffer from presbyopia and reduced visual acuity, but often lack knowledge of keyboard shortcuts like Ctrl + Plus or browser pinch-to-zoom settings. Our dedicated toolbar buttons ([A-] [A] [A+]) provide visible, high-affordance signifiers right at the top of every screen. In static/js/main.js, clicking these buttons scales the root CSS custom property --font-scale, adjusts document zoom between 0.88x and 1.35x, updates button active states, and triggers an informative toast confirmation."),
        
        (8, "How does ScamShield comply with WCAG 2.2 Level AA guidelines for touch and keyboard accessibility?",
         "We achieved compliance across several critical criteria:\n"
         "1. Target Size (SC 2.5.8): All interactive controls have a minimum bounding box of 44px x 44px.\n"
         "2. Contrast (SC 1.4.3): Standard text contrast exceeds 4.5:1, and our High Contrast Mode exceeds 7:1.\n"
         "3. Keyboard Navigable (SC 2.1.1): Full logical tab order with visible :focus-visible outlines, plus an accessible Skip-to-Content link (#main-content) fulfilling SC 2.4.1.\n"
         "4. Speech Narration: We integrated the native Web Speech API (SpeechSynthesisUtterance), allowing blind, dyslexic, or illiterate users to hear the result narrated aloud in English, Marathi, or Hindi."),
        
        (9, "Why is multilingual localization considered a fundamental HCI requirement rather than just a translation feature?",
         "In HCI, localization is an issue of Cognitive Load and Inclusive Universal Design. In India, a significant portion of internet users are non-native English speakers who conduct daily life in Marathi or Hindi.\n\n"
         "When confronting financial fraud, attempting to parse foreign cybersecurity terminology in English creates immense cognitive friction and panic. By providing instant, client-side persisted trilingual toggles across 276 localized keys in translations.py, we eliminate linguistic barriers, ensuring that elderly and rural citizens can assess threats in their native tongue without delay."),
        
        (10, "How does the OpenDyslexic font integration improve cognitive accessibility?",
         "Individuals with dyslexia frequently experience letter rotation, inversion, and crowding (e.g., confusing 'b' and 'd', or 'p' and 'q').\n\n"
         "OpenDyslexic utilizes weighted bottoms and unique asymmetric shapes for each letterform, providing a strong gravitational anchor that prevents letters from appearing flipped or shifting in the reader's perceptual field. By embedding OpenDyslexic as a one-click toggle in our accessibility panel, ScamShield accommodates neurodivergent users who would otherwise abandon text-heavy cyber warnings.")
    ]

    for qnum, qtext, qans in cat_b_qas:
        add_viva_qa(doc, qnum, qtext, qans)

    # Category C: AI Ethics, Trust Calibration & Error Handling
    add_heading_2(doc, "Category C: AI Ethics, Trust Calibration & Error Handling")
    
    cat_c_qas = [
        (11, "What is 'Calibrated Trust', and why would giving a 100% 'Guaranteed Safe' verdict be dangerous in your app?",
         "In Human-AI Interaction, Calibrated Trust means that a user's subjective trust in an automated system matches the system's actual objective capabilities.\n\n"
         "If an AI app claims a message is '100% Guaranteed Safe', it causes Over-Trust (Complacency). If the message turns out to be an unseen, zero-day spear-phishing attack (a false negative), the victim will unconditionally trust the sender and lose their life savings. Conversely, if the system flags everything as high risk, it causes Under-Trust (Cynicism), and users will bypass it entirely.\n\n"
         "ScamShield actively calibrates trust by:\n"
         "1. Labeling clean content as 'Potentially Safe' rather than 'Guaranteed Safe'.\n"
         "2. Providing an honest disclaimer that ML models rely on heuristic estimates.\n"
         "3. Educating users to inspect red flags independently, keeping the human firmly in the decision-making loop."),
        
        (12, "How does your Explainable AI (XAI) implementation satisfy the 'Right to Explanation'?",
         "Rather than acting as a black-box oracle that simply outputs a risk number, ScamShield provides multi-layered feature attribution:\n"
         "1. Visual Attribution: In risk/privacy.py, our highlight_suspicious_keywords function scans the text and wraps threat markers (e.g. URGENT, blocked, bit.ly) in <mark class='suspicious-keyword'> tags.\n"
         "2. Rule-Based Explanation: In risk/risk_engine.py, our engine outputs a human-readable list under 'Why did we give this score?' detailing exact triggers (e.g. 'The link uses an IP address instead of a recognized domain').\n"
         "3. Prescriptive Actionability: It translates technical findings into actionable safety steps under 'What should you do now?', differentiating strict prohibitions (action-dont) from recommended verifications (action-do)."),
        
        (13, "How does your system implement Shneiderman’s Rule #5: Prevent Errors?",
         "We prevent errors on multiple levels:\n"
         "1. Destructive Action Confirmation: In templates/history.html, clicking 'Clear History' does not delete data immediately; it invokes a modal dialog with focus trapped on 'Cancel' and keyboard Escape dismissal.\n"
         "2. Protocol Normalization: In app.py, our URL parser accepts raw domain inputs without schemes, preventing form crashes when users omit https://.\n"
         "3. Input Format Enclosures: The file upload dropzone restricts uploads strictly to image MIME types (.png, .jpg, .jpeg, .webp), blocking invalid binary payloads."),
        
        (14, "What is your 'Zero Dead-End' error recovery architecture?",
         "In bad UX design, an error page simply says '404 Not Found' or 'Bad Request', leaving the user stranded.\n\n"
         "In ScamShield, our unified error template (templates/error.html) implements Nielsen Heuristic #9 (Help Users Recover from Errors). It provides:\n"
         "1. A polite, non-blaming plain-language diagnosis ('Could Not Read Screenshot... The image was blurry').\n"
         "2. Two primary escape routes: a direct '🔄 Try Again' return link and a '🏠 Back to Home' button.\n"
         "3. An Error Recovery Navigation Panel rendering 4 quick shortcut chips (Check SMS, Check Email, Check URL, Check Phone), enabling users to switch modalities instantly without restarting their journey."),
        
        (15, "How does ScamShield balance data privacy with machine learning explainability?",
         "This represents our implementation of Privacy by Design (ISO/IEC 27701). In risk/privacy.py, prior to transmitting any user input to our NLP vectorizer or displaying it back on the UI, our regex sanitizers detect and mask Aadhaar numbers, 16-digit credit card PANs, and 6-digit OTP codes with asterisks (e.g., **********1234).\n\n"
         "This guarantees that sensitive financial credentials are never cached, leaked in error traces, or exposed during public demonstrations, fulfilling ethical AI requirements.")
    ]

    for qnum, qtext, qans in cat_c_qas:
        add_viva_qa(doc, qnum, qtext, qans)

    # Category D: Cognitive Psychology, Dark Patterns & User Behavior
    add_heading_2(doc, "Category D: Cognitive Psychology, Dark Patterns & User Behavior")
    
    cat_d_qas = [
        (16, "What dark patterns do cybercriminals exploit, and how does your UI design counteract them?",
         "Scammers exploit several cognitive dark patterns:\n"
         "1. Artificial Urgency ('Your account will be blocked in 10 minutes'): Exploits temporal discounting and induces adrenaline rushes that bypass prefrontal rational deliberation.\n"
         "2. False Authority ('Police Commissioner / CBI Officer calling'): Exploits Milgram's obedience bias.\n"
         "3. Quishing Obfuscation: Hiding malicious URLs behind visual QR matrices on physical posters.\n\n"
         "ScamShield counteracts these by introducing deliberate 'Cognitive Speed Bumps'—forcing the user to pause, inspect the highlighted threat keywords, review objective numerical scores, and follow structured safety protocols rather than impulsively obeying the scammer."),
        
        (17, "Why did you implement preset demo example chips on the input forms?",
         "This implements Nielsen Heuristic #6: Recognition Rather Than Recall.\n\n"
         "In cybersecurity education, novices often understand the concept of a scam abstractly but struggle to recall or synthesize what a real phishing message looks like. Our preset chips ('Electricity Disconnection Notice', 'SBI KYC Expired') act as recognizable cognitive templates. Users simply click the chip, and the system populates the textarea with authentic threat syntax, allowing immediate exploration with zero cognitive recall friction."),
        
        (18, "How does your Scan History interface support human memory and legal scaffolding?",
         "Human memory is notoriously unreliable under financial trauma. Victims often forget the exact sender address, the phishing URL, or the timestamp of the message.\n\n"
         "Our Scan History interface (templates/history.html) creates an objective audit trail stored locally in the user's session. It features an instant client-side keyword search bar and dedicated 'Export CSV' and 'Print Report' buttons. This provides external scaffolding, transforming volatile cognitive memory into structured physical documentation ready for submission to bank ombudsmen or cybercrime police."),
        
        (19, "How do Gestalt Laws of Visual Perception influence your card and form designs?",
         "We applied three primary Gestalt laws:\n"
         "1. Law of Proximity: Form labels, helper tooltips, and text inputs are positioned within 4px of each other, while distinct input groups are separated by 24px, ensuring immediate perceptual grouping.\n"
         "2. Law of Similarity: All primary call-to-action buttons share identical navy fills, rounded corners, and bold typography, establishing a clear visual vocabulary for actions.\n"
         "3. Law of Common Region (Enclosure): All assessment metrics (gauge, verdict, safety directives) are enclosed within a single bounded container with a subtle shadow, signaling that they belong to the same analytical evaluation."),
        
        (20, "What is 'Automation Bias', and how does ScamShield prevent users from becoming overly dependent on it?",
         "Automation Bias is the psychological propensity for humans to favor suggestions from automated systems and disregard contradictory information or their own common sense.\n\n"
         "We prevent automation bias by designing ScamShield as a Decision Support System rather than an autonomous decision-maker. We explicitly avoid definitive language like 'Guaranteed 100% Safe'. Instead, our UI pairs every verdict with an expandable 'Why did we give this score?' breakdown and a clear advisory: 'Always verify unexpected communications directly with the organization through official channels.'")
    ]

    for qnum, qtext, qans in cat_d_qas:
        add_viva_qa(doc, qnum, qtext, qans)

    # Category E: Technical Architecture, Multimodal Input & Evaluation
    add_heading_2(doc, "Category E: Technical Architecture, Multimodal Input & Evaluation Methodology")
    
    cat_e_qas = [
        (21, "Why did you add QR Code ('Quishing') parsing to your screenshot OCR pipeline?",
         "From an HCI perspective, Quishing exploits a critical physical-digital interface gap. Scammers paste malicious QR codes on physical parking meters, utility bills, and phishing posters.\n\n"
         "Retyping an encoded 80-character URL from a poster into a phone browser is extremely error-prone and tedious (violating Fitts's Law). Users take a photo. By integrating pyzbar and OpenCV into our screenshot pipeline (ocr/qr_detector.py), ScamShield decodes the raw URL payload directly from the image matrix, parses its domain, and evaluates it through our ML classifier in one single, fluid interaction."),
        
        (22, "What is the cognitive purpose of India's 1930 Cybercrime Helpline banner on the Report page?",
         "In financial fraud, time is the single most critical factor. India's Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS) operates a 'Golden Hour' protocol: if fraud is reported via dial 1930 within the first 2 hours, the Reserve Bank of India and law enforcement can freeze the stolen money before it is laundered through mule accounts.\n\n"
         "In templates/report.html, we placed a massive, high-contrast click-to-call banner for 1930 at the absolute top of the page (Fitts's Law), enabling panicked victims to dial the helpline with a single tap rather than searching through government directories."),
        
        (23, "How did you conduct heuristic evaluation and usability testing on this codebase?",
         "We followed Jakob Nielsen's Discount Usability Engineering methodology:\n"
         "1. Expert Heuristic Walkthrough: Audited all 12 templates against Nielsen's 10 Heuristics and Shneiderman's 8 Golden Rules, cataloging and resolving violations (such as missing loading indicators and color-only risk indicators).\n"
         "2. WCAG 2.2 Automated & Manual Audit: Verified contrast ratios with Lighthouse, ensured keyboard focus traps in modals, and tested screen reader output with NVDA.\n"
         "3. Automated Verification Suite: Created verify_all_workflows.py and test_sample_data.py to validate 28 distinct UI and ML workflows with a 100% pass rate."),
        
        (24, "Why did you avoid using complex JavaScript SPA frameworks like React or Angular for this project?",
         "This was a deliberate HCI and accessibility engineering choice:\n"
         "1. Predictable Standard Navigation: Server-rendered Jinja2 templates ensure that browser back/forward buttons, URL bookmarks, and page reloads behave with 100% predictability (Jakob's Law).\n"
         "2. Minimal Client Footprint: Low-end Android smartphones owned by rural or elderly citizens often suffer from restricted RAM and slow mobile data. Heavy SPA bundles cause 5-second initial load delays. ScamShield renders in under 200ms on 3G networks.\n"
         "3. Assistive Technology Compatibility: Server-rendered HTML delivers clean, predictable DOM structures that native screen readers (TalkBack, NVDA) can parse without complex virtual-DOM reconciliation glitches."),
        
        (25, "If you had 3 more months to research and expand ScamShield, what HCI feature would you build next?",
         "We would implement two cutting-edge HCI research features:\n"
         "1. Real-Time Telephony Voice Analysis Overlay: An on-device floating accessibility widget that listens to live incoming calls (with user consent), performs local acoustic stress and NLP urgency detection, and displays real-time visual warning banners ('⚠️ High-Pressure Extortion Detected') directly over the phone call UI.\n"
         "2. Conversational Vernacular Voice Bot: A conversational AI agent that allows rural citizens who cannot read or write to simply speak into their microphone in their native dialect (e.g., Ahirani, Varhadi, or Bhojpuri), explaining their situation and receiving conversational guidance in return.")
    ]

    for qnum, qtext, qans in cat_e_qas:
        add_viva_qa(doc, qnum, qtext, qans)

def build_chapter_5(doc):
    add_heading_1(doc, "CHAPTER 5: 5-Minute Laboratory Demonstration Script & Examiner Walkthrough")
    
    add_body_p(doc, 
        "During your laboratory project evaluation, do not give an unfocused tour of the code. "
        "Follow this exact, minute-by-minute demonstration script to showcase your mastery of Human-Computer Interaction "
        "and command the highest possible viva score."
    )

    demo_steps = [
        ("Minute 1: Inclusivity & Universal Design (Top Header)",
         "• Action: Open the landing page (http://localhost:5000).\n"
         "• Examiner Script: 'Respected examiners, we begin our demonstration with Universal Design and ISO 9241-110 Individualisation.'\n"
         "• Click [A+] twice: 'Notice our typography scaling engine instantly increases font size for senior citizens with presbyopia without breaking card layouts.'\n"
         "• Click 'मराठी' or 'हिन्दी': 'Notice our seamless trilingual localization across 276 localized keys, removing linguistic barriers for digital citizens across India.'\n"
         "• Toggle High Contrast & OpenDyslexic: 'Our interface strictly satisfies WCAG 2.2 Level AA/AAA contrast and neurodivergent accessibility.'"),
        
        ("Minute 2: Home Dashboard Triage (Hick-Hyman & Fitts's Law)",
         "• Action: Hover over the 4 primary cards.\n"
         "• Examiner Script: 'Notice our choice architecture. In high-stress cybercrime situations, complex navigation causes panic. Applying Hick-Hyman Law (T = b * log2(n+1)), we restrict primary triage to exactly 4 mutually exclusive threat channels.'\n"
         "• Point to Hotkey Badges: 'Per Shneiderman's Rule #2, power users and motor-impaired individuals can use keyboard shortcuts.'\n"
         "• Action: Press the '1' key on your keyboard to smoothly navigate to the SMS Checker."),
        
        ("Minute 3: SMS Input Usability & System Status Feedback",
         "• Action: On SMS Checker, point to the dual-modal tabs.\n"
         "• Examiner Script: 'Per Don Norman's Signifiers, we provide dual-modal input tabs—manual pasting versus screenshot OCR.'\n"
         "• Click preset chip 'Electricity Bill Disconnection': 'This implements Nielsen Heuristic #6: Recognition Rather Than Recall. Users do not need to memorize live phishing text; they can test realistic attack templates with a single click.'\n"
         "• Click 'Check Message Safety': 'Notice Nielsen Heuristic #1: Visibility of System Status. Our analyzing overlay immediately engages with micro-copy, preventing double submissions and constructing an accurate conceptual model of our ML inference.'"),
        
        ("Minute 4: Result Screen (Non-Color-Alone & Explainable AI)",
         "• Action: On the Result Screen, point to the Task Closure Banner.\n"
         "• Examiner Script: 'Per Shneiderman Rule #4, this top closure banner announces 'Scan Complete', providing immediate psychological relief.'\n"
         "• Point to the Risk Meter: 'Crucially, notice our compliance with WCAG 2.2 Guideline 1.4.1 (Non-Color-Alone). We never communicate risk via color alone. High Risk is multi-coded through numerical score (85/100), alert icon (🚨), explicit text badge, and a heavy double border for color-blind accessibility.'\n"
         "• Click '🔊 Read Aloud': Let the examiner hear the speech synthesis narrate the safety directive.\n"
         "• Expand Accordion: 'Notice Progressive Disclosure. Panicked users receive immediate safety directives in 3 seconds, while analytical users can expand the accordion to inspect highlighted suspicious keywords (<mark>) and rule-based explanations.'"),
        
        ("Minute 5: Quishing, Phone Survey & Helplines (Closing Defense)",
         "• Action: Navigate to URL Checker -> Screenshot tab.\n"
         "• Examiner Script: 'To combat physical Quishing traps on parking meters and utility bills, our OpenCV and pyzbar pipeline automatically decodes QR matrices from screenshots, saving users from typing obscure phishing links.'\n"
         "• Open Phone Questionnaire: 'Notice Miller's Law: 10 complex fraud indicators are chunked into two 5-item cognitive stages with a real-time progress bar.'\n"
         "• Open Report Page: 'Finally, we connect users to national institutional infrastructure. Applying Fitts's Law, our primary callout provides click-to-call dialing for India's 1930 Cybercrime Helpline to freeze funds in transit during the golden hour.'\n"
         "• Concluding Statement: 'ScamShield is not just a machine learning model; it is an empathetic, resilient socio-technical safety system engineered to protect human dignity in the digital era.'")
    ]

    for step_title, step_body in demo_steps:
        add_heading_2(doc, step_title)
        add_callout(doc, step_body, border_color="1B365D", bg_color="F0F4F8")

    add_heading_2(doc, "Top 3 Traps to Avoid During Evaluation")
    traps = [
        ("Trap 1: Getting Trapped in Deep ML Equations", 
         "If the examiner asks 'How does your model work?', do NOT give a purely mathematical dissertation on Multinomial Naive Bayes alpha smoothing unless specifically asked. Instead, anchor your answer in HCI: 'Our ML pipeline extracts TF-IDF n-grams, but from an HCI perspective, the critical engineering challenge is Explainable AI (XAI)—translating statistical probability into transparent, human-readable explanations and actionable checklists.'"),
        
        ("Trap 2: Saying 'The App is 100% Accurate and Safe'", 
         "Never claim your system is 100% accurate. External examiners will immediately trap you on false negatives. Always answer using the concept of Calibrated Trust: 'No AI system is infallible against zero-day social engineering. That is why ScamShield labels benign content as 'Potentially Safe' and actively educates users to retain critical skepticism.'"),
        
        ("Trap 3: Glossing Over Errors", 
         "If an input fails or an image is unreadable during the demo, do NOT apologize or panic. Smile and highlight your Zero Dead-End Error Architecture: 'Notice how our system gracefully catches this exception! Instead of crashing or showing a 500 error, it displays Nielsen Heuristic #9 plain-language recovery guidance and offers 4 shortcut chips to pivot to another channel.'")
    ]

    for t_title, t_desc in traps:
        add_bullet_p(doc, f"⚠️ {t_title}: ", t_desc)

def main():
    print("Initializing ScamShield Word Document Generation...")
    doc = create_doc()
    
    print("Building Cover Page...")
    build_cover_page(doc)
    
    print("Building Executive Summary...")
    build_executive_summary(doc)
    
    print("Building Chapter 1: Master HCI Frameworks...")
    build_chapter_1(doc)
    
    print("Building Chapter 2: End-to-End Component Audit (with embedded wireframes)...")
    build_chapter_2(doc)
    
    print("Building Chapter 3: HCI Term & Feature Cross-Reference Matrix...")
    build_chapter_3(doc)
    
    print("Building Chapter 4: Complete Viva Voce Defense Guide (25 Q&As)...")
    build_chapter_4(doc)
    
    print("Building Chapter 5: 5-Minute Demonstration Script...")
    build_chapter_5(doc)
    
    output_filename = "ScamShield_HCI_Master_Evaluation_Guide.docx"
    doc.save(output_filename)
    
    file_size_kb = os.path.getsize(output_filename) / 1024
    print(f"SUCCESS! Created '{output_filename}' ({file_size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
