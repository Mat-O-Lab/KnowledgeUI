from operator import sub

import os
import sys
import subprocess

#Create a file to get the output from subprocess

filepath= "rawInfoAboutVirtualEnv.txt"
location = ""
print("Run: pip show -f virtualenv")

with open(filepath, "w") as outfile:
    subprocess.call('pip show -f virtualenv', shell=True, stdout=outfile)
    outfile.close()
 
with open(filepath, "r") as outfile:
    lines = outfile.readlines()
    for line in lines:
        temp = line.upper()
        if(temp.find("LOCATION") != -1):
            i = line.find(':') + 2
            j = line.rfind('\\') + 1
            location = line[i:j]
        elif (temp.find("VIRTUALENV.EXE") != -1):
            k = line.find('\\') + 1
            location = location.join(['',line[k:len(line)-1]])
    outfile.close()

if os.path.exists(filepath):
    os.remove(filepath)

print(f"""Path to the virtualenv: {location}""")
cmd = f"""{location} venv"""
subprocess.call(cmd, shell=True)
print("virtual env created")