"""
Text Preprocessing and URL Extraction Utility
Handles text cleaning, tokenization normalization, HTML tag removal, and regex-based URL detection.
"""

import re
import html
from typing import List, Tuple
from urllib.parse import urlparse

# Regular expression to accurately match URLs in text
URL_REGEX = re.compile(
    r'(?:https?://|www\.)[a-zA-Z0-9.\-_~:/?#[\]@!$&\'()*+,;=%]+',
    re.IGNORECASE
)

# HTML tags regex
HTML_TAG_REGEX = re.compile(r'<[^>]+>')

# Excessive whitespace regex
WHITESPACE_REGEX = re.compile(r'\s+')


def clean_text(text: str) -> str:
    """
    Standard text cleaning pipeline for SMS and Email text:
    - Decodes HTML entities
    - Removes HTML tags
    - Converts to lowercase
    - Normalizes multiple whitespaces
    """
    if not isinstance(text, str):
        return ""
    
    # Decode HTML entities (&amp; -> &, &lt; -> <, etc.)
    text = html.unescape(text)
    
    # Strip HTML tags
    text = HTML_TAG_REGEX.sub(' ', text)
    
    # Lowercase
    text = text.lower()
    
    # Normalize whitespaces
    text = WHITESPACE_REGEX.sub(' ', text).strip()
    
    return text


def extract_urls(text: str) -> List[str]:
    """
    Extracts all valid URLs and domain links from a text string.
    Handles OCR artifact recovery (e.g. 'https-//' or 'https ://').
    Normalizes 'www.' to 'https://www.' for secure parsing.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    
    # Pre-normalize common OCR substitution patterns on protocol schemes
    normalized_input = re.sub(r'https?[\s:;\-_~.]+/{1,2}', lambda m: 'https://' if 'https' in m.group(0).lower() else 'http://', text, flags=re.IGNORECASE)
    normalized_input = re.sub(r'https?://\s+', 'https://', normalized_input, flags=re.IGNORECASE)
    
    raw_urls = URL_REGEX.findall(normalized_input)
    normalized_urls = []
    seen = set()
    
    for url in raw_urls:
        # Strip trailing punctuation that often attaches to URLs in messages
        url = url.rstrip('.,!?:;)"\'>]}')
        if url.startswith(('www.', 'WWW.')):
            url = 'https://' + url
            
        # Ensure URL contains a valid domain structure (at least one dot in host)
        domain_part = url.split('://', 1)[-1].split('/', 1)[0].split('?', 1)[0]
        if '.' in domain_part and len(domain_part) >= 4 and not domain_part.endswith('.'):
            if url not in seen:
                seen.add(url)
                normalized_urls.append(url)
            
    return normalized_urls


def clean_and_extract(text: str) -> Tuple[str, List[str]]:
    """
    Cleans the given text and extracts any embedded URLs.
    Returns (cleaned_text, list_of_urls).
    """
    urls = extract_urls(text)
    cleaned = clean_text(text)
    return cleaned, urls
