import scraper


def main():
    input_file = "company_list.txt"
    output_file = "emails.txt"

    success, message, company_names = scraper.generate_list_from_file_content(
        input_file
    )

    if success:
        results = []
        for company_name in company_names:
            success, message, html = scraper.google_search(company_name)

            if success:
                links = scraper.scrape_for_links(html)
                facebook_username = scraper.find_facebook_username(links)

                if facebook_username:
                    email = scraper.scrape_email_from_about_page(facebook_username)
                else:
                    email = "email not found"
            else:
                email = "email not found"

            results.append(f"{company_name}: {email}")

        with open(output_file, "w") as file:
            file.write("\n".join(results))
        print("Emails written to emails.txt")
    else:
        print(f"Error: {message}")


if __name__ == "__main__":
    main()
