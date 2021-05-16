import os
import subprocess
import sys
import tempfile

import tkinter as tk

import cuars

# Figure out which directory we're gonna show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    dirname = sys.argv[1]
else:
    dirname = os.getcwd()

interf = cuars.Interface(200, 150)
mark = 0

window = tk.Tk()
canvas = tk.Canvas(window)
canvas.pack()
def refresh():
    global image, mark
    list, shades = cuars.get_directory(dirname)
    mark = (mark+1)%len(list)
    interf.name = os.path.basename(dirname)
    interf.show_badges(list, (0, 0), shades, mark)
    image = interf.get_tkimage()
    canvas.create_image((0, 0), anchor=tk.NW, image=image)
refresh()

btn_a = tk.Button(window, text="A", command=refresh)
btn_b = tk.Button(window, text="B", command=refresh)
btn_a.pack(side=tk.LEFT)
btn_b.pack(side=tk.LEFT)

window.mainloop()
