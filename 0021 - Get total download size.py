from yt_dlp import YoutubeDL
# from jsonpath_ng import jsonpath, parse
import jsonpath_ng
import json
import sys



with open("List_Of_Programs.txt", "r", encoding="utf-8") as file_object:
    for entry in file_object:
        # entry [Name, href, ProdYear, Available]
        url = "https://tv.nrk.no" + json.loads(entry)[1]
        # url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"
        ytdl = YoutubeDL().extract_info(url, download=False)
        jsondump = json.dumps(ytdl)
        Program_Json_Info = json.loads(jsondump)
        
        with open("file", "w", encoding="utf-8") as f:
            original_stdout = sys.stdout    
            sys.stdout = f 
            print(Program_Json_Info)
            sys.stdout = original_stdout 

        # parseJSON = parse("$['entries'].[:0]['filesize_approx']").find(jsondump).value
        # print(len(parseJSON))
        
        
        Program_File_size_list = [] #Create or reset list.
        for match in jsonpath_ng.parse("$['entries'].[:0]['filesize_approx']").find(Program_Json_Info):
            Program_File_size_list.append(match)
            print(match)
        print("")

        print(url)
        # Program_Prod_Year = parse('$..productionYear').find(Program_Json)[0].value