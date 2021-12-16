# from jsonpath_ng import jsonpath, parse
from ctypes import GetLastError
from jsonpath_ng import jsonpath, parse
import json
from tqdm import tqdm
import humanfriendly
import urllib
from urllib.request import urlopen
import m3u8
from os import system
from yt_dlp import YoutubeDL

def export_JSON_to_file(_json, filename):
    with open("./Temp Files/" + filename, "w", encoding="utf-8") as file:
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


def FileSize(Get_or_Add, number):
    if Get_or_Add == "Add":
        Filesize_Total = Filesize_Total + number
    if Get_or_Add == "Get":
        return(Filesize_Total)

    # Update Progressbars: 
    Program_List.refresh()
    seasons_parse.refresh()
    clear()

def func_YouTubeDL(url):
    ytdl = YoutubeDL(yt_dlp_options).extract_info(url, download=False)
    jsondump = json.dumps(ytdl)
    Json_Info = json.loads(jsondump)
    return Json_Info


# 
# url = "https://tv.nrk.no" + entry[1]
# url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"
# url = "https://tv.nrk.no/serie/fleksnes/"



clear = lambda: system('cls') #on Windows System
clear()

yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        "quiet": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        "ignoreerrors": True,
    }

Filesize_Total = 0
with open("List_Of_Programs_Debug.txt", "r", encoding="utf-8") as file_object:
    # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
    file_object = file_object.readlines()
    # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
    # List_Length = len(file_object.readlines())

    Program_List = tqdm(file_object, total=len(file_object), leave=False, miniters=1)
    for Program_Entry in Program_List:
        
        # Program_Entry = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
        Program_Entry = json.loads(Program_Entry) #Load entry into JSON format: entry [Name, href, ProdYear, Available]
        
        Program_Name = Program_Entry[0]
        Program_href = Program_Entry[1]

        # if Program_Name in Excluded_List:


        Program_href_For_JSON = Program_Convert_href_To_Json(Program_href)

        # Program_List_Desc = "Current filesize: %s Finding Filesize for %s" % (humanfriendly.format_size(Filesize_Total), Program_Name)
        Program_List_Desc = "Show: %s" % Program_Name
        Program_List.set_description(Program_List_Desc) #Set description for progressbar1
        

        #START Find href to all seasons This does not take long
        show_url = "https://psapi.nrk.no/tv/catalog" + urllib.parse.quote(Program_href_For_JSON)
        url = urllib.parse.unquote(show_url)
        url_open = urlopen(url).read()
        show_JSON = json.loads(url_open)


        #Check if is a show or series: 
        check_for_show = parse('category.id').find(show_JSON)

        if check_for_show.value == "dokumentar":
            func_Solve_URL()      ##############Solve the URL for tv.nrk.no. replace program, programs etc. Done before.
            func_YouTubeDL(url)


        show_href = []
        # export_JSON_to_file(season_JSON)
        show_parse = parse('$[_links][seasons][*].href').find(show_JSON)
        for seasons in show_parse:
            # season_parse.set_description("Seasons: ")
            show_href.append(seasons.value)
            

        #STOP Find href to all seasons
         
        
        #START find episodes in season
        seasons_parse = tqdm(show_href, total=len(show_href), leave=False, miniters=1)
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

            episode_progress_bar = tqdm(episode_href, total=len(episode_href), leave=False, miniters=1)
            for episodes in episode_progress_bar:
                episode_progress_bar.set_description("Episodes: ")
                episode_url = "https://tv.nrk.no" + Program_href + "/" + episodes
                episode_Json_Info = func_YouTubeDL(episode_url)
                
                # export_JSON_to_file(episode_Json_Info, "Episode_Youtube_dl.json")
                
                episode_Json_Parsed = parse('$.filesize_approx').find(episode_Json_Info)
                for parsed_entry in episode_Json_Parsed:
                    FileSize("Add", parsed_entry.value)

                    # Filesize_Total = Filesize_Total + parsed_entry.value

                    # # Update Progressbars: 
                    # Program_List.refresh()
                    # seasons_parse.refresh()
                    # clear()


#region
            # episodes_href_tqdm = tqdm(episode_href, leave=False, miniters=0)
            # for episode_prfId in episodes_href_tqdm:
            #     episodes_href_tqdm.set_description("Episodes size: ")
                
            #     #Get manifestfile:
            #     episode_manifest_url = "https://psapi.nrk.no/playback/manifest/program/" + urllib.parse.quote(episode_prfId)
            #     episode_manifest_JSON = json.loads(urlopen(episode_manifest_url).read())

                

            #     try: m3u8_parse = parse('playable.assets[0].url').find(episode_manifest_JSON)[0].value
            #     except: break

            #     try: 
            #         m3u8_obj = m3u8.load(m3u8_parse)
            #     except: 
            #         retry_counter = 0
            #         while retry_counter > 10:
            #             import time
            #             time.sleep(5)
            #             tqdm.write("Got error getting m3u8 file. Waiting 5 seconds.")
            #             m3u8_obj = m3u8.load(m3u8_parse)
            #             retry_counter +=1
            #         if retry_counter < 10:
            #             break
                

            #     #Find biggest file, usually means best resolution
            #     biggest_filesize = 0
            #     for item in tqdm(m3u8_obj.playlists, leave=False, desc="Find biggest: ", mininterval= 1):
            #         if item.stream_info.bandwidth > biggest_filesize:
            #             biggest_filesize = item.stream_info.bandwidth
            #         else: continue
                
                #Update Progressbars: 
                # Program_List.refresh()
                # seasons_parse.refresh()


                # Filesize_Total = Filesize_Total + biggest_filesize
                # clear()
#endregion  
    
    with open("Download_Size.txt", "w") as file: 
        file.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))
    tqdm.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))

        