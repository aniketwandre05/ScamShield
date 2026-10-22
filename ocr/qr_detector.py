"""
QR Code Detection & Parsing Module
Extracts URL payloads, UPI payment strings, and embedded web links from uploaded screenshots.
Protects against 'Quishing' (QR code phishing) attacks.
"""

import re
import os
from typing import Dict, Any, Optional, Union
from pathlib import Path
from PIL import Image
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# Regex to detect URLs inside decoded QR payloads
URL_REGEX = re.compile(
    r'(https?://[^\s<>"]+|www\.[^\s<>"]+|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s<>"]*)?)',
    re.IGNORECASE
)


def extract_qr_code(image_input: Union[str, Path, bytes, Image.Image]) -> Dict[str, Any]:
    """
    Scans the provided image for a 2D QR Code.
    If detected, decodes the payload and identifies any web URLs or UPI payment URIs.
    
    Returns:
    {
        "found": bool,
        "payload": str,
        "extracted_url": str,
        "is_upi": bool,
        "is_url": bool,
        "error": Optional[str]
    }
    """
    if not HAS_CV2:
        return {
            "found": False,
            "payload": "",
            "extracted_url": "",
            "is_upi": False,
            "is_url": False,
            "error": "OpenCV is not available for QR detection."
        }

    try:
        # 1. Convert input to a PIL Image first
        if isinstance(image_input, (str, Path)):
            pil_img = Image.open(str(image_input)).convert("RGB")
        elif isinstance(image_input, bytes):
            import io
            pil_img = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, Image.Image) or hasattr(image_input, "convert"):
            pil_img = image_input.convert("RGB")
        elif hasattr(image_input, "get_image"):
            pil_img = image_input.get_image().convert("RGB")
        else:
            return {
                "found": False,
                "payload": "",
                "extracted_url": "",
                "is_upi": False,
                "is_url": False,
                "error": "Invalid image input format."
            }

        # Convert PIL Image to OpenCV BGR numpy array
        cv_img = np.array(pil_img)[:, :, ::-1].copy()

        detector = cv2.QRCodeDetector()

        # Attempt 1: Standard color image
        val, pts, _ = detector.detectAndDecode(cv_img)
        
        # Attempt 2: Grayscale image if not found
        if not val or not val.strip():
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            val, pts, _ = detector.detectAndDecode(gray)

        # Attempt 3: Contrast stretched / adaptive threshold if still not found
        if not val or not val.strip():
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 10
            )
            val, pts, _ = detector.detectAndDecode(thresh)

        payload = (val or "").strip()
        if not payload:
            return {
                "found": False,
                "payload": "",
                "extracted_url": "",
                "is_upi": False,
                "is_url": False,
                "error": None
            }

        # 2. Inspect payload content
        is_upi = payload.lower().startswith("upi://")
        is_url = bool(re.match(r'^https?://', payload, re.IGNORECASE))
        extracted_url = ""

        if is_url:
            extracted_url = payload
        elif is_upi:
            # For UPI payloads, e.g. upi://pay?pa=recipient@bank&pn=Merchant&am=1000
            # URL model evaluates the URI structure and domain parameters
            extracted_url = payload
        else:
            # Check if payload contains an embedded URL
            match = URL_REGEX.search(payload)
            if match:
                extracted_url = match.group(1)
                is_url = True
            elif "." in payload and " " not in payload and len(payload) > 4:
                # e.g. domain.com/login without scheme
                extracted_url = "http://" + payload
                is_url = True
            else:
                extracted_url = payload

        return {
            "found": True,
            "payload": payload,
            "extracted_url": extracted_url,
            "is_upi": is_upi,
            "is_url": is_url,
            "error": None
        }

    except Exception as e:
        return {
            "found": False,
            "payload": "",
            "extracted_url": "",
            "is_upi": False,
            "is_url": False,
            "error": f"QR decoding error: {str(e)}"
        }
