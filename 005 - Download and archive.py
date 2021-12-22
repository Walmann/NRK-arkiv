# import subprocess
# import urllib
# import json
# import yt_dlp
from tqdm import tqdm
import os.path
from yt_dlp import YoutubeDL
import time


#Global Variables: 
Amount_Of_Runs = 0
Amount_Of_Error = 0



def func_write_error_to_log(error_message):
    global Amount_Of_Error
    with open("Text_Files/" + "Error.log", "a") as error_file:
        error_file.write(error_message)
        Amount_Of_Error += 1


def func_add_program_to_downloaded(Program_Add_To_List):
    with open("Text_Files" + "Programs_Already_Downloaded.log", "a") as log_file:
        log_file.write(Program_Add_To_List + "\n")


def func_check_if_program_is_already_downloaded(program_to_check):
    try:
        with open("Text_Files/" + "Programs_Already_Downloaded.log", "r") as log_file: 
            if program_to_check in log_file:
                return True
            else: return False
    except: 
        with open("Text_Files/" + "Programs_Already_Downloaded.log", 'w') as document: func_check_if_program_is_already_downloaded(program_to_check)



def my_hook(d):
    if d['status'] == 'downloading':
        tqdm.write("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        filename=d['filename']
        tqdm.write(filename)

#Check for files needed:
if not os.path.isfile("./yt-dlp.exe"):
    input("yt-dlp.exe is missing. Go to https://github.com/yt-dlp/yt-dlp to download. (newest version when creating script is 2021.12.01) \n Place the EXE file in root folder of this script.")



yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        "quiet": True,
        # "verbose": True,
        # "no_verbose_header": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        # "progress_hooks": [my_hook],
        "ignoreerrors": True,
        "no_warnings:": True,
        # "extract_flat": True,
        "outtmpl": "Download Folder/%(series)s/Sessong %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s",
        # 'prefer_ffmpeg': True,
        # "ffmpeg_location": "dep/ffmpeg.exe",
        "external_downloader_args":['-loglevel quiet','-hide_banner'],
    }


debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"

# yt_dlp_command= 'yt-dlp.exe ' + debug_eposide + ' -o "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s '
# subprocess.run(yt_dlp_command)

def func_download():
    Amount_Of_Error = 0
    with open("Text_Files/" + "Programs_with_available_content.txt", "r", encoding="utf-8") as file_object:
        file_object = file_object.readlines()
        file_object_progressbar = tqdm(file_object, total=len(file_object), leave=False, miniters=1)
        for programs in file_object:
            # if func_check_if_program_is_already_downloaded(programs):
            #     continue
            file_object_progressbar.set_description("Show: " + programs)
            url_download = "https://tv.nrk.no" + programs
            try:
                tqdm.write(YoutubeDL(yt_dlp_options).download(url_download))
                # func_add_program_to_downloaded(programs)
            except: func_write_error_to_log("Error downloading: " + programs)
                
        # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
        # file_object = file_object.readlines()
        # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
        # List_Length = len(file_object.readlines())

        # Program_List = tqdm(file_object, total=len(file_object), leave=False, miniters=1)
        # for Program_Entry in Program_List:
    global Amount_Of_Runs
    Amount_Of_Runs +=1 


Amount_Of_Runs = 0
while Amount_Of_Runs <= 10:
    Amount_Of_Runs = 0
    func_download()
    time.sleep(600)
else: tqdm.write("Script is done.")