
List_Of_Programs = []
with open ("List_Of_Programs.txt", encoding="utf=8") as list:
    for item in list:
        List_Of_Programs.append(item)


import requests
from bs4 import BeautifulSoup
import json

for item in List_Of_Programs:
    item = item.rstrip()
    Program_list = json.loads(item)

    url = "https://tv.nrk.no" + Program_list[1]
    html_page = requests.get(url)
    # html_header = requests.head(url)
    # print(html_page.headers)
    beautiful_html_page = BeautifulSoup(html_page.content, "html.parser")
    # List_In_Memory = beautiful_html_page.select('div[data-program-id$="X"]')
    List_In_Memory = beautiful_html_page.find(attrs={"data-program-id"})
    if (len(List_In_Memory) == 0):
        List_In_Memory = item[1].replace("/serie/","").replace("/program/","")
    # else: List_In_Memory = beautiful_html_page.select('div[data-program-id$="X"]')

    for things in List_In_Memory:
        print(things)
