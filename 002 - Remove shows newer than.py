
import json

# Program_Entry = json.loads(Program_Entry)
new_list = []
upper_year_limit = int(input("Upper year limit (2015 for NRK removal jan. 2022): "))
# Exclude_List_Decision = input("Do you want to include extra programs? (Programs that are big, and not getting removed): ")


Exclude_List = ["Dagsrevyen", "Aktuelt - TV"]


with open("List_Of_Programs_Older_Than.txt", "w", encoding="utf-8") as file:
    with open("List_Of_Programs.txt", "r", encoding="utf-8") as _list:
        
        for item in _list:
            _item = json.loads(item)
            if int(_item[2]) > upper_year_limit or _item[0] not in Exclude_List:
                new_list.append(_item)
        
        for item in new_list:
            json.dump(item, file, ensure_ascii=False)
            file.write("\n")


            #This script does not work as intended.