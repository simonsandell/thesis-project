import subprocess

for i in [0, 1, 2, 3]:
    print(i)
    subprocess.call(["python3", "./omega_from_two_l.py", str(i)])
