import os
import sys

import tkinter as tk

import cuars

# Determine which directory to show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    dirname = sys.argv[1]
else:
    dirname = os.getcwd()

interf = cuars.Interface(300, 200)
mark = -1

window = tk.Tk()
window.title("CUARS")
canvas = tk.Canvas(window)
canvas.pack()
def refresh():
    global image, mark
    list, shades = cuars.get_directory(dirname)
    mark = (mark+1)%len(list)
    interf.name = os.path.basename(dirname)
    image = interf.get_table(list, mark)
    canvas.create_image((0, 0), anchor=tk.NW, image=image)
refresh()

btn_a = tk.Button(window, text="A", command=refresh)
btn_b = tk.Button(window, text="B", command=refresh)
btn_a.pack(side=tk.LEFT)
btn_b.pack(side=tk.LEFT)

window.mainloop()
