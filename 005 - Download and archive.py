import subprocess
import os.path
import urllib
from tqdm import tqdm
import json

import yt_dlp
from yt_dlp import YoutubeDL

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
        "ignoreerrors": True,
        "no_warnings:": True,
        # "extract_flat": True,
        "outtmpl": "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s",
    }


debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"

# yt_dlp_command= 'yt-dlp.exe ' + debug_eposide + ' -o "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s '
# subprocess.run(yt_dlp_command)

with open("Text_Files/" + "Programs_with_available_content.txt", "r", encoding="utf-8") as file_object:
    # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
    file_object = file_object.readlines()
    # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
    # List_Length = len(file_object.readlines())

    # Program_List = tqdm(file_object, total=len(file_object), leave=False, miniters=1)
    # for Program_Entry in Program_List:

    YoutubeDL(yt_dlp_options).download(debug_eposide)
    print("")
