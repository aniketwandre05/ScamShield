"""
Optical Character Recognition (OCR) Engine
Extracts text from screenshots using local Windows Native OCR or Tesseract with robust fallback.
"""

import os
import sys
import asyncio
from pathlib import Path
from PIL import Image
from typing import Dict, Any, Union

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ocr.image_preprocessing import preprocess_image_for_ocr

# Check for winocr availability
try:
    import winocr
    HAS_WINOCR = True
except ImportError:
    HAS_WINOCR = False

# Check for pytesseract availability
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False


def extract_text_from_image(image_input: Union[str, bytes, Image.Image]) -> Dict[str, Any]:
    """
    Extracts text from screenshot using available local OCR engine.
    Applies image enhancement preprocessing first.
    Returns:
        {
            "success": bool,
            "text": str,
            "char_count": int,
            "engine": str,
            "error": Optional[str]
        }
    """
    try:
        # 1. Preprocess
        processed_img = preprocess_image_for_ocr(image_input)
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "char_count": 0,
            "engine": "none",
            "error": f"Failed to load or preprocess image: {str(e)}"
        }

    extracted_text = ""
    engine_used = "none"

    # Try Windows Native OCR first
    if HAS_WINOCR:
        try:
            # winocr requires an event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    result = pool.submit(lambda: asyncio.run(winocr.recognize_pil(processed_img, 'en'))).result()
            else:
                result = loop.run_until_complete(winocr.recognize_pil(processed_img, 'en'))

            if result and hasattr(result, 'text'):
                extracted_text = result.text.strip()
                engine_used = "winocr (Windows Native OCR)"
        except Exception as e:
            # Fallback to pytesseract if winocr fails
            pass

    # Fallback to Tesseract if needed
    if not extracted_text and HAS_PYTESSERACT:
        try:
            extracted_text = pytesseract.image_to_string(processed_img).strip()
            if extracted_text:
                engine_used = "pytesseract"
        except Exception as e:
            pass

    if not extracted_text:
        return {
            "success": False,
            "text": "",
            "char_count": 0,
            "engine": engine_used,
            "error": "We could not clearly read any text in this screenshot. Please upload a clearer image or paste the text manually."
        }

    return {
        "success": True,
        "text": extracted_text,
        "char_count": len(extracted_text),
        "engine": engine_used,
        "error": None
    }
