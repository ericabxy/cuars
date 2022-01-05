#!/usr/bin/env python3
import os
import sys
import subprocess
import time

import digitalio
import board
import adafruit_rgb_display.st7789 as st7789

import cuars

dirname = len(sys.argv) > 1 and sys.argv[1] or os.getcwd()

def main():
    global dirname
    io = BoardIO()
    display = Display(135, 240)
    interf = cuars.Table(240, 135)
    mark = 0
    print("Interface should appear on the RGB display now")
    while True:
        if os.path.isfile(os.path.join(dirname, "command.ini")):
            dirlist = files(dirname, ".m3u")
            interf.show_badges(dirlist, mark=mark)
        elif os.path.isfile(os.path.join(dirname, "console.ini")):
            dirlist = echoes(dirname)
            name = os.path.basename(dirname)
            interf.bd = interf.palette[0]
            interf.tb = interf.palette[7]
            interf.name = dirlist.pop(0)
            interf.show_text(dirlist, (6, 2, 1, 5))
        else:
            dirlist = os.listdir(dirname)
            s = interf.slice(dirlist, mark)
            interf.set_list(dirlist[s:])
            interf.name = os.path.basename(dirname)
            interf.mark = mark-s
            interf.set_pager(mark+1, len(dirlist))
            interf.render()
        # Display image.
        image = interf.image
        display.show(image, 90)
        # Accept input
        if not io.B.value and not io.A.value:  # both buttons pressed
            io.backlight.value = not io.backlight.value
        elif io.B.value and not io.A.value:  # button 1 pressed
            mark = (mark+1) % len(dirlist)
        elif io.A.value and not io.B.value:  # button 2 pressed
            selected = os.path.join(dirname, dirlist[mark])
            if os.path.isdir(selected):
                mark = 0
                dirname = selected
            print("cd: " + dirname)
        # Wait for refresh
        time.sleep(0.1)


class BoardIO():
    def __init__(self):
        # Turn on the backlight
        self.backlight = digitalio.DigitalInOut(board.D22)
        self.backlight.switch_to_output()
        self.backlight.value = True
        self.A = digitalio.DigitalInOut(board.D23)
        self.B = digitalio.DigitalInOut(board.D24)
        self.A.switch_to_input()
        self.B.switch_to_input()


class Display():
    def __init__(self, width, height):
        print("adafruit: creating the ST7789 display")
        self.disp = self.get_display(width, height)

    def get_display(self, width, height):
        # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None
        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 64000000
        # Setup SPI bus using hardware SPI:
        spi = board.SPI()
        # Create the ST7789 display:
        disp = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
            width=width,
            height=height,
            x_offset=53,
            y_offset=40,
        )
        return disp

    def show(self, image, rotation):
        self.disp.image(image, rotation)


def echoes(dirname):
    """Return the output of shell scripts"""
    files = os.listdir(dirname)
    files.sort()
    echoes = []
    for name in files:
        path = os.path.join(dirname, name)
        if (os.path.splitext(path)[1] in (".bat", ".cmd", ".sh")
                and os.access(path, os.X_OK)):
            echo = str(subprocess.check_output(path))
            echo = echo.split("b'")[1]
            echo = echo.split("\\n'")[0]
            echoes.append(echo)
    return echoes

def get_files(dirname, ext):
    files = os.listdir(dirname)
    files.sort()
    list = []
    for name in files:
        if os.path.splitext(name)[1] == ext:
            list.append(name)
    return list

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt (Control-C)...")
    sys.exit()
