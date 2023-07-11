import os
import time

src = input("please enter source directory... ")
rep = input("please enter replica directory... ")
sync_int = int(input("please enter a synchronization interval (in seconds)... "))


def one_way_sync(source_folder: str, replica_folder: str):
    run = True
    i = 0

    while run:
        file_list = []
        # first creates list of files
        for file in os.listdir(source_folder):
            if file:
                file_list.append(os.path.join(source_folder, file))
        print(file_list)

        # run counter
        i += 1

        #  asks if synchronisation should continue every 5 loops
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