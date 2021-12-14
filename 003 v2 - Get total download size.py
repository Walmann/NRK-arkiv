# from jsonpath_ng import jsonpath, parse
from jsonpath_ng import jsonpath, parse
import json
from tqdm import tqdm
import humanfriendly
import urllib
from urllib.request import urlopen
import m3u8
from os import system

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


# 
# url = "https://tv.nrk.no" + entry[1]
# url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"
# url = "https://tv.nrk.no/serie/fleksnes/"



clear = lambda: system('cls') #on Windows System
clear()


Filesize_Total = 0
with open("List_Of_Programs.txt", "r", encoding="utf-8") as file_object:
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
        show_url = "https://psapi.nrk.no/tv/catalog" + urllib.parse.quote(Program_href_For_JSON)
        url_open = urlopen(urllib.parse.unquote(show_url)).read()
        show_JSON = json.loads(url_open)  



        show_href = []
        # export_JSON_to_file(season_JSON)
        show_parse = tqdm(parse('$[_links][seasons][*].href').find(show_JSON), leave=False)
        for seasons in show_parse:
            # season_parse.set_description("Seasons: ")
            show_href.append(seasons.value)
            

        #STOP Find href to all seasons
         
        
        #START find episodes in season
        seasons_parse = tqdm(show_href, total=len(show_href), leave=False)
        for seasons_href in seasons_parse:
            seasons_parse.set_description("Seasons: ")
            season_url = "https://psapi.nrk.no" + urllib.parse.quote(seasons_href)
            season_JSON = json.loads(urlopen(season_url).read())  


            #Find Href for current episode and add to list.
            episode_href = []
            #Need to find if program uses Episodes, or instalments:
            episode_parse = parse('$._embedded.instalments[*].prfId').find(season_JSON)
            if len(episode_parse) == "0":
                episode_parse = parse('$._embedded.episodes[*].prfId').find(season_JSON)
                # tqdm.write("Using backup episode parse")



            for episodes in episode_parse:
                episode_href.append(episodes.value)

            episodes_href_tqdm = tqdm(episode_href, leave=False)
            for episode_prfId in episodes_href_tqdm:
                episodes_href_tqdm.set_description("Episodes Href: ")
                
                #Get manifestfile:
                episode_manifest_url = "https://psapi.nrk.no/playback/manifest/program/" + urllib.parse.quote(episode_prfId)
                episode_manifest_JSON = json.loads(urlopen(episode_manifest_url).read())

                

                try: m3u8_parse = parse('playable.assets[0].url').find(episode_manifest_JSON)[0].value
                except: break

                try: 
                    m3u8_obj = m3u8.load(m3u8_parse)
                except: 
                    retry_counter = 0
                    while retry_counter > 10:
                        import time
                        time.sleep(5)
                        m3u8_obj = m3u8.load(m3u8_parse)
                        retry_counter +=1
                    if retry_counter < 10:
                        break
                

                #Find biggest file, usually means best resolution
                biggest_filesize = 0
                for item in tqdm(m3u8_obj.playlists, leave=False, desc="Find biggest: "):
                    if item.stream_info.bandwidth > biggest_filesize:
                        biggest_filesize = item.stream_info.bandwidth
                    else: continue
                
                #Update Progressbars: 
                Program_List.refresh()
                seasons_parse.refresh()


                Filesize_Total = Filesize_Total + biggest_filesize

    
        # print(episode_href)
    tqdm.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))

        