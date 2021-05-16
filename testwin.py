import os
import subprocess
import sys
import tempfile

import tkinter as tk

import cuars

# Figure out which directory we're gonna show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    basedir = sys.argv[1]
else:
    basedir = os.getcwd()
here = os.path.dirname(__file__)

interf = cuars.Interface(200, 150)

window = tk.Tk()
canvas = tk.Canvas(window)
btn_a = tk.Button(window, text="A")
btn_b = tk.Button(window, text="B")
canvas.pack()
btn_a.pack(side=tk.LEFT)
btn_b.pack(side=tk.LEFT)

list = cuars.get_files(basedir, ".py")
interf.show_text(list)
interfimage = interf.image
image = tk.PhotoImage(file="test.dir/image.png")
image = interf.get_tkimage()
canvas.create_image((0, 0), anchor=tk.NW, image=image)

window.mainloop()
