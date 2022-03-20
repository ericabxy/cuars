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

    def __init__(self, width, height, names, ox=20, oy=25, dx=5, dy=5):
        badges, x, y = [], ox, oy
        for i, name in enumerate(names):
            badge = Badge(name, x, y)
            badge.bgcolor = ("#AAAAFF", "#AAFFAA")[i % 2]
            badge.color = "#000000"
            badges.append(badge)
            y = y + badge.height + dy
            if y > height:
                x, y = x + badge.width + dx, oy
        self.badges = badges


class Badge():
    """A rectangular control with a label."""

    def __init__(self, name, x, y, width=120, height=30):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.bgcolor = "#FFFFFF"
        self.color = "#000000"

    def activate(self):
        print(self.name)
