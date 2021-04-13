import datetime
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

def main():
    print("Invoked: " + sys.argv[0])
    print("cuars: creating interface")
    inter = Interface(135, 240)
    if len(sys.argv) > 1:
        image = inter.get_tree(sys.argv[1])
    else:
        image = inter.get_buttons("command",
            ("arg a", "arg b", "arg c", "arg d", "arg e", "arg f", "arg e"))
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
    image.save(filename)
    print("cuars: saved image to " + filename)

class Interface():
    def __init__(self, width, height):
        execpath = os.path.dirname(sys.argv[0])
        fontpath = os.path.join(execpath, "BebasNeue.otf")
        self.font = ImageFont.truetype(fontpath, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_palettes()
        self.width = width
        self.height = height
        self.rotation = 0

    def get_buttons(self, name, list):
        left, top, right, bottom = 0, 0, self.width, self.height
        pal = self.palette
        bgcol, fgcol = pal[0], pal[7]
        rect = (left, top, right, bottom)
        self.draw.rectangle(rect, outline=0, fill=bgcol)
        self.draw.text((left+5, top+5), name.upper(), font=self.font, fill=fgcol)
        y = 30
        shades = self.scheme
        for i in range(len(list)):
            c = (i%len(shades))
            bgcol = pal[shades[c][0]]
            fgcol = pal[shades[c][1]]
            rect = (left+5, y, right-5, y+25)
            self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
            text = list[i].upper()
            self.draw.text((left+5, y), text, font=self.font, fill=fgcol)
            y += 30
        return self.image

    def get_tree(self, path):
        path = os.path.abspath(path)
        nodes = os.listdir(path)
        nodes.sort()
        shades = []
        for node in reversed(nodes):
            splitted = node.split(".")
            ext = splitted[len(splitted)-1]
            if node[0] == ".":
                nodes.remove(node)
            elif os.path.isdir(os.path.join(path, node)):
                shades.insert(0, (1, 0))
            elif ext in ("bin", "exe"):
                shades.insert(0, (2, 0))
            elif ext in ("oga", "ogg"):
                shades.insert(0, (3, 0))
            elif ext in ("tar", "zip"):
                shades.insert(0, (4, 0))
            elif ext in ("jpg", "png", "svg"):
                shades.insert(0, (5, 0))
            else:
                shades.insert(0, (7, 0))
        root = os.path.split(path)
        root = root[len(root)-1]
        self.palette = self.pal22
        self.scheme = shades
        return self.get_buttons(root, nodes)

    def set_palettes(self):
        self.pal20 = ("#111111", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                      "#FFAAAA", "#FFAAFF", "#FFFFAA", "#AAAAAA")  # extended-
        self.pal21 = ("#555555", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                      "#FFAAAA", "#FFAAFF", "#FFFFAA", "#FFFFFF")  # extended+
        self.pal22 = ("#2D2D2D", "#268BD2", "#859900", "#2AA198",
                      "#DC322F", "#D33682", "#B58900", "#EEE8D5")  # solarized
        self.palette = self.pal21
        self.scheme = ((1, 0), (2, 0))


if __name__ == "__main__":
    main()
    sys.exit()
