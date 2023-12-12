import os
import datetime


class colors:
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'


def sendError(header, raw_message, level=1):
    # Header ,Message , Level : 0 warning, 1 error, 2 error with exiting(NOT IN USE)
    time_format = datetime.datetime.now().strftime("%H:%M:%S")
    msg = f"[{datetime.date.today()} {time_format}] {header} : {raw_message}\n"

    if level in [1, 2]:
        curr_color = colors.ERROR
    else:
        curr_color = colors.WARNING

    print(f'{curr_color}{header}{colors.ENDC}')

    try:
        log_file = open("./log.txt", "a")
        log_file.write(msg)
        log_file.close()
    except _:
        print("Error in error.py: Cannot write to file!")
