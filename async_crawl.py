import asyncio
from asyncio import Lock, Semaphore

from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession

from crawl import extract_page_data, normalize_url

from config import MAX_CONCURRENCY


class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int):
        self.base_url = base_url
        self.base_domain: str = urlparse(self.base_url).netloc
        self.page_data: dict[str, dict[str, str | list[str]]] = {}
        self.lock: Lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore: Semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: ClientSession

    async def __aenter__(self):
        """Open a client session"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client session"""
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        """Check if the page was visited earlier"""
        async with self.lock:
            return normalized_url in self.page_data

    async def get_html(self, url: str) -> str:
        """Asynchronously send GET request to `url` and return its HTML or raise an exception"""
        user_agent: str = "BootCrawler/1.0"

        try:
            # send GET request
            async with self.session.get(
                url, headers={"User-Agent": user_agent}
            ) as resp:
                # catch errors
                if (resp_code := resp.status) >= 400:
                    raise Exception(
                        f"server responded with error: '{resp_code}'"
                    )
                if not (
                    content_type := resp.headers.get("content-type", "")
                ).startswith("text/html"):
                    raise Exception(
                        f"server responded with unexpected content-type: '{content_type}'"
                    )
                return await resp.text()
        except Exception as e:
            raise Exception(f"network error: {e}")

    async def crawl_page(self, current_url: str):
        """Recursively traverse found URLs"""
        # make sure the current url is on the same domain as the base url
        if urlparse(current_url).netloc != self.base_domain:
            return
        # ignore already crawled pages
        if await self.add_page_visit(
            normalized_url := normalize_url(current_url)
        ):
            return

        async with self.semaphore:
            # retrieve the HTML
            print(
                f"crawling: {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            try:
                html: str = await self.get_html(current_url)
            except Exception as e:
                print(f"error crawling {current_url}: {e}")
                return

            async with self.lock:
                # extract and store page data
                self.page_data[normalized_url] = extract_page_data(
                    html, current_url
                )

                # schedule to crawl each URL on the page
                tasks: list[asyncio.Task] = [
                    asyncio.create_task(self.crawl_page(current_url=url))
                    for url in self.page_data[normalized_url]["outgoing_links"]
                ]

        await asyncio.gather(*tasks)

    async def crawl(self) -> dict[str, dict[str, str | list[str]]]:
        """Start crawling from `base_url` and return the page data"""
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(
    base_url: str,
) -> dict[str, dict[str, str | list[str]]]:
    """Create an `AsyncCrawler`'s instance on the `base_url`
    and start crawling
    """
    async with AsyncCrawler(base_url, MAX_CONCURRENCY) as crawler:
        return await crawler.crawl()
