import subprocess
import os.path


#Check for files needed:
if not os.path.isfile("./yt-dlp.exe"):
    input("yt-dlp.exe is missing. Go to https://github.com/yt-dlp/yt-dlp to download. (newest version when creating script is 2021.12.01) \n Place the EXE file in root folder of this script.")

# try: 
#     subprocess.run("ffmpeg --version")
# except: input("ffmpeg is missing. Go to https://ffmpeg.org/download.html#build-windows to download. Might create install script later.")

#Check if yt-dlp is downloaded. Point them towards yt-dlp release page. Note wich version this program is made for

#Check if ffmpeg is installed. PiP?



debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"

yt_dlp_command= 'yt-dlp.exe ' + debug_eposide + ' -o "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s '
subprocess.run(yt_dlp_command)