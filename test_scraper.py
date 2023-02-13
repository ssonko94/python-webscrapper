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


@patch("scraper.requests")
@pytest.mark.parametrize(
    "name, args, want",
    [
        (
            "failure",
            "",
            (False, "failed to make get request: bad getway error", None),
        ),
    ],
)
def test_google_search_failure(mock_requests, name, args, want):
    def mock_function(url):
        raise Exception("bad getway error")

    mock_requests.get = mock_function
    got = scraper.google_search(args)
    assert got == want, "{}: got: {}, want: {}".format(name, got, want)


@pytest.mark.parametrize(
    "name, args, want",
    [
        (
            "success",
            "<section><a>News</a><a>here</a><a>home</a></section>",
            ["<a>home</a>", "<a>here</a>", "<a>News</a>"],
        )
    ],
)
def test_scrape_for_links(name, args, want):
    got = scraper.scrape_for_links(args)
    assert got == want, "{}: got: {}, want: {}".format(name, got, want)
