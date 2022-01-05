"""
This is a basic demonstration of CUARS using Adafruit CircuitPython to
show the display on PiTFT display hardware. It's designed for display
boards that have at least 2 buttons. It uses Python modules 'os' and
'sys' to perform basic navigation and operations, as well as to load
specialized modules for custom displays configurations.
"""
import os
import sys
#import subprocess
import time

import adargb
import cuars

io = adargb.BoardIO()
display = adargb.Display(135, 240)

def main():
    interf = cuars.Table(240, 135)
    mark = 0
    print("Interface should appear on the RGB display now")
    while True:
        dirname = os.getcwd()
        if os.path.isdir(dirname):
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
            print("cd home")
            os.chdir(os.path.expanduser("~"))
        elif io.B.value and not io.A.value:  # button 1 pressed
            mark = (mark+1) % len(dirlist)
        elif io.A.value and not io.B.value:  # button 2 pressed
            path = os.path.join(dirname, dirlist[mark])
            if os.path.isdir(path):
                print("cd: " + path)
                os.chdir(path)
                mark = 0
            else:
                print("not a directory: " + path)
        # Wait for refresh
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt (Control-C)...")
    io.backlight.value = not io.backlight.value
    sys.exit()

