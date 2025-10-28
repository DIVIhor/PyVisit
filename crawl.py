from urllib.parse import urlparse, ParseResult

from bs4 import BeautifulSoup as BS
from bs4._typing import _AtMostOneElement
from bs4.element import Tag


def normalize_url(url: str) -> str:
    """Normalize received URL to format HOST/PATH"""
    parsed_url: ParseResult = urlparse(url)
    normalized_url = f"{parsed_url.netloc}{parsed_url.path.removesuffix('/')}"

    return normalized_url.lower()

def extract_text_from_tag(tag: _AtMostOneElement) -> str:
    """Check if the `tag` is of the correct type and extract inner text,
    trimming any spaces
    """
    if isinstance(tag, Tag):
        return tag.get_text(strip=True)
    
    return ""

def get_h1_from_html(html: str) -> str:
    """Extract heading text from the HTML"""
    soup: BS = BS(html, "lxml")
    heading: str = ""
    h1 = soup.find("h1")
    heading = extract_text_from_tag(h1)

    return heading

def get_first_paragraph_from_html(html: str) -> str:
    """Extract text from the first paragraph of the HTML"""
    soup: BS = BS(html, "lxml")
    paragraph: str = ""
    main = soup.find("main")

    # try to find paragraph inside main tag
    if main is not None:
        p = main.find_next("p")
        paragraph = extract_text_from_tag(p)

    # try to find paragraph outside of main tag
    if not paragraph:
        p = soup.find("p")
        paragraph = extract_text_from_tag(p)

    return paragraph
