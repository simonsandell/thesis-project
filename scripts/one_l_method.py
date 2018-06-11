"""
stupid docstring
"""
import subprocess

import settings


FILELIST = [
    settings.datatables_path + "jun_5_2018/datatable_4combined3DXY.npy",
    settings.datatables_path + "jun_5_2018/datatable_8combined3DXY.npy",
    settings.datatables_path + "jun_5_2018/datatable_16combined3DXY.npy",
    settings.datatables_path + "jun_5_2018/datatable_32combined3DXY.npy",
    settings.datatables_path + "jun_5_2018/datatable_64combined3DXY.npy",
    settings.datatables_path + "jun_5_2018/datatable_128combined3DXY.npy",
]
TAG = "jun5"
for f in FILELIST:
    subprocess.call(
        [
            "python3",
            settings.scripts_path + "oneLana.py",
            settings.pickles_path + f,
            TAG,
        ]
    )
