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
"""
A test application to demonstrate CUARS with a Tcl/Tk interface.
"""
import os

import tkinter as tk

import cuars

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
        self.window.open_path(self.path)


class MatrixFrame(tk.LabelFrame):
    def __init__(self, container, width, height, title="TITLE"):
        super().__init__(container)
        self.configure(bg='yellow', text=title)
        self.text = tk.Text(self, bg='black', fg='white', state='disabled')
        self.text.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.button = tk.Button(self.text, text="CLICK")
        self.button.pack(side=tk.RIGHT)
        self.place(x=0, y=0, width=width, height=height)

    def put_matrix(self, matrix):
        self.matrix = matrix
        self.show_hex()

    def show_hex(self):
        self.text.configure(state='normal')
        self.text.delete("1.0", tk.END)
        for line in self.matrix.get_hexadecimal():
            self.text.insert(tk.END, line)
            self.text.insert(tk.END, "\n")
        self.text.configure(state='disabled')
        self.button.configure(text="ASC", command=self.show_asc)

    def show_asc(self):
        self.text.configure(state='normal')
        self.text.delete("1.0", tk.END)
        for line in self.matrix.get_alphanumeric():
            self.text.insert(tk.END, line)
            self.text.insert(tk.END, "\n")
        self.text.configure(state='disabled')
        self.button.configure(text="HEX", command=self.show_hex)

class TableFrame(tk.LabelFrame):
    def __init__(self, container, width, height, title="TITLE"):
        super().__init__(container)
        self.configure(bg='yellow', text=title)
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.place(x=0, y=0, width=width, height=height)

    def show_button(self, badge, root):
        button = BadgeButton(self.canvas, badge, root)


class Window(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.title("CUARS Test Window")
        self.geometry("x".join([str(width), str(height)]))
        self.frame = None
        self.button = tk.Button(self, text="HOME", command=self.go_home)
        self.button.pack(side='bottom')

    def open_path(self, path):
        if self.frame:  # recycle previous object
            self.frame.destroy()
        if os.path.isdir(path):
            os.chdir(path)
            directory = os.getcwd()
            title = os.path.basename(directory).upper()
            names = os.listdir(directory)
            table = cuars.Table(640, 400, names)
            self.frame = TableFrame(self, 640, 400, title=title)
            for badge in table.badges:
                self.frame.show_button(badge, self)
        elif os.path.isfile(path):
            title = os.path.basename(path).upper()
            self.frame = MatrixFrame(self, 640, 400, title=title)
            with open(path, 'rb') as file:
                matrix = cuars.Matrix(640, 400, file.read(256))
            self.frame.put_matrix(matrix)

    def go_home(self):
        home = os.path.expanduser("~")
        self.open_path(home)


if __name__ == "__main__":
    window = Window(640, 480)
    window.mainloop()
