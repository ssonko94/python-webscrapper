import scraper
import trial_solution


if __name__ == "__main__":
    # (is_success, message, text) = scraper.google_search("daily monitor")
    # if is_success:
    #     links = scraper.scrape_for_links(text)
    #     facebook_link = scraper.find_facebook_link(links)
    #     print(facebook_link)
    #     (hasFound, string, html) = scraper.google_search(facebook_link)
    #     anchors = scraper.scrape_for_links(html)
    # print(anchors)
    # (has_email, success_message, email) = scraper.find_email_address(html)
    # print(email)
    # links = scraper.get_links("https://www.facebook.com/DailyMonitor/")
    # print(links)
    trial_solution.main("./company_list.txt", "./company_email.txt")
