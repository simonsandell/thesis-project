import subprocess

analysis_list = [
        "three_l_method.py",
        "two_l_method.py",
        "calcExpRange.py",
        ]
for a in analysis_list:
    subprocess.call(['python3', a])

