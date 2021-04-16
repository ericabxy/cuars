import cuars
from datetime import datetime
import os
import pyglet
import subprocess
import sys

# Figure out which directory we're gonna show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    path = sys.argv[1]
else:
    path = os.getcwd()
here = os.path.dirname(__file__)

interf = cuars.Interface(135, 240)
nodes = interf.list_nodes(path)
mark = len(nodes)
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    global mark
    if symbol == pyglet.window.key.A:
        mark = (mark+1)%(len(nodes)+1)
    if symbol == pyglet.window.key.B:
        run_program(path, mark)

def run_program(path, mark):
    if mark < len(nodes):
        path = os.path.join(path, nodes[mark])
        abspath = os.path.abspath(path)
        if os.path.ismount(path):
            print("NODE " + str(mark) + ": mount point")
        elif os.path.islink(path):
            print("NODE " + str(mark) + ": symbolic link | path: ")
        elif os.path.isfile(path):
            size = os.path.getsize(path)
            exe = os.access(path, os.X_OK) and "executable | " or ""
            print("NODE " + str(mark)
                  + ": regular file | " + exe
                  + str(size) + " bytes")
        elif os.path.isdir(path):
            subnodes = len(os.listdir(path))
            sub = subnodes > 0 and str(subnodes) or "0 (empty)"
            print("NODE " + str(mark) + ": directory | contents: " + sub)
#        elif os.access(path, os.X_OK):
#            print("node " + abspath + " is executable")
#            subprocess.call(path)

@window.event
def on_draw():
    window.clear()
    filename = os.path.join(here, "interf.example.png")
    if path:
        interf.get_directory(path, mark).save(filename)
    image = pyglet.image.load(filename)
    image.anchor_x=image.width//2
    image.anchor_y=image.height//2
    image.blit(window.width//2, window.height//2)

pyglet.app.run()
