import re
from typing import List, Optional
import requests
from bs4 import BeautifulSoup


def read_company_names(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f]


def get_google_results(query: str) -> List[str]:
    url = f"https://www.google.com/search?q={query}&num=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    return [a["href"] for a in soup.find_all("a", href=True)]


def find_facebook_url(links: List[str]) -> Optional[str]:
    for link in links:
        if "facebook.com" in link:
            return link

    return None


def find_email(url: str) -> Optional[str]:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    email_links = soup.find_all("a", href=re.compile(r"mailto:"))
    if email_links:
        return email_links[0]["href"].replace("mailto:", "")

    return None


def write_output(company_name: str, email: Optional[str], file_path: str) -> None:
    with open(file_path, "a") as f:
        if email:
            f.write(f"{company_name} : {email}\n")
        else:
            f.write(f"{company_name} : No email found\n")


def main(input_file: str, output_file: str) -> None:
    company_names = read_company_names(input_file)

    for company_name in company_names:
        links = get_google_results(company_name)
        facebook_url = find_facebook_url(links)
        if facebook_url:
            email = find_email(facebook_url)
        else:
            email = None

        write_output(company_name, email, output_file)
