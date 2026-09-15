"""
Unit and Integration Tests for OCR Pipeline and Content Detection
"""

import pytest
from pathlib import Path
from ocr.ocr_engine import extract_text_from_image
from ocr.content_detector import detect_content_structure
from config import DEMO_SAMPLES_DIR


def test_ocr_extraction_on_sample_sms():
    sample_img = DEMO_SAMPLES_DIR / "screenshots" / "sample_sms_scam.png"
    assert sample_img.exists()
    
    res = extract_text_from_image(str(sample_img))
    assert res["success"] is True
    assert len(res["text"]) > 20
    
    # Check content detector on OCR text
    structure = detect_content_structure(res["text"])
    assert structure["has_urls"] is True
    assert len(structure["urls"]) >= 1


def test_ocr_extraction_on_sample_email():
    sample_img = DEMO_SAMPLES_DIR / "screenshots" / "sample_email_phish.png"
    assert sample_img.exists()
    
    res = extract_text_from_image(str(sample_img))
    assert res["success"] is True
    assert len(res["text"]) > 20
    
    structure = detect_content_structure(res["text"])
    assert structure["primary_type"] == "email"


def test_ocr_invalid_image_path():
    res = extract_text_from_image("non_existent_file.png")
    assert res["success"] is False
    assert res["error"] is not None
