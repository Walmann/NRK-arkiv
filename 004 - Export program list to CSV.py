
import json
with open("Text_Files/" + "List_Of_Programs.txt", "r", encoding="utf-8") as _list:
        with open("Text_Files/" + "List_Of_Programs_CSV.csv", "w", encoding="utf-8") as _New_file:
                new_List = []
                for item in _list:
                        item = json.loads(item)
                        
                        new_List.append(item)

                for item in new_List:
                        for thing in range(len(item)):
                                _New_file.write(str(item[thing]) + "; ")
                        _New_file.write("\n") 