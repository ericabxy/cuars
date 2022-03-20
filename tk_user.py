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
from cuars import binary, option

class Window(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.width, self.height = width, height
        self.title("CUARS Test Window")
        self.geometry("x".join([str(width), str(height)]))
        self.option_add("*Button.Font", "ArialNarrow 12 bold")
        self.option_add("*Label.Font", "ArialNarrow 14 bold")
        self.option_add("*bg", "#FF0000")
        self.option_add("*relief", "flat")
        self.frame = None
        self.resizable(False, False)
        self.open_present()

    def open_file(self, path):
        print("Window.open_file", path)
        if self.frame:
            self.frame.destroy()  # recycle previous object
        title = os.path.basename(path).upper()
        self.frame = BinaryFrame(self, path)

    def open_present(self):
        print("Window.open_present")
        if self.frame:
            self.frame.destroy()  # recycle previous object
        directory = os.getcwd()
#        title = os.path.basename(directory).upper()
#        names = os.listdir(directory)
#        table = cuars.Table(self.width, self.height, names)
        self.frame = DirectoryFrame(self, directory)
#        for option in table.badges:
#            option.path = os.path.join(directory, option.name)
#            self.frame.put_button(option)

    def open_home(self, *args):
        print("Window.open_home")
        print(args)
        home = os.path.expanduser("~")
        os.chdir(home)
        self.open_present()


class MainFrame(tk.Frame):
    def __init__(self, container, name):
        super().__init__(container)
        self.configure(bg='black')
        self.titlebar = tk.Frame(self, bg='black')
        self.titlebar.pack(side='top', fill='x')
        self.title = tk.Label(self, text=name, anchor='w',
                bg='yellow')
        self.title.place(x=0, y=0, width=container.width-50, height=20)
        self.home = tk.Button(self, text="HOME", bg='yellow')
        self.home.configure(command=container.open_home)
        self.home.place(x=container.width-45, width=45,
                        y=0, height=20)
        self.scroll = tk.Scrollbar(self, bg='black', troughcolor='yellow2')
        self.scroll.place(x=0, y=20, width=15, height=container.height-20)
        self.pack(expand=True, fill='both')
        self.container = container

    def open_file(self, path):
        """Pass on any 'open file' commands from widgets."""
        print("MainFrame.open_file", path)
        self.container.open_file(path)

    def open_present(self):
        """Pass on any 'open file' commands from widgets."""
        print("MainFrame.open_present")
        self.container.open_present()


class BinaryFrame(MainFrame):
    def __init__(self, container, path):
        name = os.path.basename(path).upper()
        super().__init__(container, name)
        self.ctrl = tk.Button(self, text="CTRL")
        self.ctrl.pack(side='right')
        self.text = tk.Text(self, bg='black', fg='white')
        self.text.place(x=15, width=container.width-57,
                        y=20, height=container.height-20)
        self.scroll.configure(command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.binary = binary.BinaryFile(path)
        self.show_hex()

    def show_hex(self):
        self.text.configure(state='normal')
        self.text.delete("1.0", tk.END)
        for line in self.binary.get_hex():
            self.text.insert(tk.END, line)
            self.text.insert(tk.END, "\n")
        self.text.configure(state='disabled')
        self.ctrl.configure(text="HEX", command=self.show_seq)

    def show_seq(self):
        self.text.configure(state='normal')
        self.text.delete("1.0", tk.END)
        for line in self.binary.get_lines():
            self.text.insert(tk.END, line)
            self.text.insert(tk.END, "\n")
        self.text.configure(state='disabled')
        self.ctrl.configure(text="ASC", command=self.show_hex)


class DirectoryFrame(MainFrame):
    def __init__(self, container, path):
        name = os.path.basename(path).upper()
        super().__init__(container, name)
#        names = os.listdir(path)  # TODO: object should do this
#        table = cuars.Table(200, 200, names)  # deprecated
        dir = option.OptionsDir(path)
        for opt in dir.options:  # TODO: bad naming
#            option.path = os.path.join(path, option.name)
            if os.path.isdir(opt.path):
                button = DirButton(self, opt)
            elif os.path.isfile(opt.path):
                button = FileButton(self, opt)


class FileButton(tk.Button):
    def __init__(self, container, option, bg="#FFFFFF", abg="#F0F0F0"):
        super().__init__(container)
        print("FileButton.path", option.path)
        path = option.path
        if os.access(path, os.X_OK) and not os.path.isdir(path):
            bg, abg = "#AAFFAA", "#A0F0A0"
        self.configure(text=option.name.upper(), command=self.activate)
        self.configure(bg=bg, activebackground=abg, highlightcolor="#FFFFFF")
        self.configure(padx=0, anchor='nw')
        self.place(x=option.x, width=option.width,
                   y=option.y, height=option.height)
        self.path = option.path  # path to file
        self.container = container

    def activate(self):
        print("FileButton.activate", self.path)
        self.container.open_file(self.path)


class DirButton(FileButton):
    """Directory version of FileButton that color-codes itself."""

    def __init__(self, container, option):
        path = option.path
        if os.path.ismount(path):
            bg, abg = "#FFAAAA", "#F0A0A0"
        elif os.path.islink(path):
            bg, abg = "#AAFFFF", "#A0F0F0"
        else:
            bg, abg = "#AAAAFF", "#A0A0F0"
        super().__init__(container, option, bg, abg)

    def activate(self):
        print("DirButton.activate", self.path)
        os.chdir(self.path)
        self.container.open_present()


if __name__ == "__main__":
    window = Window(320, 200)
    window.mainloop()
