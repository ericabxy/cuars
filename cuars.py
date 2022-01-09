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
# TODO: shouldn't need the "os" module
from PIL import Image, ImageDraw, ImageFont

class Table():
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
        self.name = "CUARS Table"
        self.pager = "0000"
        self.mark = None
        self.set_colors()
        self.set_colors()
        self.set_pattern()
        self.width = width
        self.height = height
        self.bw, self.bh = 100, 25
        self.left, self.top = 5, 25
        self.space = 5

    def render(self):
        """Render a display with a grid of interactive buttons

        Work-in-progress: still determining scope and brevity.
        Paging: make a dumb method that displays the whole list?
        Mark: can only "mark" a badge on the left side?
        """
        left, top, right, bottom = 0, 0, self.width, self.height
        self.image, draw = self.new_window()
        # draw badges
        x, y = self.left + self.space, self.top + self.space
        rects = []
        for i, text in enumerate(self.list):
            color = self.color[self.pattern[i%len(self.pattern)]]
            rect = (x, y, x+self.bw, y+self.bh)
            draw.rectangle(rect, outline=color, fill=color)
            draw.text((x, y), text, font=self.font, fill=self.color[0])
            rects.append(rect)  # dimensions for touchscreen
            y = y + self.bh + self.space
            if y+self.bh > bottom:
                x = x + self.bw + self.space
                y = self.top + self.space

    def slice(self, list, mark):
        page_height = self.height - self.bh  # height of badge area
        badge_height = self.bh + self.space  # height of badge
        page = math.floor(page_height/badge_height)  # badges per page
        slicer = math.floor(mark / page) * page
        return slicer

    def get_tkimage(self):
        # TODO: this file should not require Tk
        return ImageTk.PhotoImage(self.image)

    def new_window(self):
        window = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(window)
        # border (minimal to allow room for badges)
        draw.rectangle((0, 0, self.width, self.height),
          outline=self.color[7], fill=self.color[7])
        draw.rectangle(
          (self.left, self.top, self.width, self.height),
          outline=self.color[0], fill=self.color[0])
        # title (upper-left)
        draw.text((self.left, 0), self.name, font=self.font,
          fill=self.color[0])
        # pager (upper-right)
        x = self.width - self.font.getsize(self.pager)[0]
        draw.rectangle((x-5, 0, self.width, self.top-1),
          outline=self.color[7], fill=self.color[7])
        draw.rectangle((x-3, 0, x-1, self.top),
          outline=self.color[0], fill=self.color[0])
        draw.text((x, 0), self.pager, font=self.font, fill=self.color[0])
        # mark (indicator along left border)
        if isinstance(self.mark, int):
            markh = self.mark * (self.bh + self.space)
            y = self.top + self.space + markh
            draw.rectangle((0, y - 3, self.left, y + self.bh + 3),
              outline=self.color[0], fill=self.color[0])
            draw.rectangle((0, y, self.left, y + self.bh),
              outline=self.color[7], fill=self.color[7])
        return window, draw

    def pagelen(self):
        page_height = self.height - self.bh
        badge_height = self.bh + self.space
        page_badges = math.ceil(page_height / badge_height)
        return page_badges

    def set_font(self, path, size):
        if os.path.exists(path): self.font = ImageFont.truetype(path, size)

    def set_pager(self, num, total):
        """Paging numbers for the upper-right corner"""
        z = len(str(total))
        if isinstance(num, int):
            self.pager = str(num).zfill(z) + "-" + str(total).zfill(z)
        else:
            self.pager = str(total).zfill(z)

    def set_colors(self, palette=None):
        """Define an eight-color palette"""
        if palette:
            self.color = palette
        else:
            self.color = ("#000000", "#5555FF", "#55FF55", "#55FFFF",
                          "#FF5555", "#FF55FF", "#FFFF55", "#FFFFFF")

    def set_pattern(self, colors=(3, 5)):
        self.pattern = colors

    def set_list(self, list, colors=(3, 5)):
        self.list = list
        self.pattern = colors

class Text():
    def __init__(self, width, height):
        basedir = os.path.dirname(__file__)
        path = os.path.join(basedir, "fonts", "BebasNeue.otf")
        self.font = ImageFont.truetype(path, 22)
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.name = "CUARS Text"
        self.pager = "0000"
        self.mark = None
        self.set_colors()
        self.set_pattern()
        self.set_colors()
        self.width = width
        self.height = height
        self.bw, self.bh = 100, 25
        self.left, self.top = 5, 25
        self.space = 5

    def show_text(self, list, fore=(3, 5), back=(0, 0)):
        nodes = []
        for i, line in enumerate(list):
            fg, bg = fore[i%len(fore)], back[i%len(back)]
            nodes.append({'w': 250, 'h': 22, 'text': line,
                          'bgcolor': self.color[bg],
                          'color': self.color[fg]})
        self.nodes = nodes
        return self.show_table(nodes)


# based on a color scheme of GNOME Terminal
Solarize = ("#2D2D2D", "#268BD2", "#859900", "#2AA198",
            "#DC322F", "#D33682", "#B58900", "#EEE8D5")
# based on four-color CGA modes
Quadro_A = ("#000000", "#FF55FF", "#FF5555", "#FF55FF",
            "#FF5555", "#FF55FF", "#FF5555", "#FFFF55")
Quadro_B = ("#000000", "#55FFFF", "#FF55FF", "#55FFFF",
            "#FF55FF", "#55FFFF", "#FF55FF", "#FFFFFF")
# based on TWM color schemes
Tabman_A = ("#B03060", "#22AA99", "#22AA99", "#D9D9D9",
            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
Tabman_B = ("#708090", "#22AA99", "#B03060", "#D9D9D9",
            "#D9D9D9", "#D9D9D9", "#D9D9D9", "#D9D9D9")
# based on the EGA palette (0, 15, 23, 31, 39, 47, 55, 63)
Enhanced = ("#000000", "#AAAAFF", "#AAFFAA", "#AAFFFF",
            "#FFAAAA", "#FFAAFF", "#FFFFAA", "#FFFFFF")
