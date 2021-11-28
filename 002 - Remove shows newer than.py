
List_Of_Programs = []
with open ("List_Of_Programs.txt", encoding="utf=8") as list:
    for item in list:
        List_Of_Programs.append(item)


import requests
from bs4 import BeautifulSoup

for item in List_Of_Programs:
    item = item.rstrip()
    html_page = requests.get("https://tv.nrk.no/serie/" + item)
    beautiful_html_page = BeautifulSoup(html_page, "html.parser")
    List_In_Memory = beautiful_html_page.select('div[data-program-id$="X"]')
    for things in List_In_Memory:
        print(things)
