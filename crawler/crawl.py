from urllib.parse import urljoin, urlparse, ParseResult

from bs4 import BeautifulSoup as BS
from bs4._typing import _AtMostOneElement
from bs4.element import PageElement, Tag, ResultSet

import requests
from requests import Response


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


def get_html(url: str) -> str:
    """Send GET request to `url` and return its HTML or raise an exception"""
    user_agent: str = "BootCrawler/1.0"

    # send GET request
    try:
        resp: Response = requests.get(url, headers={"User-Agent": user_agent})
    except Exception as e:
        raise Exception(f"network error: {e}")

    # catch errors
    if (resp_code := resp.status_code) >= 400:
        raise Exception(f"server responded with error: '{resp_code}'")
    if not (content_type := resp.headers.get("content-type", "")).startswith(
        "text/html"
    ):
        raise Exception(
            f"server responded with unexpected content-type: '{content_type}'"
        )

    return resp.text


def crawl_page(
    base_url: str,
    max_pages_to_crawl: int,
    current_url: str | None = None,
    page_data: dict[str, dict[str, str | list[str]]] | None = None,
) -> dict[str, dict[str, str | list[str]]]:
    """Recursively traverse found URLs"""
    # manage missing parts
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    # check if reached limit of pages to crawl
    if max_pages_to_crawl and (len(page_data) == max_pages_to_crawl):
        return page_data

    # make sure the current url is on the same domain as the base url
    if urlparse(current_url).netloc != urlparse(base_url).netloc:
        return page_data
    # ignore already crawled pages
    if (normalized_url := normalize_url(current_url)) in page_data:
        return page_data

    # retrieve the HTML
    print(f"crawling: {current_url}")
    try:
        html: str = get_html(current_url)
    except Exception as e:
        print(f"error crawling {current_url}: {e}")
        return page_data

    # extract and store page data
    page_data[normalized_url] = extract_page_data(html, current_url)

    # crawl each URL on the page
    for url in page_data[normalized_url]["outgoing_links"]:
        page_data = crawl_page(
            base_url=base_url,
            max_pages_to_crawl=max_pages_to_crawl,
            current_url=url,
            page_data=page_data,
        )

    return page_data
