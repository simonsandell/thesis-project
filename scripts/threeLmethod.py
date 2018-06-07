import numpy as np
import settings
from analysis import threeL

MODEL = settings.model
SAVENAME = "combined"
JACK_N = 100

DATAFILES = [
    settings.datatables_path + "datatable_4combined3DXY.npy",
    settings.datatables_path + "datatable_8combined3DXY.npy",
    settings.datatables_path + "datatable_16combined3DXY.npy",
    settings.datatables_path + "datatable_32combined3DXY.npy",
    settings.datatables_path + "datatable_64combined3DXY.npy",
    settings.datatables_path + "datatable_128combined3DXY.npy"
]
JACKFILES = [
    settings.datatables_path + "jackknife/4combined.npy",
    settings.datatables_path + "jackknife/8combined.npy",
    settings.datatables_path + "jackknife/16combined.npy",
    settings.datatables_path + "jackknife/32combined.npy",
    settings.datatables_path + "jackknife/64combined.npy",
    settings.datatables_path + "jackknife/128combined.npy"
]

for i, f in enumerate(DATAFILES):
    DATAFILES[i] = np.load(f)
    JACKFILES[i] = np.loaf(JACKFILES[i])

result = np.empty(
for d1, d2, d3 in zip(DATAFILES[:-2], DATAFILES[1:-1], DATAFILES[2:]):
    result.append(threeL.threeLmethod(d1, d2, d3, MODEL, SAVENAME))
for j1, j2, j3 in zip(JACKFILES[:-1], JACKFILES[1:-1], JACKFILES[2:]):
    for i in range(JACK_N):
        
