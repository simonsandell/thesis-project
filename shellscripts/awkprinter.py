import subprocess
import os
import sys

for filename in os.listdir("./"):
    if ".txt" in filename:
        command = 'awk -F \"    \" \'{print $1, $2, $' + sys.argv[1] + '}\' ' + filename
        subprocess.call(command,shell=True)
        
