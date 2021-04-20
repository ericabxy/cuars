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
nodes = []
for name in os.listdir(basedir):
    nodes.append(os.path.join(basedir, name))
nodes.sort()
mark = len(nodes)
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    global mark
    if symbol == pyglet.window.key.A:
        mark = (mark+1)%(len(nodes)+1)
    elif symbol == pyglet.window.key.B and mark < len(nodes):
        path = os.path.join(basedir, nodes[mark])
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

@window.event
def on_draw():
    global mark
    window.clear()
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = os.path.join(tmpdirname, "interf.png")
        max = interf.draw_directory(nodes, mark)
        interf.image.save(filename)
        image = pyglet.image.load(filename)
    image.anchor_x=image.width//2
    image.anchor_y=image.height//2
    image.blit(window.width//2, window.height//2)

pyglet.app.run()
