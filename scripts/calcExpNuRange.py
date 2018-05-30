import subprocess

orange = [0.6,0.61,0.62];
nrange = [0,1,2,3];
for o in orange:
    for n in nrange:
        subprocess.Popen(["python3","calcExponent.py",str(o),str(n)]);
