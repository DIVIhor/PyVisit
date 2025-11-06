import asyncio
from asyncio import Lock, Semaphore, Task

from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession

from crawl import extract_page_data, normalize_url


class AsyncCrawler:
    def __init__(
        self, base_url: str, max_concurrency: int, max_pages_to_crawl: int
    ):
        self.base_url = base_url
        self.base_domain: str = urlparse(self.base_url).netloc
        self.page_data: dict[str, dict[str, str | list[str]]] = {}
        self.lock: Lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore: Semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: ClientSession

        # crawling control for maximum pages
        self.max_pages: int = max_pages_to_crawl
        self.should_stop: bool = False
        self.all_tasks: set[Task] = set()

    async def __aenter__(self):
        """Open a client session"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client session"""
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        """Check if the page was visited earlier or reached crawling maximum"""
        # check if crawler should stop
        if self.should_stop:
            return True

        async with self.lock:
            # check if reached max pages limit
            if len(self.page_data) == self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return True

            # check if page is already visited
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
        # stop further crawling if reached maximum crawls
        if self.should_stop:
            return

        # make sure the current url is on the same domain as the base url
        if urlparse(current_url).netloc != self.base_domain:
            return
        # ignore already crawled pages or links beyond the limit
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
                # save links for processing without locks
                links: list[str] = self.page_data[normalized_url][
                    "outgoing_links"
                ]  # type:ignore

        try:
            # schedule crawling for each URL on the page
            for url in links:
                self.all_tasks.add(asyncio.create_task(self.crawl_page(url)))
            await asyncio.gather(*self.all_tasks)
        finally:
            self.all_tasks.clear()
            return

    async def crawl(self) -> dict[str, dict[str, str | list[str]]]:
        """Start crawling from `base_url` and return the page data"""
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(
    base_url: str,
    max_concurrency: int,
    max_pages_to_crawl: int,
) -> dict[str, dict[str, str | list[str]]]:
    """Create an `AsyncCrawler`'s instance on the `base_url`
    and start crawling
    """
    async with AsyncCrawler(
        base_url, max_concurrency, max_pages_to_crawl
    ) as crawler:
        return await crawler.crawl()
