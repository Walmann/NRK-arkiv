import yt_dlp
from jsonpath_ng import parse
from json import dump

def func_export_JSON_to_file(_json, filename):
    with open("./Temp Files/" + filename, "w", encoding="utf-8") as file:
        dump(_json, file)
        # print("Exported JSON. Press enter to continue.")


def func_write_error_to_log(error_message):
    with open("Error.log", "a") as file:
        file.append(error_message)




def func_write_to_files(check_for_show_type):
    with open("Show_Types.txt", "r+") as file:
        show_type = str(check_for_show_type[0].value) + "\n"
        if not show_type in file.readlines():
            file.write(show_type)

def func_find_all_show_type(show_Json):
    check_for_show_type = []

    parse_possibilities = [
        '$.seriesType',
        '$.moreInformation.category.id'
    ]

    for parse_reg in parse_possibilities:
        check_for_show_type = parse(parse_reg).find(show_Json)
        if len(check_for_show_type) >= 1:
            func_write_to_files(check_for_show_type)
            return (check_for_show_type[0].value)
    else:
        func_write_error_to_log("Could not find show type. Printing JSON to Error file.")
        func_export_JSON_to_file(show_Json, "Show_JSON_Missing_Series_Type.json")
        input("New show check. Check JSON file.")
        return("Error")