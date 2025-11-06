import csv


def write_csv_report(
    page_data: dict[str, dict[str, str | list[str]]],
    filename: str = "report.csv",
):
    """Write crawling report to a CSV file using the provided file name."""
    if not page_data:
        print("No data to write to CSV")
        return

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
