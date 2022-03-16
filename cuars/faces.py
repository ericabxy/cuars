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

So far, this module uses nothing but builtins. Consider keeping it
that way.
"""

class Table():
    """A panel of evenly-spaced controls."""

    def __init__(self, width, height, names, left=5, top=5):
        badges, x, y = [], left, top
        for i, name in enumerate(names):
            color = ("#00FFFF", "#FF00FF")[i % 2]
            badge = Badge(name, x, y)
            badge.bgcolor, badge.color = color, "#000000"
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
    """Binary data in fixed-width lines."""

    def __init__(self, width, height, data):
        self.width, self.height = width, height
        self.data = data

    def get_hexadecimal(self, length=1, width=16):
        """Parse the data as hexadecimal integers."""
        lines = []
        for i in range(0, len(self.data), width):
            line = self.data[i: i + width]
            lines.append(line.hex(" ", length))
        return lines

    def get_characters(self, encoding='ascii', length=1, width=64):
        """Parse the data as ascii characters."""
        lines = []
        for i in range(0, len(self.data), width):
            line = self.data[i: i + width]
            lines.append(line.decode(encoding))
        return lines
