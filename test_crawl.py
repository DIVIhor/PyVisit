import unittest

from crawl import (
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
)


class TestCrawl(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        # Inner text
        self.expected_h1_text: str = "Some Fancy Title"
        self.expected_p_text: str = "This paragraph is expected."
        # URL parts
        self.url: str = "blog.boot.dev"
        self.path: str = "/some/path"
        self.img_path: str = "/image.png"
        # URL combinations
        self.url_with_path: str = f"{self.url}{self.path}"
        self.abs_url_http: str = f"http://{self.url}"
        self.abs_url_https: str = f"https://{self.url}"
        self.abs_url_with_path: str = f"{self.abs_url_https}{self.path}"
        self.abs_img_url: str = f"{self.abs_url_with_path}{self.img_path}"
        self.rel_img_url: str = f"{self.path}{self.img_path}"
        # Templates
        self.h1_template: str = "<h1>{}</h1>"
        self.main_template: str = "<main>{}</main>"
        self.p_template: str = "<p>{}</p>"
        self.a_template: str = '<a href="{}">Link text</a>'
        self.img_template: str = '<img src="{}">'
        self.html_template: str = """<html>
  <body>
    {content}
  </body>
</html>"""

    # URL normalization

    def test_normalize_url_normalized(self):
        input_url: str = self.url_with_path
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.url_with_path)

    def test_normalize_url_http(self):
        input_url: str = f"http://{self.url_with_path}"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.url_with_path)

    def test_normalize_url_https(self):
        input_url: str = f"https://{self.url_with_path}"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.url_with_path)

    def test_normalize_url_slash(self):
        input_url: str = f"{self.url_with_path}/"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.url_with_path)

    def test_normalize_url_capitals(self):
        input_url: str = f"https://{self.url_with_path.capitalize()}/"
        actual: str = normalize_url(input_url)
        self.assertEqual(actual, self.url_with_path)

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

    # URL extraction

    def test_get_urls_from_html_absolute_url(self):
        content: str = self.a_template.format(self.abs_url_https)
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_urls_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_url_https]
        self.assertListEqual(actual, expected)

    def test_get_urls_from_html_relative_url(self):
        content: str = self.a_template.format(self.path)
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_urls_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_url_with_path]
        self.assertListEqual(actual, expected)

    def test_get_urls_from_html_relative_and_absolute(self):
        rel: str = self.a_template.format(self.path)
        abs: str = self.a_template.format(self.abs_url_https)
        content: str = f"{rel}\n{abs}"
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_urls_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_url_with_path, self.abs_url_https]
        self.assertListEqual(actual, expected)

    def test_get_urls_from_html_no_urls(self):
        html: str = self.html_template.format(content="")
        actual: list[str] = get_urls_from_html(html, self.abs_url_https)
        expected: list[str] = []
        self.assertListEqual(actual, expected)

    # Image extraction

    def test_get_images_from_html_absolute_url(self):
        content: str = self.img_template.format(self.abs_img_url)
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_images_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_img_url]
        self.assertListEqual(actual, expected)

    def test_get_images_from_html_relative_url(self):
        content: str = self.img_template.format(self.rel_img_url)
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_images_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_img_url]
        self.assertListEqual(actual, expected)

    def test_get_images_from_html_relative_and_absolute(self):
        rel: str = self.img_template.format(self.rel_img_url)
        abs: str = self.img_template.format(self.abs_img_url)
        content: str = f"{rel}\n{abs}"
        html: str = self.html_template.format(content=content)
        actual: list[str] = get_images_from_html(html, self.abs_url_https)
        expected: list[str] = [self.abs_img_url, self.abs_img_url]
        self.assertListEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        html: str = self.html_template.format(content="")
        actual: list[str] = get_images_from_html(html, self.abs_url_https)
        expected: list[str] = []
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
