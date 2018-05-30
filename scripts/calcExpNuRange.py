import subprocess

orange = [0.62];
nrange = [0,1,2,3];
for o in orange:
    for n in nrange:
        subprocess.call(["python3","calcExponent.py",str(o),str(n)]);
