import math
import os
import sys

import tkinter as tk

import cuars

# Determine which directory to show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    dirname = sys.argv[1]
else:
    dirname = os.getcwd()

interf = cuars.Interface(320, 200)
mark, page = -1, 0

window = tk.Tk()
window.title("CUARS")
canvas = tk.Canvas(window)
canvas.pack()

def show_badges(list, shades):
    global image
    interf.name = os.path.basename(dirname)
    image = interf.get_table(list, shades)
    canvas.create_image((0, 0), anchor=tk.NW, image=image)

def button1():
    global mark, page
    list, shades = cuars.get_directory(dirname)
    mark = (mark+1)%len(list)
    interf.set_pager(mark, len(list))
    list, mark2 = interf.crop_list(list, mark)
    interf.mark = mark2
    pagelen = interf.pagelen()
    pages = math.ceil(len(list)/pagelen)
    page = (page+1)%pages
    show_badges(list, shades)

button1()
btn_a = tk.Button(window, text="A", command=button1)
btn_b = tk.Button(window, text="B", command=button1)
btn_a.pack(side=tk.LEFT)
btn_b.pack(side=tk.LEFT)

window.mainloop()
