import datetime
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

def main():
    print("Invoked " + sys.argv[0])
    inter = Interface(135, 240)
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
    if len(sys.argv) > 1:
        print("cuars: creating interface")
        if os.path.isdir(sys.argv[1]):
            image = inter.get_directory(sys.argv[1])
        else:
            if len(sys.argv) > 2:
                shades = sys.argv[2].split(",")
                scheme = []
                for s in shades:
                    scheme.append(int(s))
                inter.set_scheme(scheme)
            image = inter.get_table(sys.argv[1].split(","))
        image.save(filename)
        print("cuars: saved image to " + filename)
    else:
        print("cuars: no directory given")
        print("cuars: try invoking with \"test.dir\" on the command line")
        print("cuars: saving an test image to " + filename)
        image = inter.get_table(("node 1", "node 2", "node 3", "node 4",
                                 "node 5",))
        image.save(filename)

class Interface():
    def __init__(self, width, height):
        modpath = os.path.dirname(__file__)
        fontpath = os.path.join(modpath, "BebasNeue.otf")
        self.font = ImageFont.truetype(fontpath, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_frame(os.path.basename(os.getcwd()))
        self.set_palette()
        self.set_scheme((1, 0, 2, 0))
        self.width = width
        self.height = height
        self.rotation = 0

    def get_directory(self, path):
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
            elif os.access(os.path.join(path, node), os.X_OK):
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
        self.name = root[len(root)-1]
        self.scheme = shades
        return self.get_table(nodes)

    def get_table(self, list):
        left, top, right, bottom = 0, 0, self.width, self.height
        pal = self.palette
        name, bdcol = self.name, pal[self.bdcolor]
        bgcol, fgcol = pal[self.bgcolor], pal[self.fgcolor]
        rect = (left, top, right, bottom)  # draw the frame and title
        self.draw.rectangle(rect, outline=bdcol, fill=bdcol)
        self.draw.text((left+5, top), name.upper(), font=self.font, fill=fgcol)
        rect = (left+2, top+22, right, bottom)  # draw the table background
        self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
        y = 25
        shades = self.scheme
        for i in range(len(list)):
            c = (i%len(shades))
            bgcol = pal[shades[c][0]]
            fgcol = pal[shades[c][1]]
            rect = (left+5, y, left+120, y+23)
            self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
            text = list[i].upper()
            self.draw.text((left+5, y), text, font=self.font, fill=fgcol)
            y += 28
        return self.image

    def set_frame(self, name, shad=(0, 0, 6)):
        self.name = name
        self.bgcolor = shad[0]
        self.fgcolor = shad[1]
        self.bdcolor = shad[2]

    def set_palette(self, key=0):
        if key in ("solarized", 1):
            self.palette = ("#2D2D2D", "#268BD2", "#859900", "#2AA198",
                            "#DC322F", "#D33682", "#B58900", "#EEE8D5")
        elif key in ("quadro-a", 2):
            self.palette = ("#222222", "#5555AA", "#55AA55", "#DDDDDD",
                            "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD")
        elif key in ("quadro-b", 3):
            self.palette = ("#222222", "#55AAAA", "#AA55AA", "#DDDDDD",
                            "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD")
        elif key in ("tabman-a", 4):
            self.palette = ("#B03060", "#22AA99", "#22AA99", "#D9D9D9",
                            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
        elif key in ("tabman-b", 5):
            self.palette = ("#708090", "#22AA99", "#B03060", "#D9D9D9",
                            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
        else:  # default palette 0, "enhanced-"
            self.palette = ("#222222", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                            "#FFAAAA", "#FFAAFF", "#FFFFAA", "#DDDDDD")

    def set_scheme(self, seq):
        scheme = []
        for i in range(0, len(seq)-1, 2):
            scheme.append((seq[i], seq[i+1]))
        self.scheme = scheme


if __name__ == "__main__":
    main()
    sys.exit()
