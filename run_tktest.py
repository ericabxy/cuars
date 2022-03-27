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

from cuars import binary, options

class Window(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.width, self.height = width, height
        self.title("CUARS Test Window")
        self.geometry("x".join([str(width), str(height)]))
        self.option_add("*Text.Font", "Mono 8")
        self.option_add("*Button.Anchor", "w")
#        self.option_add("*relief", "flat")
        self.frame = None
        self.file_frame = None
        self.resizable(False, False)
        self.open_present()

    def open_file(self, path):
        print("Window.open_file", path)
        self.file_frame = BinaryFrame(self, path)
        self.file_frame.tkraise()

    def open_present(self):
        """Open the current working directory."""
        if self.frame: self.frame.destroy()  # recycle previous objects
        if self.file_frame: self.file_frame.destroy()
        directory = os.getcwd()
        self.frame = DirectoryFrame(self, directory)

    def open_home(self, *args):
        print("Window.open_home")
        print(args)
        home = os.path.expanduser("~")
        os.chdir(home)
        self.open_present()


class MainFrame(tk.Frame):
    """Basic root frame to organize widgets.

    Contains a title bar for controls and a canvas for content.
    """

    def __init__(self, container, name):
        super().__init__(container)
        container.update()
        width = container.winfo_width()
        height = container.winfo_height()
        self.place(x=0, y=0, width=width, height=height)
        self.canvas = ContentArea(self)
        self.titlebar = TitleBar(self, name)
        self.container = container

    def open_file(self, path):
        """Pass on any 'open file' commands from widgets."""
        self.container.open_file(path)

    def open_home(self):
        """Catch and obey any presses of titlebar '~' button."""
        home = os.path.expanduser("~")
        os.chdir(home)
        self.open_present()

    def open_present(self):
        """Tell root window to open CWD."""
        self.container.open_present()

    def page_down(self):
        print("MainFrame.page_down")

    def page_up(self):
        print("MainFrame.page_up")


class TitleButton(tk.Button):
    def __init__(self, container, text, command):
        super().__init__(container)
        self.configure(text=text, command=command)
        self.pack(side='left')


class TitleBar(tk.Frame):
    """Upper area containing information and controls."""

    def __init__(self, container, name):
        super().__init__(container)
        container.update()
        width = container.winfo_width()
        self.place(x=0, y=0, width=width)
        self.home = TitleButton(self, "~", container.open_home)
        self.title = tk.Label(self, text=name, anchor='w')
        self.title.pack(side='left', fill='x', expand=True)
        self.page = TitleButton(self, "00", container.page_down)
        self.pager = TitleButton(self, "000", container.page_up)


class ContentArea(tk.Canvas):
    def __init__(self, container):
        super().__init__(container)
        self.pack(side='top', fill='both')
        self.container = container
        self.update()
        self.width, self.height = self.winfo_width(), self.winfo_height()

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
        self.text = tk.Text(self.canvas)
        self.text.place(x=0, y=30)
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
        left, top, width, height = 5, 5, self.canvas.width, self.canvas.height
        self.directory = options.OptionsDir(path, width=width, height=height)
        self.set_buttons()

    def page_down(self):
        print("DirectoryFrame.page_down")
        self.directory.page_down()
        self.directory.set_options()
        self.titlebar.page.configure(text=self.directory.start)
        self.set_buttons()

    def page_up(self):
        print("DirectoryFrame.page_up")
        self.directory.page_up()
        self.directory.set_options()
        self.titlebar.page.configure(text=self.directory.start)
        self.set_buttons()

    def set_buttons(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()  # erase for rerendering
        for option in self.directory.options:
            if os.path.isdir(option.path):
                button = DirButton(self.canvas, option)
            elif os.path.isfile(option.path):
                button = FileButton(self.canvas, option)
        self.titlebar.page.configure(text=self.directory.start)
        self.titlebar.pager.configure(text=self.directory.total)


class FileButton(tk.Button):
    def __init__(self, container, option):
        super().__init__(container)
        self.container = container
        self.path = option.path  # path to file
        self.configure(text=option.name.upper(), command=self.activate)
        self.configure(bg=option.bgcolor, padx=0, anchor='w')
        self.place(x=option.x, width=option.width,
                   y=option.y, height=option.height)

    def activate(self):
        self.container.open_file(self.path)


class DirButton(FileButton):
    def activate(self):
        os.chdir(self.path)
        self.container.open_present()


if __name__ == "__main__":
    window = Window(240, 135)
    window.mainloop()
