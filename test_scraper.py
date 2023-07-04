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
    "links, expected_username",
    [
        (
            [
                "/url?q=https://www.facebook.com/username1&sa=U",
                "/url?q=https://www.google.com&sa=U",
            ],
            "username1",
        ),
        (
            [
                "/url?q=https://www.google.com&sa=U",
                "/url?q=https://www.facebook.com/username2&sa=U",
            ],
            "username2",
        ),
        ([], None),
    ],
)
def test_find_facebook_username(links, expected_username):
    username = scraper.find_facebook_username(links)
    assert username == expected_username


@pytest.mark.parametrize(
    "facebook_username, expected_email",
    [
        ("existing_username", "example@example.com"),
        ("non_existing_username", "no email found"),
        (None, ""),
    ],
)
@patch("selenium.webdriver.Firefox")
def test_scrape_email_from_about_page(mock_browser, facebook_username, expected_email):
    mock_driver = mock_browser.return_value
    mock_element = (
        Mock(text="example@example.com")
        if facebook_username == "existing_username"
        else None
    )
    mock_driver.find_element.return_value = mock_element

    email = scraper.scrape_email_from_about_page(facebook_username)
    assert email == expected_email
