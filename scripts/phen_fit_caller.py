import subprocess

skips = [0, 1, 2, 3];
for s in skips:
    print(s)
    subprocess.call(['python3', './fit_binder_omega.py', str(s)])
