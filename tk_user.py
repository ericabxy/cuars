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

import tkinter as tk

import cuars

class DisplayFrame(tk.LabelFrame):
    """Generic themed frame for CUARS panels."""

    def __init__(self, container, width, height, left=5, top=20):
        super().__init__(container)
        self.configure(bg='yellow', text="TITLE")
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.place(x=left, y=top, width=width-left, height=height-top)
        self.place(x=0, y=0, width=width, height=height)


class BadgeButton(tk.Button):
    def __init__(self, container, badge, window):
        super().__init__(container)
        self.configure(text=badge.name.upper(), bg=badge.bgcolor,
                fg=badge.color, command=self.activate)
        self.place(x=badge.x, y=badge.y, width=badge.width,
                height=badge.height)
        self.path = os.path.join(os.getcwd(), badge.name)
        self.window = window

    def activate(self):
        self.window.do_path(self.path)


class Window(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.title("CUARS Test Window")
        self.geometry("x".join([str(width), str(height)]))
        self.frame = None
        self.button = tk.Button(self, text="HOME", command=self.go_home)
        self.button.pack(side='bottom')

    def do_path(self, path):
        if self.frame:
            self.frame.destroy()
        if os.path.isdir(path):
            os.chdir(path)
            directory = os.getcwd()
            names = os.listdir(directory)
            table = cuars.Table(640, 400, names)
            self.frame = DisplayFrame(self, 640, 400)
            for badge in table.badges:
                button = BadgeButton(self.frame.canvas, badge, self)
        elif os.path.isfile(path):
            with open(path, 'rb') as file:
                matrix = cuars.Matrix(320, 200, file.read(256))
            self.frame = DisplayFrame(self, 640, 400)
            self.text = tk.Text(self.frame.canvas,
                    bg='black', fg='white')
            self.text.insert('1.0', matrix.script)
            self.text.configure(state='disabled')
            self.text.pack()

    def go_home(self):
        self.do_path(home)


class TableFrame(tk.Frame):
    """A widget containing filenames as buttons."""

    def __init__(self, container, directory):
        """Arrange filenames as buttons on a canvas."""
        super().__init__(container)
        self.container = container
        name = os.path.basename(directory).upper()
        label = tk.Label(self, text=name, anchor='w',
                bg='yellow', fg='black')
        label.place(x=0, y=0, width=100, height=20)
        self.configure(bg='yellow')
        self.place(x=0, y=0, width=640, height=400)
        self.show(directory)

    def show(self, directory):
        table = cuars.Table(640, 400, os.listdir(directory))
        canvas = tk.Canvas(self, bg='black')
        for badge in table.badges:
            badge.path = os.path.join(directory, badge.name)
            button = Opener(canvas, badge, self.container)
        canvas.place(x=5, y=20, width=635, height=380)
        self.tkraise()


class File(tk.Frame):
    """A panel displaying contents of a file as binary data."""

    def __init__(self, container, path):
        """Place a label displaying the hex dump."""
        super().__init__(container)
        name = os.path.basename(path).upper()
        label = tk.Label(self, text=name, anchor='w',
                bg='yellow', fg='black')
        label.place(x=0, y=0, width=100, height=20)
        self.configure(bg='yellow')
        self.place(x=0, y=0, width=640, height=400)
        self.show(path)

    def show(self, path):
        with open(path, 'rb') as file:
            matrix = cuars.Matrix(320, 200, file.read(256))
        label = tk.Label(self, text=matrix.script, anchor='nw',
                bg='black', fg='lightgray', font='TkFixedFont')
        label.place(x=5, y=20, width=635, height=440)
        self.tkraise()


class Opener(tk.Button):
    """Object stores a path to a file on the system."""

    def __init__(self, container, badge, window):
        """Store information for creating a new panel."""
        super().__init__(container)
        self.path = badge.path
        self.configure(text=badge.name.upper(), command=self.activate,
                bg=badge.bgcolor, fg=badge.color)
        self.place(x=badge.x, y=badge.y,
                width=badge.width, height=badge.height)
        self.window = window

    def activate(self):
        """Create a panel for the folder or file contents."""
        if os.path.isdir(self.path):  # show file contents of directory
            self.window.do_path(self.path)
        elif os.path.isfile(self.path):  # show binary contents of file
            self.window.new_file(self.path)


if __name__ == "__main__":
    window = Window(640, 480)
    home = os.path.expanduser("~")
#    frame = window.do_path(home)
#    badge = cuars.Badge(home, 0, 0)
#    badge.path = home
#    home_path = Opener(window, badge, window)
#    home_path.pack(side='bottom')
    window.mainloop()
