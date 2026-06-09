def extract_features(url):

    url_length = len(url)

    https = 1 if "https://" in url else 0

    at_symbol = 1 if "@" in url else 0

    dots = url.count(".")

    double_slash = 1 if "//" in url[8:] else 0

    return [
        url_length,
        https,
        at_symbol,
        dots,
        double_slash
    ]