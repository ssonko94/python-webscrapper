[![Coverage Status](https://coveralls.io/repos/github/ssonko94/python-webscrapper/badge.svg)](https://coveralls.io/github/ssonko94/python-webscrapper)

# python web scrapper

This is a demo web scraping app built with python beautiful soup library.

## Goal:

To create a **program** that takes in a file input as it's argument with a list of company names.

The programm will then get a google search results of these company names and scrape for their facebook page links.

From the facebook link the program should send request to get this facebook page then while on the page navigate to the about page and scrape for the company email adress.

In the end write to an output file the company name and corresponding email adress.

`Requirements:`

> We are required to build this program using python `beatiful soup` for scrapping.

> We also need the `requests` library to send http request.

> We are also required to write unit tests using the `pytest library`

### SpecialThanks:

> - [Nickson Mungujakisa] (https://github.com/mungujn)
> - [Daniel Ssejjemba] (https://github.com/ssejjemba)
