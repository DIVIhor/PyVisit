import sys

from crawl import get_html


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
    try:
        html: str = get_html(base_url)
    except Exception as e:
        print(f"Error fetching HTML from {base_url}: {str(e)}")
        sys.exit(1)

    print(html)


if __name__ == "__main__":
    main()
