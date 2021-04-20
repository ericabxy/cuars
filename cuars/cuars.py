#!/usr/bin/env python3
"""Copyright 2021 Eric Duhamel

This file is part of CUARS.

CUARS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CUARS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CUARS.  If not, see <https://www.gnu.org/licenses/>.
"""
import datetime
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

def main():
    print("Invoked " + sys.argv[0])
    print("cuars: creating interface")
    inter = Interface(160, 120)
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        path = sys.argv[1]
    else:
        path = os.getcwd()
    print("cuars: displaying table of contents for " + path)
    inter.draw_directory(path)
    image = inter.image
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
    image.save(filename)
    print("cuars: saved screenshot to " + filename)

class Interface():
    def __init__(self, width, height):
        basedir = os.path.dirname(__file__)
        path = os.path.join(basedir, "fonts", "BebasNeue.otf")
        self.font = ImageFont.truetype(path, 22)
        path = os.path.join(basedir, "fonts", "ASCII.ttf")
        self.icon = ImageFont.truetype(path, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.set_frame(os.path.basename(os.getcwd()))
        self.set_palette()
        self.set_scheme((1, 0, 2, 0))
        self.width = width
        self.height = height
        self.node_w = 100
        self.node_h = 25
        self.node_p = 5
        self.rotation = 0

    def draw_directory(self, dirname, mark=None):
        """List directory contents in a table

        Sets scheme to color-code each file according to the palette.
        Directories are blue. Executables are green. Symbolic links are
        cyan. Mount points are red.
        """
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
        return self.draw_table(nodes, mark)

    def draw_table(self, nodes, mark=None, start=0):
        length = len(nodes)
        left, top, right, bottom = 0, 0, self.width, self.height
        pal = self.palette
        name, bdcol = self.name, pal[self.bdcolor]
        bgcol, fgcol = pal[self.bgcolor], pal[self.fgcolor]
        rect = (left, top, right, bottom)  # draw the frame and title
        self.draw.rectangle(rect, outline=bdcol, fill=bdcol)
        text = name.upper()  # + "     " + str(length) + " nodes"
        self.draw.text((left+5, top), text, font=self.font, fill=fgcol)
        rect = (left+2, top+22, right, bottom)  # draw the table background
        self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
        shades = self.scheme
        i, x, y, w, h = start, left+5, 25, self.node_w, self.node_h
        while i < length and x < self.width:
            c = (i%len(shades))
            bgcol = pal[shades[c][0]]
            fgcol = pal[shades[c][1]]
            rect = (x, y, x+w, y+h)
            self.draw.rectangle(rect, outline=bgcol, fill=bgcol)
            text = nodes[i].upper()
            if i == mark:
#                rect = (x+92, y, x+95, y+23)
                rect = (x+5, y, x+8, y+h)
                self.draw.rectangle(rect, outline=fgcol, fill=fgcol)
                self.draw.text((x+10, y), text, font=self.font, fill=fgcol)
            else:
                self.draw.text((x, y), text, font=self.font, fill=fgcol)
            i, y = i+1, y+h+self.node_p
            if y+h > bottom:
                x, y = x+w+self.node_p, 25
        if i < length: # show paging arrows
            z = len(str(length))
            text = str(i).zfill(z)
            x = self.width - self.font.getsize(text)[0] - 1
            self.draw.rectangle((x-5, top, x-2, top+22), outline=fgcol, fill=fgcol)
            self.draw.text((x, top), text, font=self.font, fill=fgcol)
            text = str(start).zfill(z)
            x = x - 3 - self.font.getsize(text)[0] - 3
            self.draw.rectangle((x-5, top, x-2, top+22), outline=fgcol, fill=fgcol)
            self.draw.text((x, top), text, font=self.font, fill=fgcol)
        else: # show the number of nodes
            text = str(length) + " nodes"
            x = self.width - 5 - self.font.getsize(text)[0]
            self.draw.text((x, top), text, font=self.font, fill=fgcol)
        return i

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
