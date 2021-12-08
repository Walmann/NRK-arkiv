from yt_dlp import YoutubeDL

url = "https://tv.nrk.no/serie/aktuelt-tv"


yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        # "quiet": True,
        # "format": "bestvideo",
        # "ignore_no_formats_error": True,
        "ignoreerrors": True,
    }


amount = 0
for i in YoutubeDL(yt_dlp_options).extract_info(url, download=False):
    print("Gotten %d json files" % amount)
    amount =+1 