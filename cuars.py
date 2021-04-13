import os
import sys
from PIL import Image, ImageDraw, ImageFont

def main():
    fontpath = os.path.join(os.path.dirname(sys.argv[0]), "ascii.ttf")
    inter = Interface(135, 240, fontpath)
    image = inter.get_buttons("command",
        ("arg a", "arg b", "arg c", "arg d", "arg e", "arg f", "arg e"),
        2)
    image.show()
    if len(sys.argv) > 1:
        image = inter.get_tree(sys.argv[1])

class Interface():
    def __init__(self, width, height, fontpath):
        self.font = ImageFont.truetype(fontpath, 24)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_palettes()
        self.width = width
        self.height = height
        self.rotation = 0

    def get_buttons(self, name, list, sel=0):
        left, top, right, bottom = 0, 0, self.width, self.height
        pal = self.pal10
        bgcol, fgcol = pal[0], pal[3]
        rect = (left, top, right, bottom)
        self.draw.rectangle(rect, outline=0, fill=bgcol)
        self.draw.text((left+5, top+5), name.upper(), font=self.font, fill=fgcol)
        y = 30
        for i in range(len(list)):
            col = (i%2)+1
            bgcol, fgcol = pal[col], pal[0]
            rect = (left+5, y, right-5, y+25)
            self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
            text = list[i].upper()
            self.draw.text((left+5, y), text, font=self.font, fill=fgcol)
            y += 30
        return self.image

    def get_tree(self, abspath):
        for root, dirs, files in os.walk(abspath):
            break
        nodes = dirs + files
        nodes.sort()
        root = os.path.basename(abspath)
        return self.get_buttons(root, nodes)

    def set_palettes(self):
        self.pal10 = ("#000000", "#55AAAA", "#AA55AA", "#AAAAAA")  # EGA CM
        self.pal11 = ("#555555", "#AAFFFF", "#FFAAFF", "#FFFFFF")  # EGA CM
        self.pal12 = ("#2D2D2D", "#2AA198", "#D33682", "#EEE8D5")  # solarized
        self.pal20 = ("#000000", "#5555FF", "#55FF55", "#AAAAAA")  # EGA BG
        self.pal21 = ("#2D2D2D", "#859900", "#268BD2", "#EEE8D5")  # solarized


if __name__ == "__main__":
    main()
    sys.exit()
