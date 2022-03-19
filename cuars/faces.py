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
Simple command interfaces. Determine the shape of data and controls
according to a window of specific width and height.

'Table' arranges filenames or commands in a grid pattern.

'Badge' represents selectable files or commands.

'Matrix' creates binary data strings with a fixed width.

'Script' displays reflowable text in a vertical space.
"""

class Table():
    """A panel of evenly-spaced controls."""

    def __init__(self, width, height, names, left=5, top=5):
        badges, x, y = [], left, top
        for i, name in enumerate(names):
            badge = Badge(name, x, y)
            badge.bgcolor = ("#00FFFF", "#FF00FF")[i % 2]
            badge.color = "#000000"
            badges.append(badge)
            y = y + badge.height + top
            if y > height:
                x, y = x + badge.width + left, top
        self.badges = badges


class Badge():
    """A rectangular control with a label."""

    def __init__(self, name, x, y, width=120, height=30):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.bgcolor = "#AAAAAA"
        self.color = "#000000"

    def activate(self):
        print(self.name)


class Matrix():
    """Binary data arranged into cells."""

    def __init__(self, data, width, height, left=5, top=5):
        self.data = data
        self.width, self.height = width, height
        self.left, self.top = left, top

    def get_rawdata(self):
        lines = []
        for i in range(0, len(self.data), 16):
            line = self.data[i: i + 16].hex(" ")
            ascii = self.data[i: i + 16].decode()
            trans = ascii.maketrans("\n\t\r", "...")
            ascii = ascii.translate(trans)
            lines.append("   ".join([line, ascii]))
        return lines

    def get_hexadecimal(self, length=1, width=16):
        x, y = self.left, self.top
        cells = []
        for i in range(0, len(self.data), length):
            datum = self.data[i: i + length].hex()
            cell = Cell(datum, x, y)
            cells.append(cell)
            x = x + cell.width + self.left
            if x > self.width:
                x, y = self.left, y + cell.height + self.top
        return cells

    def get_alphanumeric(self, encoding='ascii', length=1, width=80):
        """Parse the data as ascii characters."""
        lines = []
        for i in range(0, len(self.data), width):
            line = self.data[i: i + width]
            try:
                lines.append(line.decode(encoding))
            except UnicodeDecodeError:
                print("caught:", UnicodeDecodeError)
        return lines


class Cell():
    def __init__(self, datum, x, y, width=20, height=15):
        self.datum = datum
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.bgcolor = "#555555"
        self.color = "#AAAAAA"
