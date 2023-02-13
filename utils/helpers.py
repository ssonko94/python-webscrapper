import requests
import bs4 as BeautifulSoup
import re


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


def get_html_string_from_a_request(url: str) -> str:
    """
    Returns html string from a request.
    """
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return str(e)


def find_links_in_html_string(html_string: str) -> list:
    """
    Returns list of links from html string.
    """
    links = []

    if html_string is None or not isinstance(html_string, str):
        return "Html string is not valid."

    soup = BeautifulSoup(html_string, "html.parser")
    for link in soup.find_all("a"):
        links.append(link.get("href"))

    return links


def get_list_of_facebook_links_from_list_of_links(links: list) -> list:
    """
    Returns list of facebook links from list of links.
    """
    facebook_links = []

    if links is None or not isinstance(links, list):
        return "Links is not valid."

    for link in links:
        if re.search("https://www.facebook.com/", link["href"]):
            facebook_links.append(link["href"])

    return facebook_links


def get_email_adress_link_from_list_of_links(links: list) -> str:
    """
    Returns email adress link from list of links.
    """
    email_adress_link = ""

    if links is None or not isinstance(links, list):
        return "Links is not valid."

    for link in links:
        if re.search("mailto:", link["href"]):
            email_adress_link = link["href"]

    return email_adress_link
