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
Presents a list as evenly-spaced buttons for interaction.
"""
import os

class OptionDir():
    def __init__(self, path, left=5, top=5, width=320, height=200):
        options = []
        x, y = left, top
        names = os.listdir(path)
        for i, name in enumerate(names):
            option = Badge(name, x, y)
            option.bgcolor = ("#00FFFF", "#FF00FF")[i % 2]
            option.color = "#000000"
            options.append(option)
            y = y + option.height + top
            if y > height:
                x, y = x + option.width + left, top
        self.options = options

class Option():
    """A rectangular control with a label."""

    def __init__(self, name, x, y, width=120, height=30):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.bgcolor = "#AAAAAA"
        self.color = "#000000"

    def activate(self):
        """Descend into the directory or view/exec the file."""
        print(self.name)
