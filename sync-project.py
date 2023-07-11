import os
import time

src = input("please enter source directory... ")
rep = input("please enter replica directory... ")
sync_int = int(input("please enter a synchronization interval (in seconds)... "))
log_path = input('please choose the directory for the log file... ')
log_name = log_path + 'log.txt'


def one_way_sync(source_folder: str, replica_folder: str):
    # create a blank text file to act as log
    with open(log_name, 'w') as text:
        text.write("***Log of All Changes***\n")
        line = '-'
        text.write(f'{line * 24}\n')

    run = True
    i = 0

    while run:
        # first creates list of file paths
        file_list = []
        current_time = time.time()
        for root, dirs, files in os.walk(source_folder):
            if files:
                for file in files:
                    file_path = root + file
                    if os.path.isfile(file_path):
                        file_list.append(file_path)

        # checking if files were modified since last sync
        for file in file_list:
            mod_time = os.path.getmtime(file)
            difference_in_times = current_time - mod_time
            if difference_in_times < sync_int:
                pass

        # run counter
        i += 1

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
                print("Invalid response, please type only y or n, cycle will continue.")


one_way_sync(src, rep)