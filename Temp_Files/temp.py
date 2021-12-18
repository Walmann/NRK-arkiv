
log_list = []

with open("Error.log", "r") as log:
    for item in log:
        log_list.append(item)
    log_list = list( dict.fromkeys(log_list))

with open("Error_sorted.log", "w") as log:
    for item in log_list:
        log.write(item)