#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import board

import adafruit_rgb_display.st7789 as st7789
import digitalio
from PIL import Image, ImageDraw, ImageFont

import cuars

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
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
#rotation = 90
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
abspath = os.path.dirname(sys.argv[0])
#ifont = ImageFont.truetype(os.path.join(abspath, "ascii.ttf"), 24)
font = ImageFont.truetype("DejaVuSansCondensed.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

interf = cuars.Interface(240, 135)
#interf.set_palette("solarized")
#interf.set_scheme((0, 1, 0, 2, 0, 3, 0, 4))

while True:
    if buttonB.value and not buttonA.value:  # just button A pressed
        if backlight.value:
            player.next()
        else:
            player.minus()
    elif buttonA.value and not buttonB.value:  # just button B pressed
        if backlight.value:
            player.skip()
        else:
            player.plus()
    elif not buttonA.value and not buttonB.value:  # both pressed
        if backlight.value:
            backlight.value = False  # turn off backlight
        else:
            backlight.value = True  # turn on backlight

    # Get track playing information
    POS = player.get_pos(16, ' ', '_')
    TIME = player.get_time()
    VOL = "Volume: " + player.get_vol()
    ALB = player.get_alb()
    NAME = "\"" + player.get_name() + "\""
    ART = player.get_art()

    # Get the display interface
    image = interf.get_table(ART, (NAME, ALB, VOL, TIME))

    # Draw a black filled box to clear the image.
    '''draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Write four lines of text.
    y = height-font.getsize(POS)[1]
    draw.text((x, y), POS, font=font, fill="#FF00FF")
    draw.text((x, y), TIME, font=font, fill="#FF00FF")
    y -= font.getsize(VOL)[1]
    draw.text((x, y), VOL, font=font, fill="#0000FF")
    y -= font.getsize(ALB)[1]
    draw.text((x, y), ALB, font=font, fill="#FFFF00")
    y -= font.getsize(NAME)[1]
    draw.text((x, y), NAME, font=font, fill="#00FF00")
    y -= font.getsize(ART)[1]
    draw.text((x, y), ART, font=font, fill="#FFFFFF")

    # Draw the controls icons.
    draw.text((width-16, 0), chr(175), font=ifont, fill="#00FFFF")
    draw.text((width-16, (height/2)-12), chr(15), font=ifont, fill="#FFFF00")
    draw.text((width-16, height-24), chr(240), font=ifont, fill="#00FFFF")
    draw.rectangle((0, 0, 8, 8), outline=0, fill=0)'''

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.033)
