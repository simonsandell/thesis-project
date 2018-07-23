import subprocess

import settings


FILELIST = settings.DATATABLES
for f in FILELIST:
    subprocess.call(
        [
            "python3",
            settings.scripts_path + "one_l_ana.py",
            settings.pickles_path + f,
        ]
    )
