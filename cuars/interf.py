#!/usr/bin/env python3
#Copyright 2022 Eric Duhamel
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
#
"""
Simple command interfaces. Determine the shape of data and controls
according to a window of specific width and height.

'Table' is for listing filenames, contents of directories.

'Badge' represents a filename in a table.

'Matrix' is for displaying the contents of a binary file.
"""

class Table():
    """A panel of evenly-spaced touchable controls."""

    def __init__(self, width, height, names):
        badges, x, y = [], 0, 0
        for i, name in enumerate(names):
            color = ("#00FFFF", "#FF00FF")[i % 2]
            badge = Badge(name, x, y, 100, 25)
            badge.color = color
            badges.append(badge)
            y = y + 30
            if y > height:
                x, y = x + 105, 0
        self.badges = badges


class Badge():
    """A touchable control with a label."""

    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = "#AAAAAA"

    def click(self):
        print(self.name)


class Matrix():
    """Binary data displayed in a fixed-width table."""

    def __init__(self):
        return None
