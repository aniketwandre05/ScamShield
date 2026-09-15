"""
Image Preprocessing for Optical Character Recognition (OCR)
Enhances screenshot quality through grayscaling, contrast boosting, and adaptive thresholding.
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
from typing import Union, Tuple


def preprocess_image_for_ocr(image_input: Union[str, bytes, Image.Image]) -> Image.Image:
    """
    Standard OCR image preprocessing pipeline:
    1. Load image (from path, bytes, or PIL object)
    2. Convert RGBA/Palette to RGB
    3. Resize if image is excessively large or very small
    4. Convert to Grayscale
    5. Enhance Contrast & Sharpness
    6. Return optimized PIL Image
    """
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, bytes):
        img = Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, Image.Image):
        img = image_input.copy()
    else:
        raise ValueError("Unsupported image input type for OCR preprocessing")

    # Handle transparent alpha channels by blending onto white background
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[3])
        img = background
    else:
        img = img.convert('RGB')

    # Resize if too large (e.g. > 2400px width/height) to conserve memory
    max_dimension = 2400
    if max(img.size) > max_dimension:
        ratio = max_dimension / float(max(img.size))
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    elif min(img.size) < 400:
        # Scale up very small screenshots to improve OCR character recognition
        ratio = 600 / float(min(img.size))
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.BICUBIC)

    # Convert to Grayscale
    gray = ImageOps.grayscale(img)

    # Boost Contrast
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(1.8)

    # Boost Sharpness
    sharp_enhancer = ImageEnhance.Sharpness(high_contrast)
    sharpened = sharp_enhancer.enhance(1.5)

    return sharpened
