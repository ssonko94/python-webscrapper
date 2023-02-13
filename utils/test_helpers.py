import requests
import helpers
import pytest


def test_make_list_from_file_content():
    # prepare
    tests = [
        {
            "name": "success",
            "args": "./test_data/test_file.txt",
            "want": ["monitor", "bukedde", "new vision"],
        },
        {
            "name": "failure",
            "args": None,
            "want": "File name is not valid.",
        },
    ]

    # test
    for test in tests:
        got = helpers.make_list_from_file_content(test["args"])

        # assert
        assert got == test["want"], "{}: got: {}, want: {}".format(
            test["name"], got, test["want"]
        )


# @pytest.mark.skip(reason="temp")
def test_get_html_string_from_a_request(mocker):

    # prepare
    query = "monitor"
    url = "https://www.google.com/search?q=" + query

    class MockResponse:
        def __init__(self, text):
            self.text = text

    mocker.patch.object(requests, "get")
    requests.get.return_value = MockResponse("<html>Hello</html>")

    # test
    res_data = helpers.get_html_string_from_a_request(url)

    # assert
    assert res_data == "<html>Hello</html>"
