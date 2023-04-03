import scraper


if __name__ == "__main__":
    (hasFoundNames, confirm, company_names) = scraper.generate_list_from_file_content(
        "./company_list.txt"
    )

for company_name in company_names:  # type: ignore
    (is_success, message, text) = scraper.google_search(company_name)  # type: ignore
    if is_success:
        links = scraper.scrape_for_links(text)
        facebook_link = scraper.find_facebook_link(links)
        facebook_html = scraper.get_facebook_about_page(facebook_link)
        anchors = scraper.scrape_for_links(facebook_html)
        print(anchors)
        # (hasEmail, email_message, email_link) = scraper.find_email_address(
        #     facebook_html
        # )
        # print(company_name, email_link)
#     (hasFound, string, html) = scraper.google_search(facebook_link)
#     anchors = scraper.scrape_for_links(html)
# print(anchors)
# (has_email, success_message, email) = scraper.find_email_address(html)
# print(email)
# links = scraper.get_links("https://www.facebook.com/DailyMonitor/")
# print(links)
# trial_solution.main("./company_list.txt", "./company_email.txt")
