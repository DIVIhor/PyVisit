import asyncio

from async_crawl import crawl_site_async
from report import write_csv_report, write_json_report, print_report

from cli_args import create_parser

from config import MAX_CONCURRENCY, MAX_PAGES_TO_CRAWL


async def main():
    # get CLI args
    parser = create_parser()
    cli_args = parser.parse_args()

    # set up crawling and concurrency limits
    max_concurrency: int = cli_args.concurrency or MAX_CONCURRENCY
    max_pages_to_crawl: int = cli_args.page_limit or MAX_PAGES_TO_CRAWL

    print(f"starting crawl of: {(base_url := cli_args.url)}")

    # crawl website
    page_data: dict[str, dict[str, str | list[str]]] = await crawl_site_async(
        base_url, max_concurrency, max_pages_to_crawl
    )

    print(f"\nCrawling complete. Found {len(page_data)} pages.\n")

    # print a simple report on fetched data
    if cli_args.verbose:
        print_report(page_data)

    # write fetched data to a CSV file
    if cli_args.csv:
        fname = cli_args.fname or "report"
        write_csv_report(page_data, fname)

    # write fetched data to a JSON file
    if cli_args.json:
        fname = cli_args.fname or "report"
        write_json_report(page_data, fname)


if __name__ == "__main__":
    asyncio.run(main())
