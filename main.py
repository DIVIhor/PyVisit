import sys


def main():
    # input control
    if (arguments := len(sys.argv)) < 2:
        print("no website provided")
        sys.exit(1)
    elif arguments > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")


if __name__ == "__main__":
    main()
