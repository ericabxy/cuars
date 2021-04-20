import datetime
import os
import re
import sys

import cuars

print("invocation: " + sys.argv[0])
print("cuars: creating interface")
inter = cuars.Interface(160, 120)
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    path = sys.argv[1]
else:
    path = os.getcwd()
print("cuars: displaying table of contents for " + path)
inter.draw_directory(path)
image = inter.image
isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
filename = "".join(re.split("-|T|:", isotime)) + ".example.png"
image.save(filename)
print("cuars: saved screenshot to " + filename)
