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

from PIL import Image, ImageDraw, ImageFont


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
        self.width = width
        self.height = height
        self.padding = 5

    def set_font(self, path, size):
        if os.path.exists(path):
            self.font = ImageFont.truetype(path, size)
            return True
        else:
            return False

    def show_badges(self, list, fore=(0, 0), back=(3, 5), mark=None):
        """Display interactive buttons (badges) in a table."""
        badges = []
        for i, line in enumerate(list):
            fg, bg = fore[i%len(fore)], back[i%len(back)]
            badges.append({'w': 100, 'h': 25, 'text': line,
                          'bgcolor': self.palette[bg],
                          'color': self.palette[fg]})
        self.nodes = badges
        return self.show_table(badges, mark)

    def show_text(self, list, fore=(3, 5), back=(0, 0)):
        nodes = []
        for i, line in enumerate(list):
            fg, bg = fore[i%len(fore)], back[i%len(back)]
            nodes.append({'w': 250, 'h': 22, 'text': line,
                          'bgcolor': self.palette[bg],
                          'color': self.palette[fg]})
        self.nodes = nodes
        return self.show_table(nodes)

    def show_table(self, badges, mark=None, start=0):
        left, top, right, bottom = 0, 0, self.width, self.height
        # Draw the display border and table background
        rect, color = (left, top, right, bottom), self.bd
        self.draw.rectangle(rect, outline=color, fill=color)
        rect, color = (left+2, top+22, right, bottom), self.bg
        self.draw.rectangle(rect, outline=color, fill=color)
        # Draw all badges that will fit in the table area
        i, x, y = start, left+5, 25
        while i < len(badges) and x < self.width:
            badge = badges[i]
            w, h = badge['w'], badge['h']
            rect, color = (x, y, x+w, y+h), badge['bgcolor']
            self.draw.rectangle(rect, outline=color, fill=color)
            text, color = badges[i]['text'].upper(), badge['color']
            if i == mark:
                rect = (x+5, y, x+8, y+h)
                self.draw.rectangle(rect, outline=color, fill=color)
                self.draw.text((x+10, y), text, font=self.font, fill=color)
            else:
                self.draw.text((x, y), text, font=self.font, fill=color)
            i, y = i+1, y+h+self.padding
            if y+h > bottom:  # Start next column
                x, y = x+w+self.padding, 25
        # Draw title and paging arrows
        text, color = self.name.upper(), self.tb
        self.draw.text((left+5, top), text, font=self.font, fill=color)
        z = len(str(len(badges)))
        text = str(start).zfill(z) + "-" + str(len(badges)).zfill(z)
        x = self.width - self.font.getsize(text)[0]
        self.draw.rectangle((x-3, top, x-1, top+22), outline=color, fill=color)
        self.draw.text((x, top), text, font=self.font, fill=color)
        return i


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
