from types import UnionType
import requests
from bs4 import BeautifulSoup
from typing import Any, List, Tuple, Union
import re


def generate_list_from_file_content(filename: str) -> Tuple[bool, str, list]:
    content_list = []
    try:
        with open(filename, "r") as file:
            for line in file:
                content_list.append(line.strip())
        return True, "reading file successfully", content_list
    except OSError as err:
        return False, f"No such file or directory: '{filename}'", []


def google_search(
    param: str,
) -> Tuple[bool, str, Union[str, Any]]:
    url = f"https://www.google.com/search?q={param}"
    try:
        response = requests.get(url)
        return (
            True,
            "Request was successful",
            response.content,
        )
    except Exception as err:
        return False, f"failed to make get request: {str(err)}", None


def scrape_for_links(html: str) -> list:
    if html == None:
        return []
    soup = BeautifulSoup(html, "html.parser")
    links = [
        link.get("href") for link in soup.find_all("a") if link.get("href") is not None
    ]
    return links


def find_facebook_link(links: list) -> str:
    facebook_link = ""
    pattern = r"(?:(?:http|https):\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?([\w\-]*)?"
    if len(links) == 0:
        facebook_link = "No links to scrape"
    for link in links:
        match = re.search(pattern, link)
        if match:
            facebook_link = trim_facebook_url(match.string)
            return facebook_link
        else:
            facebook_link = ""
    return facebook_link


def get_facebook_about_page(url: str) -> str:
    if url == "No links to scrape" or url == "":
        return "couldnot find this page"
    response = requests.get(url + "/about")
    html_text = response.content
    return str(html_text)


def find_email_address(html: str) -> Tuple[bool, str, str]:
    # reg_email_pattern = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    if html == "couldnot find this page":
        return False, "No email found", ""
    soup = BeautifulSoup(html, "html.parser")
    script = soup.get_text()
    email_links: List[str] = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", script
    )

    if len(email_links) > 0:
        return True, "", email_links[0]

    return False, "no email found", ""


def trim_facebook_url(link):
    # Define the regular expression pattern to match the Facebook URL
    pattern = r"/url\?q=(.*?)&"

    # Find the match using the pattern
    match = re.search(pattern, link)

    # If a match is found, return the captured group, else return None
    if match:
        return match.group(1)
    else:
        return "no match found"


def get_links(url):
    # Send a GET request to the URL and get the content
    response = requests.get(url)
    content = response.content

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find all the <a> tags in the HTML and extract the links
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None:
            links.append(href)

    return links


# Test the function with the provided URL
