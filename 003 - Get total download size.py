# from jsonpath_ng import jsonpath, parse
from ctypes import GetLastError
from jsonpath_ng import jsonpath, parse
import json
from tqdm import tqdm
import humanfriendly
import urllib
from urllib.request import urlopen
# import m3u8
from os import system
from yt_dlp import YoutubeDL
import yt_dlp

# from Temp_Files import find_all_show_types

def func_export_JSON_to_file(_json, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(_json, file)
        # print("Exported JSON. Press enter to continue.")


def func_write_error_to_log(error_message):
    with open("Error.log", "a") as file:
        file.write(error_message + "\n")


def func_Program_Convert_href_To_Json(Program_href): #Also get avability?
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


def func_FileSize(Get_or_Add, number):
    global Filesize_Total
    if Get_or_Add == "Add":
        Filesize_Total = Filesize_Total + number
    if Get_or_Add == "Get":
        return(Filesize_Total)

    # Update Progressbars:
    clear()
    Program_List.refresh()
    # seasons_parse.refresh()


def func_YouTubeDL(url):
    try:
        ytdl = YoutubeDL(yt_dlp_options).extract_info(url, download=False)
    except:
        func_write_error_to_log("Error getting JSON info: " + url)
        return ("Error")
    jsondump = json.dumps(ytdl)
    Json_Info = json.loads(jsondump)
    return Json_Info

def func_find_show_type(Program_href):

    if "/serie/" in Program_href:
        return ("Seasons")
    if "/program/" in Program_href:
        return ("Show")


def func_retrive_seasons(show_JSON):
    show_href = []
    show_parse = parse('$[_links][seasons][*].href').find(show_JSON)
    for seasons in show_parse:
        # season_parse.set_description("Seasons: ")
        show_href.append(seasons.value)
    #STOP Find href to all seasons


    #START find seasons in Show
    seasons_parse = tqdm(show_href, total=len(show_href), leave=False, miniters=1)
    for seasons_href in seasons_parse:
        seasons_parse.set_description("Seasons: ")
        season_url = "https://psapi.nrk.no" + urllib.parse.quote(seasons_href)
        season_JSON = json.loads(urlopen(season_url).read())
    return ()


def func_retrive_episodes(Program_href):
    show_url = "https://psapi.nrk.no/tv/catalog" + Program_href.replace("/serie/", "/series/")
    # url = urllib.parse.unquote(show_url)
    url_open = urlopen(show_url).read()
    JSON = json.loads(url_open)
    seriesType = parse("$.seriesType").find(JSON)[0].value

    if seriesType == "news":
        episode_list = parse('$._embedded.instalments._embedded.instalments[*]._links.playback.href').find(JSON)
    if seriesType == "sequential":
        episode_list = parse('$._embedded.seasons[*]._embedded.episodes[*]._links.playback.href').find(JSON)
    if seriesType == "standard":
        episode_list = parse('$._embedded.instalments._embedded.instalments.[*]._links.playback.href').find(JSON)

    episode_list = func_check_available_episodes(episode_list, JSON, seriesType)


    return episode_list


def func_check_available_episodes(episode_list, JSON, seriesType):
    new_episode_list = []
    for episodes in episode_list:
        try:
            show_url = "https://psapi.nrk.no/tv/catalog" + str(episodes.value).replace("/mediaelement", "").replace("/program/", "/programs/")
            url_open = urlopen(show_url).read()
            JSON_data = json.loads(url_open)
            parsed_data = parse('$.programInformation.availability.status').find(JSON_data)
            if parsed_data[0].value == "available":
                new_episode_list.append(episodes)
            return new_episode_list
        except:
            func_write_error_to_log("Error with URL: " + show_url)
            return new_episode_list

def func_check_available_programs(Program_href):
    new_episode_list = []
    try:
        show_url = "https://psapi.nrk.no/tv/catalog" + str(Program_href).replace("/mediaelement", "").replace("/program/", "/programs/")
        url_open = urlopen(show_url).read()
        JSON_data = json.loads(url_open)
        parsed_data = parse('$.programInformation.availability.status').find(JSON_data)
        if parsed_data[0].value == "available":
            new_episode_list.append(Program_href)
        return new_episode_list
    except:
        func_write_error_to_log("Error with URL: " + show_url)
        return new_episode_list


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
        # "verbose": True,
        # "no_verbose_header": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        "ignoreerrors": True,
        "no_warnings:": True,
        # "extract_flat": True,
    }

Filesize_Total = int()
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


        # Program_List_Desc = "Current filesize: %s Finding Filesize for %s" % (humanfriendly.format_size(Filesize_Total), Program_Name)
        Program_List_Desc = "Show: %s" % Program_Name
        Program_List.set_description(Program_List_Desc) #Set description for progressbar1



        show_type = func_find_show_type(Program_href)
        if show_type == "Show":
            episode_list = []
            episode_list = func_check_available_programs(Program_href)
            if len(episode_list) == 0:  break
            # show_player_url = "https://tv.nrk.no/" + func_Solve_URL(Program_href)      ##############Solve the URL for tv.nrk.no. replace program, programs etc. Done before.
            try:
                url = "https://tv.nrk.no" + Program_href
                # ytdl_JSON = func_YouTubeDL(url)
                ytdl_file_size = parse('$.filesize_approx').find(func_YouTubeDL(url))[0].value
                func_FileSize("Add", ytdl_file_size)
                continue #TODO: ytdl sliter med æøå i addressefeltet.
            except:
                tqdm.write("Error with URL. Noted, and continue loop.")
                func_write_error_to_log("URL Error: " + url)
                continue

        if show_type == "Seasons":
            # season_JSON = func_retrive_seasons(show_JSON)
            # seasons_JSON = func_retrive_episodes(Program_href)
            episode_JSON = func_retrive_episodes(Program_href)

            for episode in tqdm(episode_JSON, total=len(episode_JSON), leave=False, miniters=1, desc="Episode: "):
                try:
                    url = "https://tv.nrk.no" + episode.value.replace("/mediaelement", "")
                    ytdl_file_size = parse('$.filesize_approx').find(func_YouTubeDL(url))[0].value
                    func_FileSize("Add", ytdl_file_size)
                except:
                    tqdm.write("Error with URL. Noted, and continue loop.")
                    func_write_error_to_log("URL Error: " + url)
                    continue
        else: func_write_error_to_log("Error getting show type: " + show_type)
        tqdm.write(Program_Name)

    with open("Download_Size.txt", "w") as file:
        file.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))
    tqdm.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))
    print("")

