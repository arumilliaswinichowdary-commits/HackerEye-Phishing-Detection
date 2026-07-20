import re
from urllib.parse import urlparse

def extract_features(url):

    parsed = urlparse(url)

    hostname = parsed.netloc

    path = parsed.path

    features = [

        len(url),                              # URL Length

        1 if parsed.scheme == "https" else 0,  # HTTPS

        url.count("."),                        # Number of dots

        url.count("-"),                        # Hyphens

        url.count("@"),                        # @ Symbol

        url.count("?"),                        # Question Mark

        url.count("&"),                        # Ampersand

        url.count("="),                        # Equal Symbol

        url.count("%"),                        # %

        url.count("_"),                        # Underscore

        sum(c.isdigit() for c in url),         # Digits

        len(hostname),                         # Host Length

        len(path),                             # Path Length

        hostname.count("."),                   # Subdomains

        1 if re.search(r"\d+\.\d+\.\d+\.\d+", hostname) else 0,  # IP Address

        1 if "login" in url.lower() else 0,

        1 if "verify" in url.lower() else 0,

        1 if "account" in url.lower() else 0,

        1 if "update" in url.lower() else 0,

        1 if "secure" in url.lower() else 0

    ]

    return features