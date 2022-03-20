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

class BinaryData():
    def __init__(self, data):
        self.data = data

    def get_hex(self, length=1, width=16):
        """Return hexadecimal strings from the data."""
        lines = []
        for i in range(0, len(self.data), width):
#            number = hex(i)[2:].zfill(8)
            line = self.data[i: i + width].hex()
#            line = "  ".join([number, line]).upper()
            lines.append(line)
        return lines

    def get_lines(self):
        """Return the data sequence unaltered."""
        return self.data.splitlines()

    def get_pairs(self, byteorder='little'):
        """Return pairs of integers."""


class BinaryFile(BinaryData):
    def __init__(self, path):
        with open(path, 'rb') as file:
            data = file.read(4096)
        super().__init__(data)
