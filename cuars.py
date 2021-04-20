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
        self.bg, self.bd = "#222222", "#FFFFAA"
        self.width = width
        self.height = height
        self.padding = 5

    def draw_directory(self, paths, mark=None):
        """List directory contents in a table

        Color-codes each file according to the palette. Directories are
        blue. Executables are green. Symbolic links are cyan. Mount
        points are red.
        """
        nodes = []
        for path in paths:
            name = os.path.basename(path)
            node = {'w': 100, 'h': 25, 'text': name}
            if os.path.islink(path):
                node['color'] = self.palette[3]
            elif os.path.ismount(path):
                node['color'] = self.palette[4]
            elif os.path.isdir(path):
                node['color'] = self.palette[1]
            elif os.access(path, os.X_OK):
                node['color'] = self.palette[2]
            else:
                node['color'] = self.palette[7]
            nodes.append(node)
        self.nodes = nodes
        return self.draw_table(nodes, mark)

    def draw_table(self, badges, mark=None, start=0):
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
            rect, color = (x, y, x+w, y+h), badge['color']
            self.draw.rectangle(rect, outline=color, fill=color)
            text, color = badges[i]['text'].upper(), self.bg
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
        text, color = self.name.upper(), self.bg
        self.draw.text((left+5, top), text, font=self.font, fill=color)
        z = len(str(len(badges)))
        text = str(start).zfill(z) + "-" + str(i).zfill(z)
        x = self.width - self.font.getsize(text)[0]
        self.draw.rectangle((x-3, top, x-1, top+22), outline=color, fill=color)
        self.draw.text((x, top), text, font=self.font, fill=color)
        return i
