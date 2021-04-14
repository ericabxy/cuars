import datetime
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

def main():
    print("Invoked " + sys.argv[0])
    inter = Interface(135, 240)
    if len(sys.argv) > 1:
        print("cuars: creating interface")
        image = inter.get_directory(sys.argv[1])
        isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
        filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
        image.save(filename)
        print("cuars: saved image to " + filename)
    else:
        print("cuars: no directory given")
        print("cuars: try invoking with \"test.dir\" on the command line")

class Interface():
    def __init__(self, width, height):
        execpath = os.path.dirname(sys.argv[0])
        fontpath = os.path.join(execpath, "BebasNeue.otf")
        self.font = ImageFont.truetype(fontpath, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_palette()
        self.width = width
        self.height = height
        self.rotation = 0

    def get_table(self, name, list):
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
        root = root[len(root)-1]
        self.scheme = shades
        return self.get_table(root, nodes)

    def set_palette(self, key=0):
        palettes = {
            "enhanced": ("#222222", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                         "#FFAAAA", "#FFAAFF", "#FFFFAA", "#DDDDDD"),
            "solarized": ("#2D2D2D", "#268BD2", "#859900", "#2AA198",
                          "#DC322F", "#D33682", "#B58900", "#EEE8D5"),
            "quadro-a": ("#222222", "#5555AA", "#55AA55", "#DDDDDD",
                         "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD"),
            "quadro-b": ("#222222", "#55AAAA", "#AA55AA", "#DDDDDD",
                         "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD"),
            "tabman": ("#B03060", "#22AA99", "#22AA99", "#D9D9D9",
                       "#D9D9D9", "#D9D9D9", "#708090", "#D9D9D9")
        }
        if isinstance(key, int):
            for i, k in enumerate(palettes):
                if i == key:
                    self.palette = palettes[k]
                    return k
            return "not found"
        elif key in palettes:
            self.palette = palettes[key]
            return key
        else:
            self.palette = palettes["enhanced-"]
            return "default"
        self.scheme = ((3, 0), (5, 0))


if __name__ == "__main__":
    main()
    sys.exit()
