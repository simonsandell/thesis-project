import subprocess

import settings


FILELIST = settings.DATATABLES
TAG = settings.TAG
for f in FILELIST:
    subprocess.call(
        [
            "python3",
            settings.scripts_path + "one_l_ana.py",
            settings.pickles_path + f,
            TAG,
        ]
    )
