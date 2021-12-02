from bs4.element import Script
import requests
#

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

import subprocess
import sys
from yt_dlp import YoutubeDL
from selenium import webdriver
from urllib.request import urlopen

def Write_To_File(Variable):
    print("Writing Error to file: ")
    with open("Error_Variable.txt", "w", encoding="utf-8") as file_object:
        file_object.write(str(Variable))


def Program_Prod_Year(Program_href):
    org_href = Program_href
    Program_Json = ""
    # url = "https://psapi.nrk.no/tv/catalog" + Program_href
    try:
        url = "https://psapi.nrk.no/tv/catalog" + Program_href
        Program_Json = json.loads(urlopen(url).read())
    except: 
        try: 
            Program_href = Program_href.replace("/serie/", "/series/").replace("/program/", "/programs/")
            url = "https://psapi.nrk.no/tv/catalog" + Program_href
            Program_Json = json.loads(urlopen(url).read())
            Write_To_File(Program_Json)
        except:
            print("Error in getting JSON value")
            print("Lets see.")
            input()

    try:                
        Program_Prod_Year = Program_Json['_embedded']['instalments']['_embedded']['instalments'][0]['productionYear']
    except:
        try:
            Program_Prod_Year = Program_Json['moreInformation']['productionYear']
        except:
            try:
                Program_Prod_Year = Program_Json['_embedded']['seasons'][0]['_embedded']['episodes'][0]['productionYear']
            except:
                Print("Error")
                



    # print(Program_Prod_Year)
    return Program_Prod_Year


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

    #Itterate through 
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
                array = [item.text,Program_href, Program_Prod_Year(Program_href)]
                json.dump(array, file_object, ensure_ascii=False)
                file_object.write("\n")
                print(array)
                input
    print(amount)

Get_List_Of_Programs()
# ["program", /serie/programlink]
    