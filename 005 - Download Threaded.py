import subprocess
import os.path
import urllib
from tqdm import tqdm
import json
import multiprocessing
# import tkinter as tk
import yt_dlp
from yt_dlp import YoutubeDL


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
    if d['status'] == 'download':
        None
        # tqdm.write("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")

    if d['status'] == 'finished':
        filename=d['filename']
        print("Done downloading " + filename)

    if d['status'] == 'error':
        None

#Check for files needed:
if not os.path.isfile("./yt-dlp.exe"):
    input("yt-dlp.exe is missing. Go to https://github.com/yt-dlp/yt-dlp to download. (newest version when creating script is 2021.12.01) \n Place the EXE file in root folder of this script.")


def func_get_yt_dlp_options(show_type):
    if show_type == "serie":
        output_template = "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s"
    # if show_type == "program":
    
    yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        "quiet": True,
        # "verbose": True,
        "no_verbose_header": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        "progress_hooks": [my_hook],
        # "ignoreerrors": True,
        "no_warnings:": True,
        # "extract_flat": True,
        "outtmpl": output_template, 
        # 'prefer_ffmpeg': True,
        # "ffmpeg_location": "dep/ffmpeg.exe",
        "external_downloader_args":['-loglevel quiet','-hide_banner'],
        "extractor_retries": 100,
        "retries": 100,
        }
    return yt_dlp_options


debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"

# yt_dlp_command= 'yt-dlp.exe ' + debug_eposide + ' -o "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s '
# subprocess.run(yt_dlp_command)

def func_download_list(list): 
    # list_object_progressbar = tqdm(list, total=len(list), leave=False, miniters=1)
    for programs in list:
        url_download = "https://tv.nrk.no" + programs
        try:
            if programs.startswith("/serie/"):
                print(func_get_yt_dlp_options("serie"))
                YoutubeDL(func_get_yt_dlp_options()).download(url_download)
                print("Finnised downloading " + programs)
                # func_add_program_to_downloaded(programs)
            # if programs.startswith("/program/")
        except: func_write_error_to_log("Error downloading: " + programs)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

Amount_Of_Error = 0


if __name__ == "__main__":
    with open("Text_Files/" + "Programs_with_available_content.txt", "r", encoding="utf-8") as file_object:
        file_object = file_object.readlines()
        program_list = list(split(file_object, 10))
        # print(length_per_group)
        pool = multiprocessing.Pool(10)

        # master = tk.Tk()
        # master.mainloop()
        # master.geometry("50x200")
        # newWindow = tk.Toplevel(master)
        # newWindow.title("Helllo World!")
        # Label(master, text="Enter coins.[Press Buttons]").grid(row=1, column=1)
        pool.map(func_download_list, program_list)
    
            
    # file_object = '["Aktuelt - TV", "/serie/aktuelt-tv", 2015, "Available"]'
    # file_object = file_object.readlines()
    # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
    # List_Length = len(file_object.readlines())

    # Program_List = tqdm(file_object, total=len(file_object), leave=False, miniters=1)
    # for Program_Entry in Program_List:

    
    # print("")
