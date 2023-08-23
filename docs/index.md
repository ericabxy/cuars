Command Utility Access/Retrieval System
=======================================


Basic Purpose
-------------

At its most basic level, CUARS reads a filesystem using Python's `os` module
and presents it to the user in a window of specified size. The user has the
option to select the file, after which they can view or execute it. Files may
be viewed in ASCII or binary mode. CUARS thus provides a basic user interface
that can navigate a computer, view files, and execute scripts even when there
is no standard-size monitor present.


Advanced Purpose
----------------

CUARS will also provide a submodule format. If it detects that a file is a
Python submodule, it can load that submodule as an interface. The submodule
could, for example, control a music player backend while providing the user
with playback controls and media information.


Minimal User Interface
----------------------

CUARS is being designed for physical user interfaces that are typically
attached to embedded devices like Raspberry Pi and Beaglebone Black. It should
fit screens as small or smaller than 160x120 pixels. It will accept user
interaction from touch screens or even 2-button interfaces.


Inspiration
-----------

- LCARS: a cinematic fantasy computer user interface
- GNOME: a real open-source desktop environment
- GNU: a computer operating system based on UNIX


Example Interface Module
------------------------


Colors (Web)
------------

<ul>
<li class="badge">None</li>
<li class="badge blue">Blue</li>
<li class="badge green">Green</li>
<li class="badge cyan">Cyan</li>
<li class="badge red">Red</li>
<li class="badge magenta">Magenta</li>
<li class="badge yellow">Yellow</li>
<li class="badge white">White</li>
</ul>
