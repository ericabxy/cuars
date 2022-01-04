# CUARS (Command Utility Access/Retrieval System)

A visual interface for computer filesystems and command-line utilities.

CUARS is a cross-platform computer interface with a simple, geometrical 
design and high-contrast colors. It is designed for screens as small as 
160x100 with a touch overlay or two generic buttons. No keyboard or 
mouse is required.

Each display is designed with a small border to convey pertinent meta 
information, a large area to display requested data, and touchable 
"buttons" to interact with the interface.

Milestone goals are as follows.

- freely navigate an entire directory structure starting at a specified 
  "root" directory
- choose text files from the interface and display for reading
- choose script files from the interface in order to launch, background, 
  and terminate processes
- choose special python modules to display custom data

# Requirements

Requirements are still being worked out. Initially designed for a PiTFT 
display from Adafruit and their libraries. Requirement info below is 
likely outdated/innacurate.

CUARS requires Pillow, the friendly PIL fork.

> pip install pillow

The Tkinter test module requires Tkinter.
