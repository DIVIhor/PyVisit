import asyncio
import sys

from async_crawl import crawl_site_async
from csv_report import write_csv_report

from config import MAX_CONCURRENCY, MAX_PAGES_TO_CRAWL


async def main():
    # input control
    if (arguments := len(sys.argv)) < 2:
        print("no website provided")
        sys.exit(1)
    elif arguments > 4:
        print("too many arguments provided")
        sys.exit(1)

    # set up limits
    max_concurrency: int = (
        int(sys.argv[2]) if arguments == 4 else MAX_CONCURRENCY
    )
    max_pages_to_crawl: int = (
        int(sys.argv[3]) if arguments == 4 else MAX_PAGES_TO_CRAWL
    )

    print(f"starting crawl of: {(base_url := sys.argv[1])}")

    # crawl website
    page_data: dict[str, dict[str, str | list[str]]] = await crawl_site_async(
        base_url, max_concurrency, max_pages_to_crawl
    )

    print("\n", f"Crawling complete. Found {len(page_data)} pages.")

    # save crawled data
    write_csv_report(page_data)


if __name__ == "__main__":
    asyncio.run(main())
