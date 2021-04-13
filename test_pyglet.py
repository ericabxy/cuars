import os
import pyglet
import sys
import cuars

from pyglet.image.codecs.pil import PILImageDecoder

fontpath = os.path.join(os.path.dirname(sys.argv[0]), "BebasNeue.otf")
interf = cuars.Interface(135, 240, fontpath, 22)  # TODO: fix font nonsense

window = pyglet.window.Window()
image = interf.get_tree(os.getcwd())
image.save("image.png")
image = pyglet.image.load("image.png")

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
