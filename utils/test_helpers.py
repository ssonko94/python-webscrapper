import requests_mock
import helpers
import pytest


def test_make_list_from_file_content():
    # prepare
    file_name = "./test_data/test_file.txt"

    # test
    content_list = helpers.make_list_from_file_content(file_name)

    # assert

    assert content_list == ["monitor", "bukedde", "new vision"]

    file_name = {file_name: "./test_data/test_file.txt"}

    content_list = helpers.make_list_from_file_content(file_name)

    assert content_list == "File name is not valid."


@pytest.fixture
def test_get_html_string_from_a_request(mocker):
    mock_response = mocker.MagicMock(name="mock_response")
    mock_response.return_value = "<html>Hello</html>"

    # prepare
    query = "monitor"
    url = "https://www.google.com/search?q=" + query

    mocker.patch("requests.get", mock_response)

    # test
    res_data = helpers.get_html_string_from_a_request(url)

    # assert
    assert res_data == "<html>Hello</html>"
