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
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageTk


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
        self.palette = ("#222222", "#AAAAFF", "#AAFFAA", "#AAFFFF",
                        "#FFAAAA", "#FFAAFF", "#FFFFAA", "#DDDDDD")
        self.bg, self.bd, self.tb = "#222222", "#FFFFAA", "#222222"
        self.bcolor = (self.palette[3], self.palette[5])
        self.width = width
        self.height = height
        self.bw, self.bh, self.pad = 100, 25, 5
        self.padding = 5

    def draw_window(self):
        left, top, right, bottom = 0, 0, self.width, self.height
        window = Image.new("RGB", (right, bottom))
        draw = ImageDraw.Draw(window)
        draw.rectangle((left, top, right, bottom), outline=self.bd, fill=self.bd)
        draw.rectangle((left+2, top+22, right, bottom), outline=self.bg, fill=self.bg)
        return window, draw

    def get_table(self, list, start=0):
        left, top, right, bottom = 0, 0, self.width, self.height
#        display = Image.new("RGB", (right, bottom))
#        draw = ImageDraw.Draw(display)
        # draw display border
#        draw.rectangle((left, top, right, bottom), outline=self.bd, fill=self.bd)
#        draw.rectangle((left+2, top+22, right, bottom), outline=self.bg, fill=self.bg)
        display, draw = self.draw_window()
        # draw display title
        draw.text((left+5, top), self.name, font=self.font, fill=self.bg)
        # draw pagination numbers
        z = len(str(len(list)))
        text = str(start).zfill(z) + "-" + str(len(list)).zfill(z)
        x = self.width - self.font.getsize(text)[0]
        draw.rectangle((x-3, top, x-1, top+22), outline=self.tb, fill=self.tb)
        draw.text((x, top), text, font=self.font, fill=self.tb)
        # draw badges
        x, y = self.padding, self.bh
        for i in range(start, len(list)):
            text = list[i]
            color = self.bcolor[i%len(self.bcolor)]
            rect = (x, y, x+self.bw, y+self.bh)
            draw.rectangle(rect, outline=color, fill=color)
            draw.text((x, y), text, font=self.font, fill=self.bg)
            y = y + self.bh + self.padding
            if y > bottom:
                x, y = x + self.bw + self.padding, self.bh
        return ImageTk.PhotoImage(display)

    def set_font(self, path, size):
        if os.path.exists(path): self.font = ImageFont.truetype(path, size)

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
