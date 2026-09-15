"""
URL Feature Extraction Module
Extracts 17 handcrafted lexical, structural, and domain features from a URL for classical ML classification.
"""

import re
from urllib.parse import urlparse
import numpy as np
import pandas as pd
from typing import Dict, Any, List

# Known URL shorteners
SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "buff.ly", "ow.ly", "cutt.ly",
    "tiny.cc", "goo.gl", "bit.do", "shorte.st", "adf.ly", "bc.vc", "rb.gy"
}

# Suspicious keywords often present in malicious/phishing URLs
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "verification", "account", "update", "bank", "secure",
    "banking", "signin", "security", "free", "reward", "win", "winner", "prize",
    "claim", "bonus", "otp", "kyc", "billing", "support", "service", "wallet",
    "crypto", "recover", "unlock", "suspended", "confirm", "alert", "ebayisapi",
    "paypal", "appleid", "netflix", "microsoft", "amazon", "chase", "wellsfargo"
]

# IPv4 Regex pattern
IP_REGEX = re.compile(
    r'^(?:http[s]?://)?(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::[0-9]+)?(?:/.*)?$'
)

FEATURE_NAMES = [
    "url_length",
    "hostname_length",
    "path_length",
    "query_length",
    "count_dots",
    "count_hyphens",
    "count_at",
    "count_question",
    "count_equal",
    "count_slash",
    "count_digits",
    "count_special_chars",
    "subdomain_count",
    "has_https",
    "has_ip_address",
    "is_shortened",
    "suspicious_keyword_count"
]


def extract_url_features(url: str) -> Dict[str, Any]:
    """
    Extracts numerical and boolean lexical features from a URL string safely.
    Handles un-schemed strings gracefully by prepending http://.
    """
    if not isinstance(url, str) or not url.strip():
        # Default zero features for empty input
        return {k: 0 for k in FEATURE_NAMES}

    url = url.strip()
    
    # Prepend http if scheme missing for standard parsing
    parse_target = url
    if not url.startswith(("http://", "https://", "ftp://")):
        parse_target = "http://" + url

    try:
        parsed = urlparse(parse_target)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
    except Exception:
        hostname = ""
        path = ""
        query = ""

    # 1. Length features
    url_length = len(url)
    hostname_length = len(hostname)
    path_length = len(path)
    query_length = len(query)

    # 2. Character counts
    count_dots = url.count('.')
    count_hyphens = url.count('-')
    count_at = url.count('@')
    count_question = url.count('?')
    count_equal = url.count('=')
    count_slash = url.count('/')
    count_digits = sum(c.isdigit() for c in url)
    count_special_chars = sum(not c.isalnum() for c in url)

    # 3. Subdomain count
    subdomains = hostname.split('.')
    # e.g., 'sub.example.com' has 3 parts -> 1 subdomain level
    subdomain_count = max(0, len(subdomains) - 2) if len(subdomains) > 2 else 0

    # 4. HTTPS presence
    has_https = 1 if url.lower().startswith("https://") else 0

    # 5. IP Address usage in host
    has_ip_address = 1 if IP_REGEX.match(url) or (hostname and re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', hostname)) else 0

    # 6. Shortener detection
    is_shortened = 1 if any(hostname.lower() == s or hostname.lower().endswith("." + s) for s in SHORTENERS) else 0

    # 7. Suspicious keyword count
    url_lower = url.lower()
    suspicious_keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)

    return {
        "url_length": url_length,
        "hostname_length": hostname_length,
        "path_length": path_length,
        "query_length": query_length,
        "count_dots": count_dots,
        "count_hyphens": count_hyphens,
        "count_at": count_at,
        "count_question": count_question,
        "count_equal": count_equal,
        "count_slash": count_slash,
        "count_digits": count_digits,
        "count_special_chars": count_special_chars,
        "subdomain_count": subdomain_count,
        "has_https": has_https,
        "has_ip_address": has_ip_address,
        "is_shortened": is_shortened,
        "suspicious_keyword_count": suspicious_keyword_count,
    }


def url_to_feature_vector(url: str) -> np.ndarray:
    """Converts a URL to a 1D numpy array of features in FEATURE_NAMES order."""
    features = extract_url_features(url)
    return np.array([features[name] for name in FEATURE_NAMES], dtype=float).reshape(1, -1)


def urls_to_feature_dataframe(urls: List[str]) -> pd.DataFrame:
    """Converts a list of URLs to a pandas DataFrame of extracted features."""
    data = [extract_url_features(u) for u in urls]
    return pd.DataFrame(data, columns=FEATURE_NAMES)
