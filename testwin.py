import os
import subprocess
import sys
import tempfile

import pyglet

import cuars

# Figure out which directory we're gonna show
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    basedir = sys.argv[1]
else:
    basedir = os.getcwd()
here = os.path.dirname(__file__)

interf = cuars.Interface(200, 150)

start = 0
mark = 0
max = 0
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    global mark
    global max
    if symbol == pyglet.window.key.A:
        mark = mark + 1
    elif symbol == pyglet.window.key.B and mark < max:
        path = nodes[mark]
        num = str(mark)
        real = os.path.realpath(path)
        bytes = os.path.getsize(path)
        info = str(bytes) + " bytes"
        scrip = (".bat", ".cmd", ".sh")
        if os.path.ismount(path):
            print("NODE " + num + ": " + real + " | mount point | " + info)
        elif os.path.islink(path):
            print("NODE " + num + ": " + real + " | symbolic link | " + info)
        elif os.path.isdir(path):
            print("NODE " + num + ": " + real + " | directory | " + info)
        elif os.access(path, os.X_OK):
            print("NODE " + num + ": " + real + " | executable | " + info)
            if os.path.splitext(path)[1] in scrip:
                print("Running script...")
                subprocess.call(path)
                print("Script completed")
        elif os.path.isfile(path):
            print("NODE " + num + ": " + real + " | regular file | " + info)
        else:
            start = (start+1) % max

@window.event
def on_draw():
    global mark
    global max
    nodes = cuars.get_directory(basedir)
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = os.path.join(tmpdirname, "interf.png")
        mark = mark % (max+1)
        max = interf.show_directory(basedir, nodes, mark)
        interf.image.save(filename)
        image = pyglet.image.load(filename)
    window.clear()
    image.anchor_x=image.width//2
    image.anchor_y=image.height//2
    image.blit(window.width//2, window.height//2)

pyglet.app.run()
