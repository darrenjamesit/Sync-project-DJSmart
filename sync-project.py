import os
import time

src = input("please enter source directory...")
rep = input("please enter replica directory...")
sync_int = int(input("please enter a synchronization interval (in seconds)..."))

def one_way_sync(src, rep):
    run = True
    while run:
        print(src)
        print(rep)
        break

