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
import math
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageTk

# TODO: split "Interface" into distinct types
# This will be called "Table" or "BadgeTable"
class Interface():
    def __init__(self, width, height):
        """Create a display area from specified dimensions

        This area will have a frame itentifying its utility and space
        for displaying each command as a badge.
        """
        basedir = os.path.dirname(__file__)
        path = os.path.join(basedir, "fonts", "BebasNeue.otf")
        self.font = ImageFont.truetype(path, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.name = "CUARS"
        self.pager = "000"
        self.mark = None
        self.set_palette()
        self.set_colors()
        self.width = width
        self.height = height
        self.bw, self.bh = 100, 25
        self.badge = {"width": 100, "height": 25}
        self.border = {"width": 2, "height": 22}
        self.padding = 5

    def crop_list(self, list, mark):
        page_height = self.height-self.bh  # height of badge area
        badge_height = self.badge["height"]+self.padding  # height of badge
        page = math.ceil(page_height/badge_height)  # badges per page
        while mark >= page:
            for i in range(page):
                list.pop(0)
                mark = mark - 1
        return list, mark

    def get_table(self, list, scheme=(1, 2)):
        """Render a display with a grid of interactive buttons

        Work-in-progress: still determining scope and brevity.
        Paging: make a dumb method that displays the whole list?
        Mark: can only "mark" a badge on the left side?
        """
        left, top, right, bottom = 0, 0, self.width, self.height
        display, draw = self.new_window()
        # draw badges
        x, y = self.padding, self.bh
        rects = []
        for i, text in enumerate(list):
            color = self.palette[scheme[i%len(scheme)]]
            rect = (x, y, x+self.badge["width"], y+self.badge["height"])
            draw.rounded_rectangle(rect, outline=color, fill=color, radius=1)
            draw.text((x, y), text, font=self.font, fill=self.color[0])
            rects.append(rect)  # dimensions for touchscreen
            y = y + self.bh + self.padding
            if y > bottom:
                x, y = x + self.badge["width"] + self.padding, self.badge["height"]
        return ImageTk.PhotoImage(display)

    def new_window(self):
        left, top, right, bottom = 0, 0, self.width, self.height
        window = Image.new("RGB", (right, bottom))
        draw = ImageDraw.Draw(window)
        # border (minimal to allow room for badges)
        draw.rounded_rectangle((left, top, right, bottom), radius=1,
          outline=self.color[3], fill=self.color[3])
        draw.rounded_rectangle((left+2, top+22, right, bottom), radius=1,
          outline=self.color[0], fill=self.color[0])
        # title (upper-left)
        draw.text((left+5, top), self.name, font=self.font,
          fill=self.palette[0])
        # pager (upper-right)
        x = self.width - self.font.getsize(self.pager)[0]
        draw.rectangle((x-3, 0, x-1, 22),
          outline=self.color[0], fill=self.color[0])
        draw.text((x, 0), self.pager, font=self.font, fill=self.color[0])
        # mark (indicator along left border)
        if isinstance(self.mark, int):
            badge_height = self.badge["height"]+self.padding
            y = 25+(self.mark*badge_height)
            draw.rectangle((0, y, 5, y+self.badge["height"]),
              outline=self.color[3], fill=self.color[3])
        return window, draw

    def pagelen(self):
        page_height = self.height-self.bh
        badge_height = self.badge["height"]+self.padding
        page_badges = math.ceil(page_height/badge_height)
        return page_badges

    def set_colors(self, a=0, b=2, c=4, d=6):
        """Define a four-color subset of the overall palette"""
        self.color = (self.palette[a], self.palette[b], self.palette[c],
          self.palette[d])

    def set_font(self, path, size):
        if os.path.exists(path): self.font = ImageFont.truetype(path, size)

    def set_pager(self, number, total):
        """Paging numbers for the upper-right corner"""
        z = len(str(total))
        self.pager = str(number).zfill(z) + "-" + str(total).zfill(z)

    def set_palette(self, palette=None):
        """Define an eight-color palette"""
        if palette:
            self.palette = palette
        else:
            self.palette = ("#222222", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                            "#FFAAAA", "#FFAAFF", "#FFFFAA", "#DDDDDD")

    def show_text(self, list, fore=(3, 5), back=(0, 0)):
        nodes = []
        for i, line in enumerate(list):
            fg, bg = fore[i%len(fore)], back[i%len(back)]
            nodes.append({'w': 250, 'h': 22, 'text': line,
                          'bgcolor': self.palette[bg],
                          'color': self.palette[fg]})
        self.nodes = nodes
        return self.show_table(nodes)


def get_directory(dirname):
    """Return the unhidden contents of a directory

    Color-codes each file according to the palette. Directories are
    blue. Executables are green. Symbolic links are cyan. Mount
    points are red.
    """
    files = os.listdir(dirname)
    files.sort()
    list, shade = [], []
    for name in files:
        if name[0] != ".":
            path = os.path.join(dirname, name)
            list.append(name)
            if os.path.islink(path):
                shade.append(3)
            elif os.path.ismount(path):
                shade.append(4)
            elif os.path.isdir(path):
                shade.append(1)
            elif os.access(path, os.X_OK):
                shade.append(2)
            else:
                shade.append(7)
    return list, shade

def get_echoes(dirname):
    """Return the output of shell scripts"""
    files = os.listdir(dirname)
    files.sort()
    echoes = []
    for name in files:
        path = os.path.join(dirname, name)
        if (os.path.splitext(path)[1] in (".bat", ".cmd", ".sh")
                and os.access(path, os.X_OK)):
            echo = str(subprocess.check_output(path))
            echo = echo.split("b'")[1]
            echo = echo.split("\\n'")[0]
            echoes.append(echo)
    return echoes

def get_files(dirname, ext):
    files = os.listdir(dirname)
    files.sort()
    list = []
    for name in files:
        if os.path.splitext(name)[1] == ext:
            list.append(name)
    return list

# based on a color scheme of GNOME Terminal
Solarize = ("#2D2D2D", "#268BD2", "#859900", "#2AA198",
            "#DC322F", "#D33682", "#B58900", "#EEE8D5")
# based on four-color CGA modes
Quadro_A = ("#222222", "#5555AA", "#55AA55", "#DDDDDD",
            "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD")
Quadro_B = ("#222222", "#55AAAA", "#AA55AA", "#DDDDDD",
            "#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD")
# based on TWM color schemes
Tabman_A = ("#B03060", "#22AA99", "#22AA99", "#D9D9D9",
            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
Tabman_B = ("#708090", "#22AA99", "#B03060", "#D9D9D9",
            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
# based on part of the EGA palette
Enhanced = ("#222222", "#AAAAFF", "#AAFFAA", "#AAFFFF",
            "#FFAAAA", "#FFAAFF", "#FFFFAA", "#DDDDDD")
