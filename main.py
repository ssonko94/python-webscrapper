from utils import helpers
import scraper


if __name__ == "__main__":
    (is_success, message, text) = scraper.google_search("daily monitor")
    links = scraper.scrape_for_links(text)
    facebook_link = scraper.find_facebook_link(links, "daily monitor")
    about_page = scraper.get_facebook_about_page(facebook_link)
    address = scraper.find_email_address(about_page)
    print(address)
