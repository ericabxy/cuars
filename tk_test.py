"""
A basic demonstration of CUARS using Tkinter to show the display on a
canvas. Emulates a two-button interface (TODO: also a button to take
screenshots of the display). Python modules 'os' and 'sys' are used to
perform basic navigation and operations. Note that much of this basic
functionality should eventually be moved to CUARS submodules.
"""
import os
import sys
import time

import tkinter as tk

import cuars

"""
TODO: depending on whether a directory, a text file, or an image file
is supplied as a command-line argument, set up the correct display
TODO: option to show login information
TODO: option to show system information
TODO: this is really messy, too many globals and confusion
TODO: allow "index" to value "None" until "A" pressed
TODO: "Table.newwindow" pager rect must fill area
Paths and files are named after os.path functions
"""

# print some login information
print("Login: " + os.getlogin())
print("Current Working Directory: " + os.getcwd())
print("Process ID: " + os.getpid())
print("Times: ", os.times())

# initialize directory navigation variables
index = 0
dirname = os.path.expanduser("~")
dirlist = os.listdir(dirname)
print("User: " + os.getlogin())
print("Directory: " + dirname)

# initialize the display object
interf = cuars.Table(250, 150)

# callbacks for tkinter widgets
def do_button1():  # advance file index by 1 and loop
    global dirlist, dirname, index
    index = (index+1)%(len(dirlist)+1)
    print(dirname, dirlist[index])
    show_table(dirname, dirlist, index)

def do_button2():
    global dirlist, dirname, index
    print(dirname, dirlist[index])
    name = dirlist[index]
    path = os.path.join(dirname, name)
    if os.path.isdir(path):
        dirname, index = path, 0
        dirlist = os.listdir(dirname)
        show_table(dirname, dirlist, index)

def do_button1and2(path="~"):
    global dirlist, dirname, index
    index = 0
    dirname = os.path.expanduser(path)
    dirlist = os.listdir(dirname)
    show_table(dirname, dirlist, index)

def do_expand():
    pass

def do_screenshot():
    pass

# setup a basic Tkinter window
root = tk.Tk()
root.title("CUARS")
canvas = tk.Canvas(root)
btn_a = tk.Button(root, text="A", command=do_button1)
btn_b = tk.Button(root, text="B", command=do_button2)
btn_s = tk.Button(root, text="screenshot", command=do_screenshot)
btn_ab = tk.Button(root, text="A+B", command=do_button1and2)
btn_a.pack(side=tk.TOP)
btn_b.pack(side=tk.TOP)
btn_ab.pack(side=tk.TOP)
btn_s.pack(side=tk.BOTTOM)
canvas.pack()

def colorize(root, files, tags={}):
    """Return a color-coded list from a list of files

    Optional 'tags' dictionary codes list based on extensions"""
    colors = []
    for name in files:
        path = os.path.join(root, name)
        if os.path.islink(path): colors.append(3)
        elif os.path.ismount(path): colors.append(4)
        elif os.path.isdir(path): colors.append(1)
        elif os.access(path, os.X_OK): colors.append(2)
        elif os.path.splitext(path)[1] in tags:
            colors.append(tags[os.path.splitext(path)[1]])
        else: colors.append(7)
    return colors

def show_table(root, list, mark):
    global image
    interf.name = os.path.split(dirname)[1]
    interf.set_pager(mark+1, len(list))
    s = interf.slice(list, mark)
#    interf.set_pattern(colorize(root, list))
    interf.set_list(list[s:], colorize(root, list[s:]))
    interf.mark = mark-s
    interf.render()
    image = interf.get_tkimage()
    canvas.create_image((0, 0), anchor=tk.NW, image=image)

def fileinfo(path):
    info = os.stat(path)
    dir = os.path.dirname(path)
    list = os.path.listdir(dir)
    print("")
    print("Dirname: " + os.path.dirname(path))
    print("File " + str(index+1) + " of " + len(list))
    print("Filename: " + os.path.basename(path))
    print("Realpath: " + os.path.realpath(path))
    print("Mode: " + str(info.st_mode))
    print("Links: " + str(info.st_nlink))
    print("User: " + str(info.st_uid))
    print("Group: " + str(info.st_gid))
    print("Size: " + str(info.st_size))
    print("Accessed: " + time.ctime(info.st_atime))
    print("Modified: " + time.ctime(info.st_mtime))
    print("Working: " + os.getcwd())

fileinfo(dirname)

show_table(dirname, dirlist, index)

# startup the TK interface
root.mainloop()
