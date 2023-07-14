import os
import time
import shutil
from datetime import datetime

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

    # creates replica directory and copies all files to replica folder
    if not os.path.exists(replica_folder):
        print('Replica folder has been created.')
        shutil.copytree(source_folder, replica_folder)
    else:
        print('Replica folder already exists.')
        for file in os.listdir(source_folder):
            source_file = os.path.join(source_folder, file)
            replica_file = os.path.join(replica_folder, file)
            shutil.copy2(source_file, replica_file)

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
        try:
            # if nothing changed, prints "no changes found"
            if reference_file_list == temp_file_list:
                current_time = datetime.now().time()
                print(f"No changes found at {current_time}.")
                with open(log, 'a') as text:
                    text.write(f"There were no changes at {current_time}. \n")
            else:
                # looks for deletions from previous run
                for file in reference_file_list:
                    if file not in temp_file_list:
                        current_time = datetime.now().time()
                        file_folder = file.rsplit('\\', 1)[-1]
                        rep_file = replica_folder + '\\' + file_folder
                        os.remove(rep_file)
                        print(f'The file: {file} has been removed at {current_time}.')
                        with open(log, 'a') as text:
                            text.write(f"The file: {file} has been removed at {current_time}.\n")
                        reference_file_list.remove(file)

                # looks for additions from previous run
                for file in temp_file_list:
                    if file not in reference_file_list:
                        current_time = datetime.now().time()
                        shutil.copy(file, replica_folder)
                        print(f'The file: {file} has been added at {current_time}.')
                        with open(log, 'a') as text:
                            text.write(f'The file: {file} has been added at {current_time}.\n')
                        reference_file_list.append(file)

        except FileNotFoundError:
            # catches FileNotFoundError if a change occurs during a synchronisation run
            # which will be rectified in the next run
            continue

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
                print("The program will nopw terminate, thank you!")
            else:
                run = True
                print("Invalid response, please type only y or n, cycle will repeat.")


one_way_sync(src, rep, log_name, sync_int)
