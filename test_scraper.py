import scraper
import pytest
from unittest.mock import MagicMock, Mock, patch


def _mock_response(
    status=200,
    content="CONTENT",
):
    mock_resp = Mock()
    mock_resp.status = status
    mock_resp.content = content

    return mock_resp


@pytest.mark.parametrize(
    "name, args, want",
    [
        (
            "success",
            "./test_data/test_file.txt",
            (
                True,
                "reading file successfully",
                ["monitor", "bukedde", "new vision"],
            ),
        ),
        (
            "failed",
            "fluter.txt",
            (False, "No such file or directory: 'fluter.txt'", []),
        ),
    ],
)
def test_generate_list_from_file_content(name, args, want):
    got = scraper.generate_list_from_file_content(args)
    assert got == want, "{}: got: {}, want: {}".format(name, got, want)


@pytest.mark.parametrize(
    "name, args, want",
    [
        (
            "success",
            """<a  href="mailto:digital@ug.nationmedia.com" role="link" tabindex="0" target="_blank">digital@ug.nationmedia.com</a>""",
            (
                True,
                "",
                "digital@ug.nationmedia.com",
            ),
        ),
        (
            "faliure",
            "",
            (False, "no email found", ""),
        ),
    ],
)
def test_find_email_adress(name, args, want):
    got = scraper.find_email_address(args)
    assert got == want, "{}: got: {}, want: {}".format(name, got, want)


@patch("scraper.requests")
@pytest.mark.parametrize(
    "name, args, want",
    [
        (
            "success",
            "dailymonitor",
            (True, "Request was successful", "<h1>Hello from daily monitor</h1>"),
        )
    ],
)
def test_google_search_success(mock_requests, name, args, want):
    mock_response = _mock_response(content="<h1>Hello from daily monitor</h1>")
    mock_requests.get.return_value = mock_response
    got = scraper.google_search(args)
    assert got == want, "{}: got: {}, want: {}".format(name, got, want)


@pytest.mark.parametrize(
    "html, expected",
    [
        (
            '<html><body><a href="https://www.google.com">Google</a><a href="https://www.amazon.com">Amazon</a></body></html>',
            ["https://www.google.com", "https://www.amazon.com"],
        ),
        (
            '<html><body><a href="https://www.facebook.com">Facebook</a></body></html>',
            ["https://www.facebook.com"],
        ),
        (
            '<html><body><a href="https://www.twitter.com">Twitter</a><p>Some text</p></body></html>',
            ["https://www.twitter.com"],
        ),
        ("<html><body></body></html>", []),
        (None, []),
    ],
)
def test_scrape_for_links(html, expected):
    assert scraper.scrape_for_links(html) == expected


@pytest.mark.parametrize(
    "links, expected",
    [
        (
            [
                "https://www.facebook.com/",
                "https://www.linkedin.com/",
                "https://www.youtube.com/",
            ],
            "https://www.facebook.com/",
        ),
        (
            [
                "https://www.google.com/",
                "https://www.yahoo.com/",
                "https://www.facebook.com/pages/123456789",
            ],
            "https://www.facebook.com/pages/123456789",
        ),
        (
            [
                "https://www.twitter.com/",
                "https://www.instagram.com/",
                "https://www.facebook.com/#123456789",
            ],
            "https://www.facebook.com/#123456789",
        ),
        ([], "No links to scrape"),
        (
            [
                "https://www.google.com/",
                "https://www.linkedin.com/",
                "https://www.youtube.com/",
            ],
            "",
        ),
    ],
)
def test_find_facebook_link(links, expected):
    assert scraper.find_facebook_link(links) == expected


def test_trim_facebook_url():
    assert (
        scraper.trim_facebook_url("https://www.facebook.com/pages/123456789")
        == "https://www.facebook.com/pages/123456789"
    )
    assert (
        scraper.trim_facebook_url("https://www.facebook.com/#123456789")
        == "https://www.facebook.com/#123456789"
    )
    assert (
        scraper.trim_facebook_url("https://www.facebook.com/username")
        == "https://www.facebook.com/username"
    )
