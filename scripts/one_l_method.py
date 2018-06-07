"""
stupid docstring
"""
import subprocess

import settings


FILELIST = []
TAG = ""
for f in FILELIST:
    subprocess.call(
        [
            "python3",
            settings.scripts_path + "oneLana.py",
            settings.pickles_path + f,
            TAG,
        ]
    )
