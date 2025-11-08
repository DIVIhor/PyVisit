import argparse
from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    """Create and return a CLI argument parser with the following parameters
    - `url` - URL to crawl to, a required positional parameter
    - `-s`, `--sync` - synchronous mode, a flag
    - `-c`, `--concurrency` - limit concurrent requests, an optional integer argument
    - `-p`, `--page-limit` - limit number of pages to crawl, an optional integer argument
    - `-v`, `--verbose` - print CLI report, an optional parameter
    - `--csv` - specifies whether to write a report in a CSV file,
    an optional argument
    - `--json` - specifies whether to write a report in a JSON file,
    an optional argument
    - `--fname` - specifies a file name to write a report to
    """
    # create an argument parser
    parser = argparse.ArgumentParser()

    # add a positional URL parameter
    parser.add_argument("url", help="root URL of the website")

    # synchronous mode
    parser.add_argument(
        "-s",
        "--sync",
        help="run crawler in synchronous mode",
        action="store_true",
    )

    # crawling page limit
    parser.add_argument(
        "-p",
        "--page-limit",
        type=int,
        help="the maximum number of pages to crawl, integer (default is 10)",
    )
    # concurrency limit
    parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        help="the maximum number of concurrent requests, integer (default is 3)",
    )

    # reporting parameters
    report_group = parser.add_argument_group()
    report_group.add_argument(
        "-v",
        "--verbose",
        help="display a simplified report in the CLI",
        action="store_true",
    )
    report_group.add_argument(
        "--csv",
        help="write report to a CSV file",
        action="store_true",
    )
    report_group.add_argument(
        "--json", help="write report to a JSON file", action="store_true"
    )
    report_group.add_argument(
        "--fname",
        help="specify a file name to write a report to (default is `report`)",
    )

    return parser
