import yt_dlp 

url= "https://tv.nrk.no/program/F%C3%98ST70001193"
# url= "https://tv.nrk.no/serie/groenn-hverdag-mitt-valge/1990/FHLD30000290"


try: 
    yt_dlp.YoutubeDL().extract_info(url)
except: print("Error")