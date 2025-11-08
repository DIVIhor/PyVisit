# PyVisit

**PyVisit** is a simple Python-based crawler that collects all internal links from anchors and images on the website. Then it generates a report in desired format.

You can use the default parameters or specify a page crawl limit and the maximum number of asynchronous crawling tasks.
By default, crawler works in asynchronous mode with a max concurrency set of 3 and a limit of 10 pages to crawl.

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
- [Usage](#usage)
  - [Notes](#notes)

## Features

- Crawls the specified URL and extracts the following data:
  - Heading from the **\<h1>** tag
  - The first paragraph on the page (with priority given to the **\<main>** section)
  - All image URLs on the page
  - All links from anchors available on the page
- Crawls each URL found in anchors and extracts the same data as above
- Displays a CLI message indicating that crawling is complete and the number of additional pages found
- Generates a crawl report, with options to combine the following:
  - Display a simplified version in the CLI
  - Write the report to a CSV file
  - Write the report to a JSON file
- Can operate in either asynchronous or synchronous mode

## Requirements

Any desktop OS: Linux (or WSL for Windows) / MacOS / Windows.

To use the app you need to have **Python version 3.12+** on your computer.

## Installation Guide

1. Clone the repository with `git clone <URL>` or download and unzip it.
2. Create a virtual environment using one of the following:
    - _venv_: `python3 -m venv .venv` or `py -m venv .venv` for Windows
    - _uv_: `uv venv`
3. Activate your virtual environment with one of the following:
    - Linux: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\activate`
4. Install dependencies using one of the following:
    - _pip_: `pip install .`
    - _uv_: `uv sync`

## Usage

Open your CLI in the app's root folder. Use `python3` for Linux (or `py` for Windows) to run PyVisit
with the following using the following syntax:

```bash
python3 crawler/main.py [-h] [-s] [-p PAGE_LIMIT] [-c CONCURRENCY] [-v] [--csv] [--json] [--fname FNAME] url
```

### Parameters

#### Positional

`url` - root URL of the website to crawl

#### Optional

- `-h,` `--help` - show this help message and exit
- `-s`, `--sync` - run crawler in synchronous mode
- `-p PAGE_LIMIT`, `--page-limit PAGE_LIMIT` - the maximum number of pages to crawl, integer (default is 10)
- `-c CONCURRENCY`, `--concurrency CONCURRENCY` - the maximum number of concurrent requests, integer (default is 3)
- `-v`, `--verbose` - display a simplified report in the CLI
- `--csv` - write report to a CSV file
- `--json` - write report to a JSON file
- `--fname FNAME` - specify a file name to write a report to (default is `report`)

### Notes

- You can specify just the `url` by omitting the other arguments.
- You can combine the output parameters.
