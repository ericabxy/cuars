#!/usr/bin/env python
import platform

info = platform.uname()
print("Name: " + info.node)
print("OS: " + info.system)
print("Release: " + info.release)
print("Version: " + info.version)
print("Arch: " + info.machine)
