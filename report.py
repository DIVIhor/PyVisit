import csv
import json


def write_csv_report(
    page_data: dict[str, dict[str, str | list[str]]],
    filename: str,
):
    """Write crawling report to a CSV file using the provided file name."""
    if not page_data:
        print("No data to write to CSV")
        return

    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        # create writer for further data writing
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "page_url",
                "h1",
                "first_paragraph",
                "outgoing_link_urls",
                "image_urls",
            ],
        )

        # write column names
        writer.writeheader()
        # write rows
        for page in page_data.values():
            processed_page: dict[str, str] = {
                "page_url": str(page["url"]),
                "h1": str(page["h1"]),
                "first_paragraph": str(page["first_paragraph"]),
                "outgoing_link_urls": ";".join(page["outgoing_links"]),
                "image_urls": ";".join(page["image_urls"]),
            }

            writer.writerow(processed_page)

    print(f"Report written to {filename}")


def write_json_report(
    page_data: dict[str, dict[str, str | list[str]]], filename: str
):
    """Write crawling report to a JSON file using the provided file name."""
    if not page_data:
        print("No data to write to JSON")
        return

    if not filename.endswith(".json"):
        filename = f"{filename}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=4)

    print(f"Report written to {filename}")


def print_report(page_data: dict[str, dict[str, str | list[str]]]):
    """Print a simplified crawling report"""
    print("=" * 120, "Crawling Report".center(120, " "), "=" * 120, sep="\n")
    for id, page in enumerate(page_data.values(), 1):
        print(
            f"{id}.",
            f"'{page['url']}' contains:",
            f"{'h1,' if page['h1'] else ''}",
            f"{'p,' if page['first_paragraph'] else ''}",
            f"URLs: {len(page['outgoing_links'])},",
            f"images: {len(page['image_urls'])}",
            "\n" + "-" * 120,
        )
