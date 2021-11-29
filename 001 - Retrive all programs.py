
import string

from bs4.element import Script

# extra_letters = "ae, oe, aa, 0-9"
# letters = string.ascii_lowercase
# letters = list(string.ascii_lowercase)
# letters.extend(extra_letters)

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ae", "oe", "aa", "0-9"]
# letters = ["ae", "oe", "aa", "0-9"]
print(letters)
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

from selenium import webdriver
import time

List_In_Memory = []
amount = 0
for link in letters:
    driver = webdriver.Chrome("C:\chromedriver\chromedriver.exe")
    driver.get("https://tv.nrk.no/alle-programmer/" + link)
    # time.sleep(1)
    html_page = driver.page_source
    beautiful_html_page = BeautifulSoup(html_page, "html.parser")
    List_In_Memory = beautiful_html_page.find_all("a", class_="tv-cl-letter-element tv-text-styles-subhead")
    amount += 1



#    TODO: Fix the extra_letters pages not being included.
    with open("List_Of_Programs.txt", "a", encoding="utf-8") as file_object:
        for item in List_In_Memory:
            array = [item.text,item['href']]
            json.dump(array, file_object, ensure_ascii=False)
            file_object.write("\n")
print(amount)
# ["program", /serie/programlink]
    