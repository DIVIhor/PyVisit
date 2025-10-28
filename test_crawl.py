import unittest

from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    expected_url: str = "blog.boot.dev/path"

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


if __name__ == "__main__":
    unittest.main()
