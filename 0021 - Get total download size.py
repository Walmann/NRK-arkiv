from yt_dlp import YoutubeDL
# from jsonpath_ng import jsonpath, parse
import jsonpath_ng
import json
from tqdm import tqdm
import humanfriendly

# def sizeof_fmt(num, suffix="B"):
#     for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
#         if abs(num) < 1024.0:
#             return f"{num:3.1f}{unit}{suffix}"
#         num /= 1024.0
#     return f"{num:.1f}Yi{suffix}"

yt_dlp_options = {
        # "outtmpl": "%(id)s%(ext)s",
        # "noplaylist": True,
        "quiet": True,
        # "format": "bestvideo",
    }



Filesize_Total = 0
with open("List_Of_Programs.txt", "r", encoding="utf-8") as file_object:
    file_object = file_object.readlines()
    # Filesize_Total_Human_Readable = sizeof_fmt(Filesize_Total)
    # List_Length = len(file_object.readlines())

    Program_List = tqdm(file_object, total=len(file_object))
    for entry in Program_List:
        entry = json.loads(entry)
        Program_List_Desc = "Finding Filesize for %s, Current filesize: %s" % (entry[0], humanfriendly.format_size(Filesize_Total))
        Program_List.set_description(Program_List_Desc)


        # entry [Name, href, ProdYear, Available]
        url = "https://tv.nrk.no" + entry[1]
        # url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"
        ytdl = YoutubeDL(yt_dlp_options).extract_info(url, download=False)
        jsondump = json.dumps(ytdl)
        Program_Json_Info = json.loads(jsondump)
        
        # with open("file", "w", encoding="utf-8") as f:
        #     original_stdout = sys.stdout    
        #     sys.stdout = f 
        #     print(Program_Json_Info)
        #     sys.stdout = original_stdout 

        # parseJSON = parse("$['entries'].[:0]['filesize_approx']").find(jsondump).value
        # print(len(parseJSON))
        
        
        Program_File_size_list = [] #Create or reset list.
        for match in jsonpath_ng.parse("$.entries[*].filesize_approx").find(Program_Json_Info):
            # Program_File_size_list.append(match.value)
            # print(match)
            Filesize_Total = Filesize_Total + match.value
        
        


    print("Total filesize: " + humanfriendly.format_size(Filesize_Total) + "In Bytes: " + Filesize_Total)
        # Program_Prod_Year = parse('$..productionYear').find(Program_Json)[0].value