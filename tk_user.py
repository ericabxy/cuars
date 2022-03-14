#!/usr/bin/env python3
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
#    <https://www.gnu.org/licenses/>.
import os

import tkinter

from cuars import interf

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("tk_user")
        self.geometry("320x240")


class PathObject():
    def __init__(self, fullpath):
        self.directory = os.path.dirname(fullpath)
        self.name = os.path.basename(fullpath)

    def click(self):
        path = os.path.join(self.directory, self.name)
        if os.path.isdir(path):  # show contents of directory
            fullpath = os.path.join(self.directory, self.name)
            panel = Panel(window)
            panel.make_table(fullpath)
            panel.tkraise()
        elif os.path.isfile(path):
            fullpath = os.path.join(self.directory, self.name)
            file = open(fullpath, 'rb')
            panel = Panel(window)
            panel.make_matrix(file.read(256))
            panel.tkraise()


class Panel(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='black', width=320, height=200)

    def make_table(self, directory):
        table = interf.Table(320, 200, os.listdir(directory))
        for badge in table.badges:
            fullpath = os.path.join(directory, badge.name)
            fileobj = PathObject(fullpath)
            button = tkinter.Button(self, text=badge.name.upper(),
                    bg=badge.bgcolor, fg=badge.color,
                    command=fileobj.click)
            button.place(x=badge.x, y=badge.y,
                    height=badge.height, width=badge.width)
        self.place(x=0, y=40)

    def make_matrix(self, filename):
        matrix = interf.Matrix(320, 200, filename)
        label = tkinter.Label(self, text=matrix.script,
                bg='black', fg='lightgray')
        label.place(x=0, y=0)
        self.place(x=0, y=40)

    def click(self):
        self.tkraise()


if __name__ == "__main__":
    window = Window()
    homeobj = PathObject(os.path.expanduser("~"))
    workobj = PathObject(os.getcwd())
    rootobj = PathObject("/")
    homebtn = tkinter.Button(window, text="home", command=homeobj.click)
    rootbtn = tkinter.Button(window, text="root", command=rootobj.click)
    workbtn = tkinter.Button(window, text="work", command=workobj.click)
    homebtn.place(x=0, y=0)
    rootbtn.place(x=100, y=0)
    workbtn.place(x=200, y=0)
    window.mainloop()
