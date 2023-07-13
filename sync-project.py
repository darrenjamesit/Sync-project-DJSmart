import os
import time
from pathlib import Path

src = input("please enter source directory... ")
rep = input("please enter replica directory... ")
sync_int = int(input("please enter a synchronization interval (in seconds)... "))
log_path = input('please choose the directory for the log file... ')
log_name = log_path + '\\log.txt'


def one_way_sync(source_folder: str, replica_folder: str, log: str, interval: int):
    # create a blank text file to act as log
    with open(log, 'w') as text:
        text.write("***Log of All Changes***\n")
        line = '-'
        text.write(f'{line * 24}\n')

    # make the replica directory (catches error if directory already exists
    rep_path = Path(replica_folder)
    try:
        rep_path.mkdir()
        print("Replica directory has been created...")
    except FileExistsError:
        print("Replica directory already exists...")

    run = True
    i = 0

    # first creates list of file paths
    file_list = []
    for root, dirs, files in os.walk(source_folder):
        if files:
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                if os.path.isfile(file_path):
                    file_list.append(file_path)

    while run:
        # looks for deletions from previous run
        for filename in file_list:
            pass

        # run counter
        i += 1

        time.sleep(interval)

        # asks if synchronisation should continue every 5 loops
        if i == 5:
            run_query = input("would you like to continue? y / n... ")
            if run_query == 'y':
                run = True
                i = 0
            elif run_query == 'n':
                run = False
            else:
                run = True
                print("Invalid response, please type only y or n, cycle will repeat.")


one_way_sync(src, rep, log_name, sync_int)
