
import string

from bs4.element import Script
import requests
# import yt_dlp

# extra_letters = "ae, oe, aa, 0-9"
# letters = string.ascii_lowercase
# letters = list(string.ascii_lowercase)
# letters.extend(extra_letters)

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ae", "oe", "aa", "0-9"]
# letters = ["ae", "oe", "aa", "0-9"]
print(letters)
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

import subprocess
import sys
from yt_dlp import YoutubeDL
from selenium import webdriver

def Write_To_File(Variable):
    with open("Error_Variable.txt", "a", encoding="utf-8") as file_object:
        file_object.write(str(Variable))



def Get_Program_Id(Program_href):
    ydl_opts = {'playlistend': 1, 'ignoreerrors': True}
    url = "https://tv.nrk.no" + Program_href
    # url = "https://tv.nrk.no/serie/animanimals"
    Program_Json = YoutubeDL(ydl_opts).extract_info(url, download=False)
    try:
        return Program_Json['entries'][0]['id']
    except:
        try: Program_Json['id']
        except:
            try: 
                if Program_Json['entries'] == [None]:
                    return "None"
                else: return Program_Json['entries'] 
            except: print("Could not find ID"), Write_To_File(Program_Json), input()
    

def Get_Program_Year(Program_ID):
    from urllib.request import urlopen
    url = "https://psapi.nrk.no/tv/catalog/programs/" + Program_ID
    Program_Json = json.loads(urlopen(url).read())
    return Program_Json['moreInformation']['productionYear']
    
def Check_Avability(Program_ID):
    from urllib.request import urlopen
    url = "https://psapi.nrk.no/tv/catalog/programs/" + Program_ID
    Program_Json = json.loads(urlopen(url).read())
    return Program_Json['programInformation']['availability']['status']


def Get_Program_ID_Year_Avability(Program_href): 
    from urllib.request import urlopen
    url = "https://psapi.nrk.no/tv/catalog/" + Program_href
    Program_Json = json.loads(urlopen(url).read())
    Program_ID = Program_ID[]
    return Program_ID, Program_Year, Program_Avability
    input()

List_In_Memory = []
amount = 0

chromedriver_path =  "./chromedriver.exe"
options = webdriver.ChromeOptions()
# options.binary_location = chromedriver_path
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--window-size=800x800")
options.add_argument("--mute-audio")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument('--disable-extensions')
# options.add_argument('--disable-gpu')

for link in letters:
    driver = webdriver.Chrome(chrome_options=options,executable_path=chromedriver_path)
    driver.get("https://tv.nrk.no/alle-programmer/" + link)
    # time.sleep(1)
    html_page = driver.page_source
    beautiful_html_page = BeautifulSoup(html_page, "html.parser")
    List_In_Memory = beautiful_html_page.find_all("a", class_="tv-cl-letter-element tv-text-styles-subhead")
    amount += 1



#    TODO: Fix the extra_letters pages not being included.
    with open("List_Of_Programs.txt", "a", encoding="utf-8") as file_object:
        for item in List_In_Memory:
            Program_href = item["href"]
            Program_ID, Program_Year, Program_Avability = Get_Program_ID_Year_Avability(Program_ID)
            # Program_ID = Get_Program_Id(Program_href)
            if not Program_ID == "None":
                if Check_Avability(Program_ID) == "available":
                    Program_ID, Program_Year, Program_Avability = Get_Program_Year(Program_ID)
                    array = [item.text,Program_href, Program_ID, Program_Year]
                    json.dump(array, file_object, ensure_ascii=False)
                    file_object.write("\n")
                    print(array)
                    input
print(amount)
# ["program", /serie/programlink]
    