import requests
from bs4 import BeautifulSoup
from typing import Any, Tuple, Union
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


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
    url = f"https://www.google.com/search?q={param}&num=20"
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


def find_facebook_username(links) -> str | None:
    pattern = (
        r"(?i)\/url\?q=https:\/\/(?:www\.)?facebook\.com\/(?P<username>[a-zA-Z0-9.]*)"
    )
    for link in links:
        match = re.search(pattern, link)
        if match:
            return match.group("username")
    return None


def scrape_email_from_about_page(facebook_username) -> str:
    if facebook_username == None:
        return ""
    url = f"https://www.facebook.com/{facebook_username}/about"

    browser = webdriver.Firefox()
    browser.get(url)
    email = "no email found"
    try:
        email_element = browser.find_element(By.XPATH, '//span[contains(text(),"@")]')
        if email_element:
            email = email_element.text

    except:
        return "no email found"
    finally:
        browser.quit()
        return email
