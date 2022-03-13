#!/usr/bin/env python3
#a stylized user interface to the filesystem
#    Copyright 2022 Eric Duhamel
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see
#    <https://www.gnu.org/licenses/>. import os
#
import tkinter

from cuars import interf
from PIL import Image

directory = os.getcwd()
basename = os.path.basename(directory)
table = interf.Table(320, 200, os.listdir(directory))

class Window(tkinter.Tk):
    def __init__(self, directory):
        super().__init__()
        self.title(os.path.basename(directory))
        self.geometry("320x200")
        self.configure(bg='black')
        table = interf.Table(320, 200, os.listdir(directory))
        for badge in table.badges:
            name, color = badge.name, badge.color
            x, y, width, height = badge.x, badge.y, badge.width, badge.height
            fileobj = File(name)
            button = tkinter.Button(self, text=name.upper(),
                    bg=color,
                    command=fileobj.click)
            button.place(x=x, y=y, width=width, height=height)


class File():
    def __init__(self, name):
        self.name = name

    def click(self):
        if os.path.isdir(self.name):
            print(os.listdir(self.name))  # list contents of directory
        elif os.path.isfile(self.name):
            with open(self.name, 'rb') as file:
                print(file.read(64))  # print first 64 bytes of file


if __name__ == "__main__":
    directory = os.getcwd()
    window = Window(directory)
    window.mainloop()
