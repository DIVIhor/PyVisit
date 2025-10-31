import sys

from crawl import crawl_page


def main():
    # input control
    if (arguments := len(sys.argv)) < 2:
        print("no website provided")
        sys.exit(1)
    elif arguments > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {(base_url := sys.argv[1])}")

    # fetch HTML
    page_data: dict[str, dict[str, str | list[str]]] = crawl_page(base_url)
    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")


if __name__ == "__main__":
    main()
