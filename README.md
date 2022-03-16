# CUARS (Command Utility Access/Retrieval System)

A visual interface for computer filesystems and command-line utilities.

Each display is designed with a small border to convey pertinent meta 
information, a large area to display requested data, and touchable 
"buttons" to interact with the interface.

Milestone goals are as follows.

- navigate an entire file structure using the "Table" display
- read any text file with the "Text" display
- display the contents of any binary file with the "Bin" display
- launch, background, and terminate executable script files
- run special python modules to display data in a customized way

## Concept

CUARS uses standard Python libraries to navigate a filesystem and 
retrieve information about the files, computer, user, and processes. 
Functions that are not cross-platform are avoided. CUARS is like virtual 
terminal without a keyboard.

Functionality beyond basic file navigation and operation is provided by 
special submodules that start programs in the background and retrieve 
information to CUARS for display, accept input via buttons pressed in 
the CUARS interface, and terminate when told to.

## Requirements

Tkinter test modules require [Tkinter][1]. Direct rendering modules 
require [Pillow][2].

[1]: https://wiki.python.org/moin/TkInter
[2]: https://python-pillow.org/
