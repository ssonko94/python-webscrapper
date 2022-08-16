import requests


def make_list_from_file_content(file_name: str) -> list:
    """
    Reads file content and returns list of lines.
    """
    content_list = []

    if file_name is None or not isinstance(file_name, str):
        return "File name is not valid."

    with open(file_name, "r") as file:
        for line in file:
            content_list.append(line.strip())

    return content_list


def get_html_string_from_a_request(query: str) -> str:
    """
        Returns html string from a request.
    """
    url = "https://www.google.com/search?q=" + query
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return str(e)
