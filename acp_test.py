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
interf = cuars.Table(240, 135)

def main():
    mark = 0
    print("Interface should appear on the RGB display now")
    while True:
        dirname = os.getcwd()
        if os.path.isdir(dirname):
            dirlist = os.listdir(dirname)
            pattern = colorize(dirname, dirlist)
            s = interf.slice(dirlist, mark)
            interf.set_list(dirlist[s:])
            interf.set_pattern(pattern[s:])
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
                print("\nFile " + str(mark+1) + " of " + str(len(dirlist)))
                fileinfo(path)
        # Wait for refresh
        time.sleep(0.1)

def colorize(root, files):
    """Return a color codes from a list of files"""
    colors = []
    for name in files:
        path = os.path.join(root, name)
        if os.path.islink(path): colors.append(3)
        elif os.path.ismount(path): colors.append(4)
        elif os.path.isdir(path): colors.append(1)
        elif os.access(path, os.X_OK): colors.append(2)
        else: colors.append(7)
    return colors

def fileinfo(path):
    info = os.stat(path)
    print("Dirname: " + os.path.dirname(path))
    print("Basename: " + os.path.basename(path))
    print("Realpath: " + os.path.realpath(path))
    print("Stat")
    print("  Mode: " + str(info.st_mode))
    print("  Links: " + str(info.st_nlink))
    print("  User: " + str(info.st_uid))
    print("  Group: " + str(info.st_gid))
    print("  Size: " + str(info.st_size))
    print("  Accessed: " + time.ctime(info.st_atime))
    print("  Modified: " + time.ctime(info.st_mtime))
    print("Working: " + os.getcwd())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt (Control-C)...")
    io.backlight.value = not io.backlight.value
    sys.exit()

