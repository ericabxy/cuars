#!/usr/bin/env python3
import os
import sys
import subprocess
import time

import digitalio
import board
import adafruit_rgb_display.st7789 as st7789

import cuars

def main():
    io = BoardIO()
    display = Display(135, 240)
    interf = cuars.Interface(240, 135)
    mark = -1
    print("Interface should appear on the RGB display now")
    while True:
        dirname = len(sys.argv) > 1 and sys.argv[1] or os.getcwd()
        if os.path.isfile(os.path.join(dirname, "console.ini")):
            lines = cuars.get_echoes(dirname)
            name = os.path.basename(dirname)
#            interf.set_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            interf.bd = interf.palette[0]
            interf.tb = interf.palette[5]
            interf.name = lines.pop(0)
            interf.show_text(lines, (1, 2, 3, 4))
        else:
            files = cuars.get_directory(dirname)
            interf.show_directory(dirname, files)
        # Display image.
        image = interf.image
        display.show(image, 270)
        # Accept input
        if io.B.value and not io.A.value:  # button 1 pressed
            mark = (mark+1) % 6
        if io.A.value and not io.B.value:  # button 2 pressed
            pass
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt (Control-C)...")
    sys.exit()
