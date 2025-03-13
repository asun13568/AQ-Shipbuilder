import os
import pathlib as Path
import shutil

with open("completed.txt", 'r') as f:
    thing = f.read()

for item in thing:
    path = Path.cwd(item)

path = os.path.join("ss", "completed", "we")