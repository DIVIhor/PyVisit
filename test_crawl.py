import unittest

from crawl import (
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
)


class TestCrawl(unittest.TestCase):
    expected_url: str = "blog.boot.dev/path"
    expected_h1_text: str = "Some Fancy Title"
    expected_p_text: str = "This is paragraph is expected."
    h1_template: str = "<h1>{}</h1>"
    main_template: str = "<main>{}</main>"
    p_template: str = "<p>{}</p>"
    html_template: str = """<html>
  <body>
    {content}
  </body>
</html>"""

    # URL normalization

    def test_normalize_url_normalized(self):
        input_url: str = self.expected_url
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.expected_url)

    def test_normalize_url_http(self):
        input_url: str = f"http://{self.expected_url}"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.expected_url)

    def test_normalize_url_https(self):
        input_url: str = f"https://{self.expected_url}"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.expected_url)

    def test_normalize_url_slash(self):
        input_url: str = f"{self.expected_url}/"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.expected_url)

    def test_normalize_url_capitals(self):
        input_url: str = f"https://{self.expected_url.capitalize()}/"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.expected_url)

    # Heading extraction

    def test_get_h1_from_html_basic(self):
        input_h1: str = self.h1_template.format(self.expected_h1_text)
        input_html: str = self.html_template.format(content=input_h1)
        actual: str = get_h1_from_html(input_html)
        self.assertEqual(actual, self.expected_h1_text)

    def test_get_h1_from_html_two_h1(self):
        input_h1_first: str = self.h1_template.format(self.expected_h1_text)
        input_h1_second: str = self.h1_template.format("Additional Heading")
        input_h1: str = f"{input_h1_first}\n{input_h1_second}"
        input_html: str = self.html_template.format(content=input_h1)
        actual: str = get_h1_from_html(input_html)
        self.assertEqual(actual, self.expected_h1_text)

    def test_get_h1_from_html_with_spaces(self):
        input_h1: str = self.h1_template.format(f" {self.expected_h1_text}\n")
        input_html: str = self.html_template.format(content=input_h1)
        actual: str = get_h1_from_html(input_html)
        self.assertEqual(actual, self.expected_h1_text)

    def test_get_h1_from_html_no_h1(self):
        actual: str = get_h1_from_html(self.html_template)
        self.assertEqual(actual, "")

    # Paragraph extraction

    def test_get_first_paragraph_from_html_main_priority(self):
        p: str = self.p_template.format(
            "This paragraph is outside the main tag."
        )
        p_main: str = self.p_template.format(self.expected_p_text)
        main: str = self.main_template.format(p_main)
        input_html: str = self.html_template.format(content=f"{p}\n{main}")
        actual: str = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, self.expected_p_text)

    def test_get_first_paragraph_from_html_with_spaces(self):
        p_main: str = self.p_template.format(f" {self.expected_p_text}\n")
        main: str = self.main_template.format(p_main)
        input_html: str = self.html_template.format(content=main)
        actual: str = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, self.expected_p_text)

    def test_get_first_paragraph_from_html_no_main(self):
        p: str = self.p_template.format(self.expected_p_text)
        input_html: str = self.html_template.format(content=p)
        actual: str = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, self.expected_p_text)

    def test_get_first_paragraph_from_html_two_p(self):
        p1: str = self.p_template.format(self.expected_p_text)
        p2: str = self.p_template.format("This paragraph is not expected.")
        input_p: str = f"{p1}\n{p2}"
        input_html: str = self.html_template.format(content=input_p)
        actual: str = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, self.expected_p_text)

    def test_get_first_paragraph_from_html_no_p(self):
        actual: str = get_first_paragraph_from_html(self.html_template)
        self.assertEqual(actual, "")


if __name__ == "__main__":
    unittest.main()
