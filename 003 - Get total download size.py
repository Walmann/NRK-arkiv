from jsonpath_ng import parse
import json
from tqdm import tqdm
import humanfriendly
import urllib
from urllib.request import urlopen
from os import system
from yt_dlp import YoutubeDL


def func_export_JSON_to_file(_json, filename):
    with open("Text_Files/" + filename, "w", encoding="utf-8") as file:
        json.dump(_json, file)
        # print("Exported JSON. Press enter to continue.")


def func_write_error_to_log(error_message):
    global Amount_Of_Error
    with open("Text_Files/" + "Error.log", "a") as error_file:
        error_file.write(error_message + "\n")
        Amount_Of_Error += 1


def func_Program_Convert_href_To_Json(Program_href_original): #Also get avability?
    Program_href_Possibilities = [
        Program_href_original,
        Program_href_original.replace("/serie/", "/series/"),
        Program_href_original.replace("/program/", "/programs/")
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
    episode_list_itterate.refresh()
    tqdm.write("Current Estimate: " + humanfriendly.format_size(Filesize_Total)+ "| Amount of errors: " + str(Amount_Of_Error))


def func_YouTubeDL(func_yt_url):
    try:
        ytdl = YoutubeDL(yt_dlp_options).extract_info(func_yt_url, download=False)
    except:
        func_write_error_to_log("Error getting JSON info: " + func_yt_url)
        return ("Error")
    jsondump = json.dumps(ytdl)
    Json_Info = json.loads(jsondump)
    return Json_Info

def func_find_show_type(Program_href_find_show):

    if "/serie/" in Program_href_find_show:
        return ("Seasons")
    if "/program/" in Program_href_find_show:
        return ("Show")


def func_retrive_episodes(Program_href_retrive_episode):
    try:
        new_episode_list = []
        show_url = "https://psapi.nrk.no/tv/catalog" + Program_href_retrive_episode.replace("/serie/", "/series/").replace("/program/", "/programs/")
        # url = urllib.parse.unquote(show_url)
        url_open = urlopen(show_url).read()
        JSON = json.loads(url_open)
        if "https://psapi.nrk.no/tv/catalog/series/" in show_url:
            seriesType = parse("$.seriesType").find(JSON)[0].value
            if seriesType == "news":
                episode_list = parse('$._embedded.instalments._embedded.instalments[*]._links.playback.href').find(JSON)
            if seriesType == "sequential":
                episode_list = parse('$._embedded.seasons[*]._embedded.episodes[*]._links.playback.href').find(JSON)
            if seriesType == "standard":
                episode_list = parse('$._embedded.instalments._embedded.instalments.[*]._links.playback.href').find(JSON)
            for element in episode_list:
                new_episode_list.append(str(element.value).replace("/mediaelement", "").replace("/program/", "/programs/"))
        if "https://psapi.nrk.no/tv/catalog/programs/" in show_url:
            new_episode_list.append(str(Program_href_retrive_episode).replace("/mediaelement", "").replace("/program/", "/programs/"))
    except: func_write_error_to_log("Error with Program_href_retrive_episode: " + Program_href_retrive_episode)

    # if "https://psapi.nrk.no/tv/catalog/programs/" in show_url:

    episode_list_sorted = func_check_available_episodes(new_episode_list)

    if not len(new_episode_list) == 0:
        with open("Text_Files/" + "Programs_with_available_content.txt", "a+") as available_list_file:
            if not Program_href_retrive_episode in available_list_file:
                Programs_with_available_items.append(Program_href_retrive_episode)
    return episode_list_sorted


def func_check_available_episodes(episode_list): #(episode_list, JSON, seriesType)
    if isinstance(episode_list, str):
        episode_list = [episode_list]

    new_episode_list = []
    for episodes in episode_list:
        try:
            show_url = "https://psapi.nrk.no/tv/catalog" + episodes
            url_open = urlopen(show_url).read()
            JSON_data = json.loads(url_open)
            parsed_data = parse('$.programInformation.availability.status').find(JSON_data)

            if parsed_data[0].value == "available" or parsed_data[0].value == "expires":
                new_episode_list.append(episodes)
        except:
            try:
                func_write_error_to_log("Error with url in Check_available_episodes: " + show_url)
            except:
                func_write_error_to_log("Error with show_url in Check_available_episodes:: " + episodes)

    return new_episode_list

def func_check_available_programs(Program_href_check_available): #This can be removed. Keeping it for the time being.
    local_program_list = []
    try:
        show_url = "https://psapi.nrk.no/tv/catalog" + str(Program_href_check_available).replace("/mediaelement", "").replace("/program/", "/programs/")
        url_open = urlopen(show_url).read()
        JSON_data = json.loads(url_open)
        parsed_data = parse('$.programInformation.availability.status').find(JSON_data)
        if parsed_data[0].value == "available":
            local_program_list.append(Program_href_check_available)
    except:
        func_write_error_to_log("Error with URL in Check_Available_programs: " + show_url)



    return local_program_list

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
Amount_Of_Error = int()
Programs_with_available_items = []
with open("Text_Files/" + "List_Of_Programs_Older_Than.txt", "r", encoding="utf-8") as file_object:
    # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
    file_object = file_object.readlines()
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
            episode_list = func_retrive_episodes(Program_href)
            if len(episode_list) == 0:  continue
            # show_player_url = "https://tv.nrk.no/" + func_Solve_URL(Program_href)      ##############Solve the URL for tv.nrk.no. replace program, programs etc. Done before.
            try:
                url = "https://tv.nrk.no" + Program_href
                # ytdl_JSON = func_YouTubeDL(url)
                ytdl_file_size = parse('$.filesize_approx').find(func_YouTubeDL(url))[0].value
                func_FileSize("Add", ytdl_file_size)
                continue #TODO: ytdl sliter med æøå i addressefeltet. 
            except:
                # tqdm.write("Error with URL. Noted, and continue loop.")
                func_write_error_to_log("URL Error yt-dlp in main, SHOW section: " + url)
                continue

        if show_type == "Seasons":

            # seasons_JSON = func_retrive_episodes(Program_href)
            episode_JSON = func_retrive_episodes(Program_href)

            episode_list_itterate = tqdm(episode_JSON, total=len(episode_JSON), leave=False, miniters=1, desc="Episode: ")
            for episode in episode_list_itterate:
                try:
                    url = "https://tv.nrk.no" + episode
                    ytdl_file_size = parse('$.filesize_approx').find(func_YouTubeDL(url))[0].value
                    func_FileSize("Add", ytdl_file_size)
                    continue
                except:
                    func_write_error_to_log("URL Error when getting filesize in main, SEASONS: " + url)
                    continue
        else: func_write_error_to_log("Error getting show type: " + show_type + ", Program_href: " + Program_href)

    with open("Text_Files/" + "Programs_with_available_content.txt", "w") as file:
        for line in Programs_with_available_items:
            file.write(line + "\n")
    with open("Text_Files/" + "Download_Size.txt", "w") as file:
        file.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))
    tqdm.write("Current Filesize: " + humanfriendly.format_size(Filesize_Total))
    print("")

