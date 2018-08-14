import subprocess

#for i,mn,mx in zip([2, 3], [40, 50], [80, 80]):
for i,mn,mx in zip([0, 1, 2, 3], [0, 0, 40, 50], [100, 100, 80, 80]):
    subprocess.call(["python3", "./omega_from_two_l.py", str(i), str(mn), str(mx)])
