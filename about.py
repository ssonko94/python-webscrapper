from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
URL = "https://www.facebook.com/DailyMonitor/about/"
driver.get(URL)
anchors = driver.find_elements_by_tag_name("a")
target = next(anchor for anchor in anchors if "mailto:" in anchor.get_attribute("href"))
print(target.text)
