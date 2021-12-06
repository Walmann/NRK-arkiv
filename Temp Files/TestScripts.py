# from bs4.element import Script
# import requests
#

# import requests
# from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

import subprocess
import sys
from yt_dlp import YoutubeDL
from selenium import webdriver
import urllib
from urllib.request import urlopen
from jsonpath_ng import jsonpath, parse


Program_href = "/series/animanimals"
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




Program_Available_List = []
# match = parse('$..productionYear').find(Program_Json)
Program_Prod_Year = parse('$..productionYear').find(Program_Json)[0].value
# Program_Available_List_Parse = parse('$..availability.status')

for match in parse('$..availability.status').find(Program_Json):
    Program_Available_List.append(match.value)


if "available" in Program_Available_List:
    Program_Available = "Available"
else: Program_Available = "Not Available"


print(Program_Available)