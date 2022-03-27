#!/usr/bin/env python3
#    Copyright 2022 Eric Duhamel
#
#    This file is part of CUARS.
#
#    CUARS is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CUARS is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CUARS. If not, see <https://www.gnu.org/licenses/>.
"""
A list of evenly-spaced choices.

In the case of a directory, options are color-coded with a 24-bit color
depth hexadecimal string.
"""
import os

DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 200
OPTION_LEFT = 5
OPTION_TOP = 35
BTN_WIDTH = 120
BTN_HEIGHT = 30
BTN_PADDING = 5

class OptionsDir():
    """A list of choices from a directory of files.

    This object is expected to have some essential attributes.

    + the name of the directory that was listed
    + a list of "Option" objects called "options"
    + a "pagelen" indicating how many options fit on one column
    """

    def __init__(self, path, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.width, self.height = width, height
        self.names = os.listdir(path)
        self.dirname = path
        vertical_space = height - OPTION_TOP
        button_space = BTN_HEIGHT + BTN_PADDING
        self.pagelen = int(vertical_space / button_space) + 1
        self.pages = int(len(self.names) / self.pagelen) + 1
        self.pagelast = self.pages * self.pagelen
        self.start = 0
        self.stop = len(self.names)
        self.set_options()

    def page_down(self):
        self.start = (self.start - self.pagelen) % self.pagelast

    def page_up(self):
        self.start = (self.start + self.pagelen) % self.pagelast

    def set_options(self, left=OPTION_LEFT, top=OPTION_TOP,
                    padding=BTN_PADDING):
        options = []
        x, y = left, top
        sliced = self.names[self.start:self.stop]
        for i, name in enumerate(sliced):
            path = os.path.join(self.dirname, name)
            option = OptionPath(path, x, y)
            options.append(option)
            if y + padding + option.height > self.height:
                y, x = top, x + padding + option.width
            else:
                y = y + padding + option.height
        self.options = options
        self.total = len(self.names)


class OptionPath():
    """A rectangular control with a label.

    This object is expected to have some essential attributes.

    + the "name" of the associated object
    + rectangular dimensions "x", "y", "width", "height" ("x2", "y2"?)
    + a foreground "color" and a background "bgcolor"
    """

    def __init__(self, path, x, y, width=BTN_WIDTH, height=BTN_HEIGHT):
        self.path = path
        self.name = os.path.basename(path)
        self.x, self.y = x, y
        self.width, self.height = width, height
        if os.path.ismount(path):
            self.bgcolor = "#FFAAAA"
        elif os.path.islink(path):
            self.bgcolor = "#AAFFFF"
        elif os.path.isdir(path):
            self.bgcolor = "#AAAAFF"
        elif os.path.isfile(path) and os.access(path, os.X_OK):
            self.bgcolor = "#AAFFAA"
        elif os.path.isfile(path):
            self.bgcolor = "#FFFFFF"

    def activate(self):
        """Descend into the directory or view/exec the file."""
        print(self.name)  # This is just a placeholder statement
