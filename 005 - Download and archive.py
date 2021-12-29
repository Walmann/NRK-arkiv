import os.path
import urllib
from tqdm import tqdm
import multiprocessing
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
        filename=d['filename']
        print(filename)

    if d['status'] == 'finished':
        # filename=d['filename']
        # print("Done downloading " + filename)

    if d['status'] == 'error':
        None


def func_get_yt_dlp_options(show_type):
    if show_type == "serie":
        output_template = "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s"
    if show_type == "program":
        output_template = "Download Folder/%(title)s/%(title)s"

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


#Check for files needed:
if not os.path.isfile("./yt-dlp.exe"):
    input("yt-dlp.exe is missing. Go to https://github.com/yt-dlp/yt-dlp to download. (newest version when creating script is 2021.12.01) \n Place the EXE file in root folder of this script.")


debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"


def func_download_list(list):
    for programs in list:
        url_download = "https://tv.nrk.no" + programs
        try:
            if programs.startswith("/serie/"):

                YoutubeDL(func_get_yt_dlp_options("serie")).download(url_download)
            if programs.startswith("/program/"):
                YoutubeDL(func_get_yt_dlp_options("program")).download(url_download)
        except:
            func_write_error_to_log("Error downloading: " + programs)
            continue

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
        pool.map(func_download_list, program_list)



