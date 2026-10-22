import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

img_dir = Path("wireframes/images")
img_dir.mkdir(parents=True, exist_ok=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not Path(chrome_path).exists():
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

screens = [
    ("index.html", "00_master_gallery.png", 1800, 2500),
    ("home.html", "01_home_dashboard.png", 1800, 1850),
    ("sms.html", "02_check_sms.png", 1800, 1950),
    ("email.html", "03_check_email.png", 1800, 2050),
    ("url.html", "04_check_url_qr.png", 1800, 1950),
    ("phone.html", "05_check_phone.png", 1800, 2050),
    ("result_high.html", "06_result_high_risk.png", 1800, 2250),
    ("result_medium.html", "07_result_medium_risk.png", 1800, 2050),
    ("result_low.html", "08_result_low_risk.png", 1800, 2050),
    ("history.html", "09_scan_history.png", 1800, 1850),
    ("learn.html", "10_learning_center.png", 1800, 2500),
    ("report.html", "11_report_helplines.png", 1800, 2050),
    ("error.html", "12_error_recovery.png", 1800, 1650),
    ("overlays.html", "13_ui_overlays.png", 1800, 1650),
    ("flow.html", "14_user_flow_map.png", 1800, 2250),
]

print(f"Generating screenshots for {len(screens)} wireframe screens using: {chrome_path}")
print("=" * 75)

for html_file, img_file, width, height in screens:
    input_path = Path("wireframes") / html_file
    output_path = img_dir / img_file
    
    if not input_path.exists():
        print(f"[MISSING] {input_path}")
        continue

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        f"--screenshot={output_path.resolve()}",
        input_path.resolve().as_uri()
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if output_path.exists() and output_path.stat().st_size > 1000:
        size_kb = output_path.stat().st_size / 1024
        print(f"  [OK] {html_file:<18} -> {img_file:<25} ({size_kb:6.1f} KB)")
    else:
        print(f"  [FAILED] {html_file} -> Return Code: {res.returncode}")

print("=" * 75)
print("All wireframe images generated in wireframes/images/ successfully!")
