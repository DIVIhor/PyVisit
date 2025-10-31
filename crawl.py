from urllib.parse import urljoin, urlparse, ParseResult

from bs4 import BeautifulSoup as BS
from bs4._typing import _AtMostOneElement
from bs4.element import PageElement, Tag, ResultSet


PARSER: str = "lxml"


def extract_page_data(html: str, page_url: str) -> dict[str, str | list[str]]:
    """Extract and return a dictionary with the following parameters:
    - `url` - current URL
    - `h1` - main heading text
    - `first_paragraph` - text block from the first paragraph
    - `outgoing_links` - a list of URLs from anchors
    - `image_urls` - a list of URLs from images
    """
    page_data: dict[str, str | list[str]] = {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

    return page_data


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    """Find all anchors in the HTML and extract their references.
    Return a list of un-normalized URLs.
    """
    soup: BS = BS(html, PARSER)
    anchors: ResultSet[PageElement] = soup.find_all("a")
    links: list[str] = []
    for a in anchors:
        if isinstance(a, Tag):
            url: str = str(a.get("href", ""))
            parsed_url: ParseResult = urlparse(url)
            links.append(urljoin(base_url, parsed_url.path))

    return links


def get_images_from_html(html: str, base_url: str) -> list[str]:
    """Find all image tags in the HTML and extract their sources.
    Return a list of un-normalized URLs.
    """
    soup: BS = BS(html, PARSER)
    images: ResultSet[PageElement] = soup.find_all("img")
    links: list[str] = []
    for img in images:
        if isinstance(img, Tag):
            url: str = str(img.get("src", ""))
            parsed_url: ParseResult = urlparse(url)
            links.append(urljoin(base_url, parsed_url.path))

    return links


def get_h1_from_html(html: str) -> str:
    """Extract heading text from the HTML"""
    soup: BS = BS(html, PARSER)
    heading: str = ""
    h1 = soup.find("h1")
    heading = extract_text_from_tag(h1)

    return heading


def get_first_paragraph_from_html(html: str) -> str:
    """Extract text from the first paragraph of the HTML"""
    soup: BS = BS(html, PARSER)
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


def extract_text_from_tag(tag: _AtMostOneElement) -> str:
    """Check if the `tag` is of the correct type and extract inner text,
    trimming any spaces
    """
    if isinstance(tag, Tag):
        return tag.get_text(strip=True)

    return ""


def normalize_url(url: str) -> str:
    """Normalize received URL to format HOST/PATH"""
    parsed_url: ParseResult = urlparse(url)
    normalized_url: str = (
        f"{parsed_url.netloc}{parsed_url.path.removesuffix('/')}"
    )

    return normalized_url.lower()
