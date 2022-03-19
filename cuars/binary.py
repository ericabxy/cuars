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
Handles binary data by converting it or decoding it into lines of
printable characters.

BinaryFile: takes a path to a file to open.

BinaryData: takes a binary data sequence.
"""

class BinaryFile():
    def __init__(self, path, width=320, height=200):
        with open(path, 'rb') as file:
            self.data = file.read()

    def get_hex(self, length=2, width=16):
        """Return hexadecimal strings from the data."""
        lines = []
        for i in range(0, len(self.data), width):
            number = hex(i)[2:].zfill(8)
            line = self.data[i: i + width].hex(" ", length)
            line = "  ".join([number, line]).upper()
            lines.append(line)
        return lines

    def get_seq(self, length=40):
        """Return the data sequence unaltered."""
        lines = []
        for i in range(0, len(self.data), length):
            line = self.data[i: i + length]
            lines.append(line)
        return lines

    def get_pairs(self, byteorder='little'):
        """Return pairs of integers."""
