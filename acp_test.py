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
This is a basic demonstration of CUARS using Adafruit CircuitPython to
show the display on PiTFT display hardware. It's designed for display
boards that have at least 2 buttons. It uses Python modules 'os' and
'sys' to perform basic navigation and operations, as well as to load
specialized modules for custom displays configurations.
"""
import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont

from cuars import faces
import adargb

io = adargb.BoardIO()
display = adargb.Display(135, 240)

table = faces.Table(240, 135, os.listdir(os.getcwd()))
font = ImageFont.truetype("fonts/BebasNeue.otf", 22)
image = Image.new("RGB", (240, 135))
draw = ImageDraw.Draw(image)

def main():
    print("Interface should appear on the RGB display now")
    while True:
        # Display image.
        for badge in table.badges:
            rect = (badge.x, badge.y,
                    badge.x + badge.width, badge.y + badge.height)
            bgcolor, color = badge.bgcolor, badge.color
            name = badge.name
            draw.rectangle(rect, outline=bgcolor, fill=bgcolor)
            draw.text(rect, name, font=font, fill=color)
        display.show(image, 270)
        # Accept input
        if not io.B.value and not io.A.value:  # both buttons pressed
            print("restart")
        elif io.B.value and not io.A.value:  # button 1 pressed
            print("select")
        elif io.A.value and not io.B.value:  # button 2 pressed
            print("start")
        # Wait for refresh
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt (Control-C)...")
    io.backlight.value = not io.backlight.value
    sys.exit()
