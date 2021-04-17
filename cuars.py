#!/usr/bin/env python3
'''
Copyright 2021 Eric Duhamel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import datetime
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

def main():
    print("Invoked " + sys.argv[0])
    print("cuars: creating interface")
    inter = Interface(135, 240)
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        path = sys.argv[1]
    else:
        path = os.getcwd()
    print("cuars: displaying table of contents for " + path)
    image = inter.get_directory(path)
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
    image.save(filename)
    print("cuars: saved screenshot to " + filename)

class Interface():
    def __init__(self, width, height):
        basedir = os.path.dirname(__file__)
        path = os.path.join(basedir, "fonts", "BebasNeue.otf")
        self.font = ImageFont.truetype(path, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_frame(os.path.basename(os.getcwd()))
        self.set_palette()
        self.set_scheme((1, 0, 2, 0))
        self.width = width
        self.height = height
        self.rotation = 0

    def get_directory(self, dirname, mark=None):
        self.name = os.path.split(dirname)[1]
        nodes = self.list_nodes(dirname)
        shades = []
        for node in nodes:
            path = os.path.join(dirname, node)
            if os.path.islink(path):
                shades.append(3)
                shades.append(0)
            elif os.path.ismount(path):
                shades.append(4)
                shades.append(0)
            elif os.path.isdir(path):
                shades.append(1)
                shades.append(0)
            elif os.access(path, os.X_OK):
                shades.append(2)
                shades.append(0)
            elif os.path.isfile(path):
                shades.append(7)
                shades.append(0)
        self.set_scheme(shades)
        return self.get_table(nodes, mark)

    def get_table(self, nodes, mark=None):
        left, top, right, bottom = 0, 0, self.width, self.height
        pal = self.palette
        name, bdcol = self.name, pal[self.bdcolor]
        bgcol, fgcol = pal[self.bgcolor], pal[self.fgcolor]
        rect = (left, top, right, bottom)  # draw the frame and title
        self.draw.rectangle(rect, outline=bdcol, fill=bdcol)
        self.draw.text((left+5, top), name.upper(), font=self.font, fill=fgcol)
        text = "nodes " + str(len(nodes))  # draw the # of nodes
        self.draw.text((right-75, top), text, font=self.font, fill=fgcol)
        rect = (left+2, top+22, right, bottom)  # draw the table background
        self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
        y = 25
        shades = self.scheme
        for i in range(len(nodes)):
            c = (i%len(shades))
            bgcol = pal[shades[c][0]]
            fgcol = pal[shades[c][1]]
            rect = (left+5, y, left+105, y+23)
            self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
            text = nodes[i].upper()
            self.draw.text((left+5, y), text, font=self.font, fill=fgcol)
            if i == mark:
                rect = (left+97, y, left+100, y+23)
                self.draw.rectangle(rect, outline=fgcol, fill=fgcol)
            y += 28
            if y > bottom:
                y = 25
                left = left + 105
        return self.image

    def list_nodes(self, path):
        nodes = os.listdir(path)
        for node in nodes:
            if node[0] == ".":
                nodes.remove(node)
        nodes.sort()
        return nodes

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
