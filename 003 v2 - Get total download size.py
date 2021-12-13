# from jsonpath_ng import jsonpath, parse
from jsonpath_ng import jsonpath, parse
import json
from tqdm import tqdm
import humanfriendly
import urllib
from urllib.request import urlopen


def export_JSON_to_file(_json):
    with open("JSON_export.json", "w", encoding="utf-8") as file:
        json.dump(_json, file)
        print("Exported JSON. Press enter to continue.")




def Program_Convert_href_To_Json(Program_href): #Also get avability?
    org_href = Program_href
    JSON_Data = ""
    Program_href_Possibilities = [
        Program_href,
        Program_href.replace("/serie/", "/series/"),
        Program_href.replace("/program/", "/programs/")
    ]
    Finding_JSON = True
    while Finding_JSON == True:
        for Possibilities in Program_href_Possibilities:
            new_href = urllib.parse.quote(Possibilities)
            url = "https://psapi.nrk.no/tv/catalog" + new_href
            
            try:
                JSON_Data = json.loads(urlopen(url).read())
                Finding_JSON = False
                break
            except: 
                # input("Error getting JSON from " + Program_href)
                pass
    return new_href

yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        "quiet": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        "ignoreerrors": True,
    }


# 
# url = "https://tv.nrk.no" + entry[1]
# url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"
url = "https://tv.nrk.no/serie/fleksnes/"


Filesize_Total = 0
with open("List_Of_Programs_Debug.txt", "r", encoding="utf-8") as file_object:
    # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
    file_object = file_object.readlines()
    # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
    # List_Length = len(file_object.readlines())

    Program_List = tqdm(file_object, total=len(file_object), leave=False)
    for Program_Entry in Program_List:
        # Program_Entry = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
        Program_Entry = json.loads(Program_Entry) #Load entry into JSON format: entry [Name, href, ProdYear, Available]
        
        Program_Name = Program_Entry[0]
        Program_href = Program_Entry[1]

        Program_href_For_JSON = Program_Convert_href_To_Json(Program_href)

        # Program_List_Desc = "Current filesize: %s Finding Filesize for %s" % (humanfriendly.format_size(Filesize_Total), Program_Name)
        Program_List_Desc = "Show: %s" % Program_Name
        Program_List.set_description(Program_List_Desc) #Set description for progressbar1
        

        #START Find href to all seasons This does not take long
        seasons_url = "https://psapi.nrk.no/tv/catalog" + urllib.parse.quote(Program_href_For_JSON)
        season_JSON = json.loads(urlopen(seasons_url).read())  
        seasons_href = []
        # export_JSON_to_file(season_JSON)
        season_parse = tqdm(parse('$[_links][seasons][*].href').find(season_JSON), leave=False)
        for entries in season_parse:
            # season_parse.set_description("Seasons: ")
            seasons_href.append(entries.value)

        #STOP Find href to all seasons
         
        
        #START find episodes in season
        season_Entry = tqdm(seasons_href, total=len(seasons_href), leave=False)
        for episodes_in_season in season_Entry:
            season_Entry.set_description("Seasons: ")
            episode_url = "https://psapi.nrk.no" + urllib.parse.quote(episodes_in_season)
            episode_JSON = json.loads(urlopen(episode_url).read())  
            export_JSON_to_file(episode_JSON), input()

            #Find Href for current episode and add to list.
            episode_href = []
            # episode_parse = tqdm(parse('$._embedded.instalments[*]._links.self.href').find(episode_JSON), leave=False )
            episode_parse = tqdm(parse('$._embedded.instalments[*]._links.self.href').find(episode_JSON), leave=False ).set_description("Episodes: ")
            for eposides in episode_parse:
                # episode_name = parse()
                # episode_parse.set_description("Episodes: ")
                episode_href.append(entries.value)
    
        # print(episode_href)
    tqdm.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))

        