import asyncio
import sys

from async_crawl import crawl_site_async


async def main():
    # input control
    if (arguments := len(sys.argv)) < 2:
        print("no website provided")
        sys.exit(1)
    elif arguments > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {(base_url := sys.argv[1])}")

    # fetch HTML
    page_data: dict[str, dict[str, str | list[str]]] = await crawl_site_async(
        base_url
    )
    print("\n", f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")


if __name__ == "__main__":
    asyncio.run(main())
