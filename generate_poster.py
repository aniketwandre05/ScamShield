"""
ScamShield Academic Poster Generator
Generates high-definition, publication-grade academic poster image and PDF.
Matches the exact layout, color palette, tables, workflow, risk engine, and screenshot cards
from the reference poster.
"""

import os
import subprocess
import base64
import shutil
import qrcode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_qr():
    qr = qrcode.QRCode(version=1, box_size=8, border=1)
    qr.add_data('https://scamshield-ozpr.onrender.com')
    qr.make(fit=True)
    img = qr.make_image(fill_color='#0B1A2D', back_color='white')
    qr_path = os.path.join(BASE_DIR, 'poster_qr.png')
    img.save(qr_path)
    with open(qr_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def build_poster_html():
    qr_b64 = create_qr()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ScamShield Academic Poster</title>
<style>
  @page {{
    size: 1600px 2400px;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  html, body {{
    width: 1600px;
    height: 2400px;
    background-color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1E293B;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }}

  /* Top Header Banner */
  header {{
    background-color: #0B132B;
    color: #FFFFFF;
    padding: 24px 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(0,0,0,0.18);
    height: 250px;
    flex-shrink: 0;
  }}
  .logo-box {{
    border: 2px dashed #38BDF8;
    border-radius: 10px;
    width: 150px;
    height: 105px;
    color: #7DD3FC;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: monospace;
    font-weight: 600;
    background: rgba(56, 189, 248, 0.04);
  }}
  .header-center {{
    text-align: center;
    flex: 1;
    margin: 0 24px;
  }}
  .title-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }}
  .shield-svg {{
    width: 54px;
    height: 54px;
    filter: drop-shadow(0 4px 10px rgba(0, 196, 159, 0.45));
  }}
  .main-title {{
    font-size: 64px;
    font-weight: 900;
    letter-spacing: 3px;
    color: #FFFFFF;
    line-height: 1.1;
  }}
  .subtitle {{
    color: #38BDF8;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
    letter-spacing: 0.5px;
  }}
  .author-line {{
    color: #E2E8F0;
    font-size: 21px;
    margin-top: 10px;
  }}
  .author-line b {{
    color: #FFFFFF;
  }}
  .dept-line {{
    color: #94A3B8;
    font-size: 17px;
    margin-top: 4px;
  }}

  /* Main 3-Column Grid */
  main {{
    flex: 1;
    padding: 24px 36px;
    display: grid;
    grid-template-columns: 1fr 1fr 1.05fr;
    grid-column-gap: 24px;
    overflow: hidden;
  }}
  .column {{
    display: flex;
    flex-direction: column;
    gap: 18px;
    height: 100%;
  }}
  .column .card:last-child {{
    flex: 1;
  }}

  /* Generic Card Styles */
  .card {{
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.04);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}
  .card-header {{
    background: #0B1A2D;
    color: #FFFFFF;
    padding: 12px 20px;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }}
  .card-body {{
    padding: 18px 20px;
    font-size: 18px;
    line-height: 1.5;
    color: #1E293B;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}

  /* System Workflow Boxes */
  .wf-step {{
    background: #F0FDF9;
    border: 1.5px solid #CCFBF1;
    border-radius: 8px;
    padding: 11px 14px;
  }}
  .wf-step-title {{
    font-weight: 800;
    color: #0F172A;
    font-size: 18.5px;
    margin-bottom: 2px;
  }}
  .wf-step-desc {{
    font-size: 16px;
    color: #475569;
    line-height: 1.35;
  }}
  .wf-arrow {{
    text-align: center;
    color: #0D9488;
    font-size: 20px;
    font-weight: 900;
    line-height: 1;
    margin: 2px 0;
  }}

  /* Feature list */
  .feat-item {{
    margin-bottom: 16px;
  }}
  .feat-item:last-child {{
    margin-bottom: 0;
  }}
  .feat-item b {{
    color: #0F172A;
    font-size: 19px;
  }}
  .feat-item span {{
    color: #475569;
    font-size: 16.5px;
    display: block;
    margin-top: 2px;
    line-height: 1.35;
  }}

  /* Tables in Models & Results */
  .model-card {{
    border: 1.5px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 12px;
    background: #FFFFFF;
  }}
  .model-card:last-child {{
    margin-bottom: 0;
  }}
  .model-title {{
    font-weight: 800;
    font-size: 20px;
    color: #0F172A;
  }}
  .model-sub {{
    font-size: 15px;
    color: #64748B;
    margin: 2px 0 8px 0;
  }}
  .metrics-table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .metrics-table th {{
    font-size: 14px;
    font-weight: 800;
    color: #0D9488;
    padding: 3px 4px;
    text-align: center;
    letter-spacing: 0.5px;
  }}
  .metrics-table td {{
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    padding: 4px;
    text-align: center;
    font-family: monospace;
  }}

  /* Hybrid Risk Engine */
  .formula-box {{
    background: #E6F4F1;
    border: 1.5px solid #B2DFDB;
    border-radius: 8px;
    padding: 12px 14px;
    font-family: monospace;
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
  }}
  .risk-badges {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
  }}
  .risk-badge {{
    padding: 10px 4px;
    border-radius: 7px;
    color: white;
    text-align: center;
    font-weight: 900;
    font-size: 16px;
    line-height: 1.25;
    letter-spacing: 0.5px;
  }}
  .badge-low {{ background: #16A34A; }}
  .badge-med {{ background: #C2410C; }}
  .badge-high {{ background: #B91C1C; }}

  /* Feature importance bars */
  .bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    font-size: 17px;
  }}
  .bar-label {{
    width: 140px;
    font-family: monospace;
    font-weight: 700;
    color: #334155;
  }}
  .bar-track {{
    flex: 1;
    height: 19px;
    background: #E2E8F0;
    border-radius: 6px;
    overflow: hidden;
    margin: 0 12px;
  }}
  .bar-fill {{
    height: 100%;
    background: #0D9488;
    border-radius: 6px;
  }}
  .bar-val {{
    width: 45px;
    font-family: monospace;
    font-weight: 800;
    color: #0F172A;
    text-align: right;
  }}

  /* Screenshot Mockups */
  .mockup-card {{
    background: #F8FAFC;
    border: 1.5px solid #CBD5E1;
    border-radius: 8px;
    padding: 12px;
  }}
  .mockup-home-title {{
    font-size: 17.5px;
    font-weight: 800;
    text-align: center;
    color: #0F172A;
    margin-bottom: 3px;
  }}
  .mockup-home-sub {{
    font-size: 13.5px;
    color: #64748B;
    text-align: center;
    margin-bottom: 10px;
  }}
  .home-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }}
  .home-item {{
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 7px;
    padding: 10px 6px;
    text-align: center;
  }}
  .home-item-icon {{
    font-size: 16px;
    margin-bottom: 2px;
  }}
  .home-item-title {{
    font-size: 13.5px;
    font-weight: 800;
    color: #1E3A8A;
    letter-spacing: 0.5px;
  }}
  .home-item-desc {{
    font-size: 11px;
    color: #64748B;
    margin-top: 2px;
    line-height: 1.25;
  }}
  .home-btn {{
    display: inline-block;
    background: #1E40AF;
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 4px;
    margin-top: 6px;
  }}

  /* Result Mockup & Side-by-Side Flex */
  .fig2-container {{
    display: flex;
    gap: 14px;
    align-items: flex-start;
    margin-top: 10px;
  }}
  .fig2-mockup {{
    width: 53%;
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 7px;
    padding: 8px 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  }}
  .fig2-caption {{
    width: 47%;
    font-size: 15px;
    color: #475569;
    line-height: 1.45;
  }}
  .fig2-caption b {{
    color: #0F172A;
  }}

  .res-head {{
    font-size: 13px;
    font-weight: 800;
    text-align: center;
    color: #0F172A;
  }}
  .res-subhead {{
    font-size: 9.5px;
    color: #64748B;
    text-align: center;
    margin-bottom: 4px;
  }}
  .res-score-box {{
    background: #FEF2F2;
    border: 1.5px solid #FCA5A5;
    border-radius: 6px;
    padding: 6px 4px;
    text-align: center;
    margin: 4px 0 6px 0;
  }}
  .res-score-label {{
    font-size: 9.5px;
    color: #64748B;
    font-weight: 700;
  }}
  .res-score-num {{
    font-size: 22px;
    font-weight: 900;
    color: #DC2626;
  }}
  .res-bar {{
    height: 6px;
    background: #FEE2E2;
    border-radius: 3px;
    overflow: hidden;
    margin: 4px 14px;
  }}
  .res-bar-fill {{
    width: 78%;
    height: 100%;
    background: #DC2626;
  }}
  .res-badge {{
    font-size: 10px;
    font-weight: 900;
    color: #DC2626;
  }}
  .res-summary {{
    font-size: 10px;
    color: #334155;
    text-align: center;
    margin-bottom: 6px;
    line-height: 1.3;
  }}
  .res-box {{
    background: #F8FAFC;
    border-left: 3.5px solid #0284C7;
    padding: 4px 6px;
    font-size: 9.5px;
    margin-bottom: 4px;
    line-height: 1.25;
  }}
  .res-box-warn {{
    border-left-color: #DC2626;
    background: #FEF2F2;
  }}
  .caption {{
    font-size: 15px;
    color: #475569;
    margin-top: 8px;
    line-height: 1.4;
  }}
  .caption b {{
    color: #0F172A;
  }}

  /* Try It Live Card */
  .live-row {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}
  .qr-img {{
    width: 125px;
    height: 125px;
    border: 1.5px solid #CBD5E1;
    border-radius: 7px;
  }}
  .live-details {{
    flex: 1;
  }}
  .live-label {{
    font-size: 15.5px;
    color: #64748B;
  }}
  .live-url {{
    font-size: 18.5px;
    font-weight: 800;
    color: #0F172A;
    font-family: monospace;
    margin: 3px 0 8px 0;
    word-break: break-all;
  }}
  .code-url {{
    font-size: 15.5px;
    font-weight: 700;
    color: #2563EB;
    font-family: monospace;
    word-break: break-all;
  }}

  /* Tech Stack Pills */
  .pills-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .pill {{
    background: #F1F5F9;
    border: 1.5px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 15.5px;
    font-family: monospace;
    color: #0F172A;
    font-weight: 700;
  }}

  /* References */
  .ref-item {{
    font-size: 15px;
    color: #475569;
    margin-bottom: 10px;
    line-height: 1.4;
  }}
  .ref-item:last-child {{
    margin-bottom: 0;
  }}

  /* Bottom Footer */
  footer {{
    background: #0B132B;
    color: #FFFFFF;
    height: 70px;
    padding: 0 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }}
  .footer-left {{
    font-size: 19px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 0.3px;
  }}
  .footer-right {{
    font-size: 16.5px;
    font-style: italic;
    font-family: monospace;
    color: #38BDF8;
  }}
</style>
</head>
<body>

  <!-- Top Header Banner -->
  <header>
    <div class="logo-box">[College logo]</div>
    <div class="header-center">
      <div class="title-row">
        <!-- Crisp SVG Shield with Checkmark matching reference -->
        <svg class="shield-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L4 5V11.5C4 16.5 7.4 21.1 12 22.5C16.6 21.1 20 16.5 20 11.5V5L12 2Z" fill="#00C49F"/>
          <path d="M9.5 12L11 13.5L15 9.5" stroke="#0B132B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="main-title">SCAMSHIELD</div>
      </div>
      <div class="subtitle">AI-Based Scam Detection and Risk Assessment System</div>
      <div class="author-line"><b>Aniket Wandre</b> &bull; [Roll No &bull; Division] &bull; Guide: [Faculty Name]</div>
      <div class="dept-line">[College / Department] &bull; Machine Learning Lab Project</div>
    </div>
    <div class="logo-box" style="visibility: hidden;">[Spacer]</div>
  </header>

  <!-- Main 3 Columns -->
  <main>
    <!-- Column 1: Left -->
    <div class="column">
      
      <!-- Introduction -->
      <div class="card">
        <div class="card-header">Introduction</div>
        <div class="card-body">
          <p>Phishing, smishing and social-engineering fraud hit <b>older adults and non-technical users</b> hardest. Existing tools are jargon-heavy or invasive, and people need a simple, private way to check something <b>before</b> they click, share an OTP or transfer money.</p>
          <div style="margin-top: 14px; font-weight: 700; color: #0F172A;"><b>ScamShield</b> is a hybrid ML web app that:</div>
          <ol style="margin: 6px 0 0 22px; padding: 0; line-height: 1.48;">
            <li>Detects scams in SMS / WhatsApp, email, URLs and phone calls</li>
            <li>Reads screenshots with OCR</li>
            <li>Fuses ML and rules into a 0–100 risk score</li>
            <li>Explains the result in plain English</li>
          </ol>
        </div>
      </div>

      <!-- System Workflow -->
      <div class="card">
        <div class="card-header">System Workflow</div>
        <div class="card-body" style="gap: 2px;">
          <div class="wf-step"><div class="wf-step-title">1 &bull; Input</div><div class="wf-step-desc">SMS, email, URL, phone questionnaire or screenshot</div></div>
          <div class="wf-arrow">&darr;</div>
          <div class="wf-step"><div class="wf-step-title">2 &bull; Preprocess</div><div class="wf-step-desc">Text cleaning; OCR (WinOCR / Tesseract) and URL extraction</div></div>
          <div class="wf-arrow">&darr;</div>
          <div class="wf-step"><div class="wf-step-title">3 &bull; Analyse</div><div class="wf-step-desc">SMS, email and URL ML models, heuristic rules, phone matrix</div></div>
          <div class="wf-arrow">&darr;</div>
          <div class="wf-step"><div class="wf-step-title">4 &bull; Hybrid risk engine</div><div class="wf-step-desc">Weighted fusion into one score (0–100)</div></div>
          <div class="wf-arrow">&darr;</div>
          <div class="wf-step"><div class="wf-step-title">5 &bull; Result</div><div class="wf-step-desc">Risk level, "why this score" and what to do / not do</div></div>
        </div>
      </div>

      <!-- Key Features -->
      <div class="card">
        <div class="card-header">Key Features</div>
        <div class="card-body">
          <div class="feat-item"><b>Pre-click URL checks</b><span>17 structural and lexical features; the link is never opened</span></div>
          <div class="feat-item"><b>Screenshot OCR</b><span>Upload from phone or chat apps, no separate model needed</span></div>
          <div class="feat-item"><b>Accessible UI</b><span>Font sizing, high contrast, dyslexia font, dark mode</span></div>
          <div class="feat-item"><b>Three languages</b><span>English, Hindi and Marathi Interface</span></div>
          <div class="feat-item"><b>Privacy masking</b><span>Card numbers, CVVs and OTPs are masked</span></div>
          <div class="feat-item"><b>Learn, history and report</b><span>Scam tips, scan history and a reporting page</span></div>
        </div>
      </div>

    </div>

    <!-- Column 2: Center -->
    <div class="column">
      
      <!-- Models & Results -->
      <div class="card">
        <div class="card-header">Models &amp; Results</div>
        <div class="card-body">
          <div class="model-card">
            <div class="model-title">SMS</div>
            <div class="model-sub">TF-IDF (1–2 grams) + Logistic Regression &bull; SMS Spam Collection, 5,572 messages</div>
            <table class="metrics-table">
              <tr><th>ACC</th><th>PREC</th><th>REC</th><th>F1</th><th>AUC</th></tr>
              <tr><td>98.90</td><td>94.35</td><td>96.69</td><td>95.51</td><td>0.996</td></tr>
            </table>
          </div>
          <div class="model-card">
            <div class="model-title">Email</div>
            <div class="model-sub">TF-IDF (1–2 grams) + Logistic Regression &bull; 82,486 emails (40k balanced sample)</div>
            <table class="metrics-table">
              <tr><th>ACC</th><th>PREC</th><th>REC</th><th>F1</th><th>AUC</th></tr>
              <tr><td>98.55</td><td>98.28</td><td>98.94</td><td>98.61</td><td>0.999</td></tr>
            </table>
          </div>
          <div class="model-card">
            <div class="model-title">URL</div>
            <div class="model-sub">Random Forest (100 trees, 17 features) &bull; 632,508 URLs (40k balanced sample)</div>
            <table class="metrics-table">
              <tr><th>ACC</th><th>PREC</th><th>REC</th><th>F1</th><th>AUC</th></tr>
              <tr><td>98.80</td><td>99.59</td><td>97.96</td><td>98.77</td><td>0.998</td></tr>
            </table>
          </div>
          <div style="font-size: 14.5px; color: #64748B; margin-top: 8px; font-style: italic;">Metrics in %, on held-out test data (80/20 split).</div>
        </div>
      </div>

      <!-- Hybrid Risk Engine -->
      <div class="card">
        <div class="card-header">Hybrid Risk Engine</div>
        <div class="card-body">
          <div class="formula-box">Risk = 0.50 &middot; P(text) + 0.30 &middot; P(URL) + 0.20 &middot; Rules</div>
          <div class="risk-badges">
            <div class="risk-badge badge-low">0–29<br/>LOW</div>
            <div class="risk-badge badge-med">30–59<br/>MEDIUM</div>
            <div class="risk-badge badge-high">60–100<br/>HIGH</div>
          </div>
          <p style="font-size: 16.5px; color: #334155; line-height: 1.45;"><b>Phone calls</b> use a weighted <b>10-question matrix</b> (pressure, OTP requests, impersonation, remote access) instead of a trained model.</p>
        </div>
      </div>

      <!-- What the URL Model Learned -->
      <div class="card">
        <div class="card-header">What the URL Model Learned</div>
        <div class="card-body">
          <div class="bar-row"><div class="bar-label">has_https</div><div class="bar-track"><div class="bar-fill" style="width: 69%;"></div></div><div class="bar-val">0.69</div></div>
          <div class="bar-row"><div class="bar-label">subdomains</div><div class="bar-track"><div class="bar-fill" style="width: 12%;"></div></div><div class="bar-val">0.12</div></div>
          <div class="bar-row"><div class="bar-label">special chars</div><div class="bar-track"><div class="bar-fill" style="width: 4%;"></div></div><div class="bar-val">0.04</div></div>
          <div style="font-size: 14.5px; color: #64748B; margin-top: 6px;">Top Random Forest feature importances.</div>
        </div>
      </div>

      <!-- Limitations & Future Work -->
      <div class="card">
        <div class="card-header">Limitations &amp; Future Work</div>
        <div class="card-body">
          <p style="margin-bottom: 12px;">
            Models are trained on English text, and brand-new URL tricks may score only medium without reputation lookups.
          </p>
          <p>
            <b>Next:</b> multilingual models, a browser extension, URL reputation lookups and live call-transcript guidance.
          </p>
        </div>
      </div>

    </div>

    <!-- Column 3: Right -->
    <div class="column">
      
      <!-- Application Screenshots -->
      <div class="card">
        <div class="card-header">Application Screenshots</div>
        <div class="card-body">
          <!-- Fig. 1 Mockup Card -->
          <div class="mockup-card">
            <div class="mockup-home-title">What would you like to check today?</div>
            <div class="mockup-home-sub">Check suspicious messages, emails, links, and phone calls before you act or click.</div>
            <div class="home-grid">
              <div class="home-item">
                <div class="home-item-icon">&#128172;</div>
                <div class="home-item-title">CHECK SMS</div>
                <div class="home-item-desc">Check a suspicious SMS or WhatsApp message.</div>
                <div class="home-btn">Check Message &rarr;</div>
              </div>
              <div class="home-item">
                <div class="home-item-icon">&#9993;</div>
                <div class="home-item-title">CHECK EMAIL</div>
                <div class="home-item-desc">Check an email for suspicious or phishing content.</div>
                <div class="home-btn">Check Email &rarr;</div>
              </div>
              <div class="home-item">
                <div class="home-item-icon">&#128279;</div>
                <div class="home-item-title">CHECK URL</div>
                <div class="home-item-desc">Check whether a website link appears suspicious.</div>
                <div class="home-btn">Check Link &rarr;</div>
              </div>
              <div class="home-item">
                <div class="home-item-icon">&#128222;</div>
                <div class="home-item-title">CHECK PHONE CALL</div>
                <div class="home-item-desc">Answer a few questions about a suspicious call.</div>
                <div class="home-btn">Start Questions &rarr;</div>
              </div>
            </div>
          </div>
          <div class="caption"><b>Fig. 1</b> Home: four check options, a 3-step guide and an EN / MR / HI switch.</div>

          <!-- Fig. 2 Side-by-Side Flex -->
          <div class="fig2-container">
            <div class="fig2-mockup">
              <div class="res-head">ScamShield Assessment Result</div>
              <div class="res-subhead">Inspection Report &bull; Verified Evaluation Pipeline</div>
              <div class="res-score-box">
                <div class="res-score-label">ESTIMATED RISK SCORE</div>
                <div class="res-score-num">78 <span style="font-size: 13px; color: #64748B;">/ 100</span></div>
                <div class="res-bar"><div class="res-bar-fill"></div></div>
                <div class="res-badge">&#9888; POTENTIAL SCAM - HIGH RISK</div>
              </div>
              <div class="res-summary">High likelihood of scam or phishing attempt. Do not share information or click links.</div>
              <div class="res-box"><b>Why Did We Give This Score?</b><br/>Urgent threat of account deactivation; suspicious short-link.</div>
              <div class="res-box res-box-warn"><b>What Should You Do Now?</b><br/>Do NOT click the link. Never share OTP or netbanking password.</div>
            </div>
            <div class="fig2-caption">
              <b>Fig. 2</b> Result for a phishing email: score 78 / 100 (High Risk), highlighted trigger words, &ldquo;Why did we give this score?&rdquo; and &ldquo;What should you do now?&rdquo;.
            </div>
          </div>
        </div>
      </div>

      <!-- Try It Live -->
      <div class="card">
        <div class="card-header">Try It Live</div>
        <div class="card-body">
          <div class="live-row">
            <img src="data:image/png;base64,{qr_b64}" class="qr-img" alt="QR Code">
            <div class="live-details">
              <div class="live-label">Scan to open the deployed app:</div>
              <div class="live-url">scamshield-ozpr.onrender.com</div>
              <div class="live-label">Code:</div>
              <div class="code-url">github.com/aniketwandre05/ScamShield</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="card">
        <div class="card-header">Tech Stack</div>
        <div class="card-body">
          <div class="pills-container">
            <span class="pill">Python</span><span class="pill">Flask</span><span class="pill">scikit-learn</span>
            <span class="pill">pandas</span><span class="pill">NumPy</span><span class="pill">Tesseract / WinOCR</span>
            <span class="pill">HTML</span><span class="pill">CSS</span><span class="pill">JS</span><span class="pill">pytest</span>
            <span class="pill">Docker</span><span class="pill">Render</span>
          </div>
        </div>
      </div>

      <!-- Datasets & References -->
      <div class="card">
        <div class="card-header">Datasets &amp; References</div>
        <div class="card-body">
          <div class="ref-item">[1] SMS Spam Collection (UCI ML Repository / Kaggle), 5,572 messages</div>
          <div class="ref-item">[2] Phishing Email Dataset, 82,486 labelled emails (Enron + Nazario)</div>
          <div class="ref-item">[3] Balanced Malicious &amp; Benign URLs Dataset, 632,508 URLs</div>
          <div class="ref-item">[4] Pedregosa et al., "Scikit-learn: Machine Learning in Python", JMLR 12, 2011.</div>
        </div>
      </div>

    </div>
  </main>

  <!-- Bottom Footer -->
  <footer>
    <div class="footer-left">Prevention first: three ML models plus transparent rules, explained in plain English.</div>
    <div class="footer-right">Estimated risk, not a guarantee</div>
  </footer>

</body>
</html>"""
    
    html_path = os.path.join(BASE_DIR, 'poster_render.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path

def render_poster():
    html_path = build_poster_html()
    output_png = os.path.join(BASE_DIR, 'ScamShield_Project_Poster.png')
    output_pdf = os.path.join(BASE_DIR, 'ScamShield_Project_Poster.pdf')
    
    edge_paths = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    ]
    browser = None
    for p in edge_paths:
        if os.path.exists(p):
            browser = p
            break
            
    if not browser:
        raise RuntimeError("No Chromium/Edge browser found for high-res rendering.")
        
    print(f"Rendering poster using {browser}...")
    
    # 1. Render High-Resolution PNG (1600 x 2400 px)
    cmd_png = [
        browser,
        '--headless',
        f'--screenshot={output_png}',
        '--window-size=1600,2400',
        '--hide-scrollbars',
        '--disable-gpu',
        f'file:///{html_path}'
    ]
    subprocess.run(cmd_png, check=True)
    
    # 2. Render Single-Page Vector PDF
    cmd_pdf = [
        browser,
        '--headless',
        f'--print-to-pdf={output_pdf}',
        '--no-pdf-header-footer',
        f'file:///{html_path}'
    ]
    subprocess.run(cmd_pdf, check=True)
    
    if os.path.exists(output_png) and os.path.exists(output_pdf):
        print(f"Generated PNG: {output_png} ({os.path.getsize(output_png)} bytes)")
        print(f"Generated PDF: {output_pdf} ({os.path.getsize(output_pdf)} bytes)")
        
        # Copy both to Downloads folder
        dst_png = r'c:\Users\anike\Downloads\ScamShield_Project_Poster.png'
        dst_pdf = r'c:\Users\anike\Downloads\ScamShield_Project_Poster.pdf'
        shutil.copy2(output_png, dst_png)
        shutil.copy2(output_pdf, dst_pdf)
        print(f"Copied poster PNG to: {dst_png}")
        print(f"Copied poster PDF to: {dst_pdf}")
    else:
        print("Error: Output files not created.")

if __name__ == '__main__':
    render_poster()
