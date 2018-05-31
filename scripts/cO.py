import subprocess

for i in [0,1,2,3]:
    print(i)
    subprocess.call(["python3","./calculateOmega2L.py",str(i)]);
