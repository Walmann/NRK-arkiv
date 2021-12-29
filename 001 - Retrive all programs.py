from bs4 import BeautifulSoup
import json

import subprocess
import sys
from yt_dlp import YoutubeDL
from selenium import webdriver
import urllib
from urllib.request import urlopen
from jsonpath_ng import jsonpath, parse


def Write_To_File(Variable):
    print("Writing Error to file: ")
    with open("Error_Variable.txt", "w", encoding="utf-8") as file_object:
        file_object.write(str(Variable))


def Program_Prod_Year(Program_href): #Also get avability?
    org_href = Program_href
    Program_Json = ""
    Program_href_Possibilities = [
        Program_href,
        Program_href.replace("/serie/", "/series/"),
        Program_href.replace("/program/", "/programs/")
    ]
    Finding_JSON = True
    while Finding_JSON == True:
        for Possibilities in Program_href_Possibilities:
            url = "https://psapi.nrk.no/tv/catalog" + urllib.parse.quote(Possibilities)
            
            try:
                Program_Json = json.loads(urlopen(url).read())
                Finding_JSON = False
                break

            except: 
                # input("Error getting JSON from " + Program_href)
                pass

    
    #Get production year
    Program_Prod_Year = parse('$..productionYear').find(Program_Json)[0].value


    #Check if available. Even if it's only a few episodes
    Program_Available_List = [] #Create or reset list.
    for match in parse('$..availability.status').find(Program_Json):
        Program_Available_List.append(match.value)

    if "available" in Program_Available_List:
        Program_Available = "Available"
    else: Program_Available = "Not Available"



    # print(Program_Prod_Year)
    return Program_Prod_Year, Program_Available


def Get_List_Of_Programs(): #Get list of programs and put them into List_Of_Programs.txt
    List_In_Memory = []
    amount = 0
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ae", "oe", "aa", "0-9"]

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

    #Itterate through links
    Last_Link_Used = ""
    for link in letters:
        driver = webdriver.Chrome(chrome_options=options,executable_path=chromedriver_path)
        driver.get("https://tv.nrk.no/alle-programmer/" + link)
        # time.sleep(1)
        html_page = driver.page_source
        beautiful_html_page = BeautifulSoup(html_page, "html.parser")
        List_In_Memory = beautiful_html_page.find_all("a", class_="tv-cl-letter-element tv-text-styles-subhead")
        amount += 1


        #Write to file
        with open("List_Of_Programs.txt", "a", encoding="utf-8") as file_object:
            for item in List_In_Memory:
                Program_href = item["href"]
                Prod_Year, Available = Program_Prod_Year(Program_href)
                array = [item.text,Program_href, Prod_Year, Available]
                json.dump(array, file_object, ensure_ascii=False)
                file_object.write("\n")
                print(array)
                Last_Link_Used = link
    if not Last_Link_Used == "0-9":
        print("Last link is not '0-9'. This could mean the loop did not fully work. Manually check List_Of_Programs for errors.")
    print(amount)

Get_List_Of_Programs()
# ["program", /serie/programlink]
    