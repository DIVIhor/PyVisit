import asyncio

from argparse import ArgumentParser, Namespace

from async_crawl import crawl_site_async
from crawl import crawl_page

from report import write_csv_report, write_json_report, print_report

from cli_args import create_parser

from config import MAX_CONCURRENCY, MAX_PAGES_TO_CRAWL


async def main():
    # get CLI args
    parser: ArgumentParser = create_parser()
    cli_args: Namespace = parser.parse_args()

    # set up crawling limit
    max_pages_to_crawl: int = cli_args.page_limit or MAX_PAGES_TO_CRAWL

    print(f"starting crawl of: {(base_url := cli_args.url)}")

    page_data: dict[str, dict[str, str | list[str]]]
    # crawl in sync mode
    if cli_args.sync:
        page_data = crawl_page(base_url, max_pages_to_crawl=max_pages_to_crawl)
    # crawl in async mode
    else:
        # set up concurrency limit and start crawling
        max_concurrency: int = cli_args.concurrency or MAX_CONCURRENCY
        page_data = await crawl_site_async(
            base_url, max_concurrency, max_pages_to_crawl
        )

    print(f"\nCrawling complete. Found {len(page_data)} pages.\n")

    # write fetched data to a CSV file
    if cli_args.csv:
        fname: str = cli_args.fname or "report"
        write_csv_report(page_data, fname)

    # write fetched data to a JSON file
    if cli_args.json:
        fname: str = cli_args.fname or "report"
        write_json_report(page_data, fname)

    # print a simple report on fetched data
    # if requested or no other options for output provided
    if cli_args.verbose or not (cli_args.csv or cli_args.json):
        print_report(page_data)


if __name__ == "__main__":
    asyncio.run(main())
