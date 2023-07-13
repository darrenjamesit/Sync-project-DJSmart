import os
import time
from pathlib import Path
import shutil

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

    # make the replica directory (catches error if directory already exists)
    rep_path = Path(replica_folder)
    try:
        rep_path.mkdir()
        print("Replica directory has been created...")
    except FileExistsError:
        print("Replica directory already exists...")
    finally:
        # copies all files to replica folder
        shutil.copytree(source_folder, replica_folder)

    # first creates a reference list of file paths to determine if changes have occurred
    reference_file_list = []
    for root, dirs, files in os.walk(source_folder):
        if files:
            for file in files:
                ref_file_path = os.path.join(root, file)
                print(ref_file_path)
                if os.path.isfile(ref_file_path):
                    reference_file_list.append(ref_file_path)

    run = True
    i = 0

    while run:
        # first makes a new list to compare to reference list (anything
        temp_file_list = []
        for root, dirs, files in os.walk(source_folder):
            if files:
                for file in files:
                    temp_file_path = os.path.join(root, file)
                    if os.path.isfile(temp_file_path):
                        temp_file_list.append(temp_file_path)

        # looks for deletions from previous run
        for file in reference_file_list:
            if file not in temp_file_list:
                rep_file = file.replace('\\source', '\\replica')
                os.remove(rep_file)
                print(f'The file: {file} has been removed.')
                with open(log, 'a') as text:
                    text.write(f'The file: {file} has been removed.')
                reference_file_list.remove(file)

        # looks for additions from previous run
        for file in temp_file_list:
            if file not in reference_file_list:
                rep_file = file.replace('\\source', '\\replica')
                os.remove(rep_file)
                print(f'The file: {file} has been added.')
                with open(log, 'a') as text:
                    text.write(f'The file: {file} has been added.')
                reference_file_list.append(file)

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
