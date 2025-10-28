from urllib.parse import urlparse, ParseResult


def normalize_url(url: str) -> str:
    """Normalize received URL to format HOST/PATH"""
    parsed_url: ParseResult = urlparse(url)
    normalized_url = f"{parsed_url.netloc}{parsed_url.path.removesuffix('/')}"

    return normalized_url.lower()
