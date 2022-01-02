import math
import os
import sys
import time

import tkinter as tk

import cuars

"""
TODO: depending on whether a directory, a text file, or an image file
is supplied as a command-line argument, set up the correct display
"""

def colorize(root, files, tags={}):
    colors = []
    for name in files:
        path = os.path.join(dirname, name)
        if os.path.islink(path): colors.append(3)
        elif os.path.ismount(path): colors.append(4)
        elif os.path.isdir(path): colors.append(1)
        elif os.access(path, os.X_OK): colors.append(2)
        elif os.path.splitext(path)[1] in tags:
            colors.append(tags[os.path.splitext(path)[1]])
        else: colors.append(7)
    return colors

def show_table(list):
    global dirlist, image, index
    interf.name = os.path.basename(dirname)
    interf.set_pager(index+1, len(dirlist))
    list, mark = interf.crop_list(list, index)
    interf.set_pattern(colorize(dirname, list))
    interf.mark = mark
    image = interf.get_render(list)
    canvas.create_image((0, 0), anchor=tk.NW, image=image)

def button1():
    global index
    list = os.listdir(dirname)
    shades = colorize(dirname, list)
    index = (index+1)%len(list)
    show_table(list)

def button2():
    name = dirlist[index]
    path = os.path.join(dirname, name)
    info = os.stat(path)
    print("")
    print("Dirname: " + os.path.dirname(path))
    print(str(index+1) + " of N " + " Filename: " + os.path.basename(path))
    print("Realpath: " + os.path.realpath(path))
    print("Mode: " + str(info.st_mode))
    print("Links: " + str(info.st_nlink))
    print("User: " + str(info.st_uid))
    print("Group: " + str(info.st_gid))
    print("Size: " + str(info.st_size))
    print("Accessed: " + time.ctime(info.st_atime))
    print("Modified: " + time.ctime(info.st_mtime))
#    print("Created: " + time.ctime(info.st_ctime))
    print("Working: " + os.getcwd())

def screenshot():
    pass

# setup a basic Tkinter window
root = tk.Tk()
root.title("CUARS")
canvas = tk.Canvas(root)
btn_a = tk.Button(root, text="A", command=button1)
btn_b = tk.Button(root, text="B", command=button2)
btn_s = tk.Button(root, text="SHOT", command=screenshot)
btn_a.pack(side=tk.LEFT)
btn_b.pack(side=tk.LEFT)
btn_s.pack(side=tk.LEFT)
canvas.pack()

# Determine which directory to show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]): dirname = sys.argv[1]
else: dirname = os.getcwd()

interf = cuars.Table(250, 150)
dirlist = os.listdir(dirname)
index = 0

show_table(dirlist)

# startup the TK interface
root.mainloop()
