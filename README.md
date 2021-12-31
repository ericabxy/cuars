# CUARS (Command Utility Access/Retrieval System)

A visual interface for computer filesystems and command-line utilities.

CUARS is designed for screens as small as 160x120 with either a touch
interface or a two-button interface. No keyboard or mouse required.


# Goals

- use standard Python libraries to gather general information about OS 
  and filesystem
- render a simple visual image representing the information, like a list 
  of files in a directory
- allow user to select and activate individual items in the image using
  buttons or a touch screen
- execute scripts, display image files, show text files


# Requirements

Requirements are still being worked out. Initially designed for a PiTFT 
display from Adafruit and their libraries. Requirement info below is 
likely outdated/innacurate.

CUARS requires Pillow, the friendly PIL fork.

> pip install pillow
