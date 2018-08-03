import subprocess

skips = [0, 1, 2];
for s in skips:
    subprocess.call(['python3', './fit_binder_omega.py', str(s)])
