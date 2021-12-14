

from types import NoneType


new_list = NoneType
upper_year_limit = input("Upper year limit (2005 for NRK removal 2022)")
with open("List_Of_Programs_Older_Than.txt", "w", encoding="utf-8") as file:
    with open("List_Of_Programs.txt", "r", encoding="utf-8") as list:
        for item in list:
            if item[2] < upper_year_limit:
                new_list.append(item)
        
        for item in new_list:
            file.write(item + "\n")

            #This script does not work as intended.