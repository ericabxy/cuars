"""
This is a module designed to interact with CUARS and constuct highly
customized displays. This one will show system, login, and process
information for the current user.
"""
import platform

# print some system information
print("Operating System: " + platform.system())
print("Network Name: " + platform.node())
print("Release: " + platform.release())
print("Version: " + platform.version())
print("Machine Type: " + platform.machine())
print("Processor: " + platform.processor())
