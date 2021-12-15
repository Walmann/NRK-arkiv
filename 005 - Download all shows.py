import subprocess



debug_eposide = "https://tv.nrk.no/serie/minibarna/sesong/2/episode/1"

yt_dlp_command= 'yt-dlp.exe ' + debug_eposide + ' -o "Download Folder/%(series)s/Season %(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s '
subprocess.run(yt_dlp_command)