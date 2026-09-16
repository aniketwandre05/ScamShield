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


def extract_text_from_image(image_input: Union[str, bytes, Image.Image], lang: str = "en") -> Dict[str, Any]:
    """
    Extracts text from screenshot using available local OCR engine.
    Supports English ('en'), Marathi ('mr'), and Hindi ('hi') with fallback.
    Applies image enhancement preprocessing first.
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

    # Map ScamShield language codes to OCR language tags
    ocr_lang_map = {
        "en": "en",
        "mr": "mr",
        "hi": "hi"
    }
    target_ocr_lang = ocr_lang_map.get(lang, "en")

    # Try Windows Native OCR first
    if HAS_WINOCR:
        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Try target language first, then fallback to 'en'
            for lang_code in [target_ocr_lang, "en"] if target_ocr_lang != "en" else ["en"]:
                try:
                    if loop.is_running():
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as pool:
                            result = pool.submit(lambda: asyncio.run(winocr.recognize_pil(processed_img, lang_code))).result()
                    else:
                        result = loop.run_until_complete(winocr.recognize_pil(processed_img, lang_code))

                    if result and hasattr(result, 'text') and result.text.strip():
                        extracted_text = result.text.strip()
                        engine_used = f"winocr ({lang_code})"
                        break
                except Exception:
                    continue
        except Exception:
            pass

    # Fallback to Tesseract if needed
    if not extracted_text and HAS_PYTESSERACT:
        try:
            for t_lang in [f"{target_ocr_lang}+eng", "eng"] if target_ocr_lang != "en" else ["eng"]:
                try:
                    extracted_text = pytesseract.image_to_string(processed_img, lang=t_lang).strip()
                    if extracted_text:
                        engine_used = f"pytesseract ({t_lang})"
                        break
                except Exception:
                    continue
        except Exception:
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
