import numpy as np

import settings
from analysis import threeL
from plotting import fileWriter

MODEL = settings.model
SAVENAME = "jun_26"
JACK_N = 500

CURFOLDER = "June_26_2018/"

DATAFILES = [
    settings.datatables_path + CURFOLDER + "datatable_4.0jun_153DXY.npy",
    settings.datatables_path + CURFOLDER + "datatable_8.0jun_153DXY.npy",
    settings.datatables_path + CURFOLDER + "datatable_16.0jun_153DXY.npy",
    settings.datatables_path + CURFOLDER + "datatable_32.0jun_263DXY.npy",
    settings.datatables_path + CURFOLDER + "datatable_64.0jun_263DXY.npy",
    settings.datatables_path + CURFOLDER + "datatable_128.0jun_263DXY.npy"
]

JACKFILES = [
    settings.datatables_path + CURFOLDER + "jackknife/4combined_nf.npy",
    settings.datatables_path + CURFOLDER + "jackknife/8combined_nf.npy",
    settings.datatables_path + CURFOLDER + "jackknife/16combined_nf.npy",
    settings.datatables_path + CURFOLDER + "jackknife/32combined_nf.npy",
    settings.datatables_path + CURFOLDER + "jackknife/64combined_nf.npy",
    settings.datatables_path + CURFOLDER + "jackknife/128combined_nf.npy"
]

for i, f in enumerate(DATAFILES):
    DATAFILES[i] = np.load(f)
    JACKFILES[i] = np.load(JACKFILES[i])

RESULT = []

for i, (d1, d2, d3) in enumerate(zip(DATAFILES[:-2], DATAFILES[1:-1], DATAFILES[2:])):
    RESULT.append(threeL.threeLmethod(d1, d2, d3))
    for temp_res in RESULT[i]:
        temp_res.append(d1[0, 29] + d2[0, 29] + d3[0, 29])
RESULT = np.array(RESULT)
print(RESULT.shape)
J_RESULT = []

for ind, (j1, j2, j3) in enumerate(zip(JACKFILES[:-1], JACKFILES[1:-1], JACKFILES[2:])):
    J_RESULT.append([])

    for i in range(JACK_N):
        J_RESULT[ind].append(threeL.threeLmethod(
            j1[i,: , :], j2[i, :, :], j3[i, :, :]
            ))
J_RESULT = np.array(J_RESULT)
print(J_RESULT.shape)

FINAL_RESULT = np.empty((RESULT.shape[0], RESULT.shape[1], RESULT.shape[2] + 2))

for line in range(J_RESULT.shape[0]):
    deltas = np.empty((RESULT.shape[1], 2))
    for temp in range(J_RESULT.shape[2]):
        delta_bin = np.sqrt(J_RESULT.shape[1]-1)*np.std(J_RESULT[line, :, temp, 1])
        delta_rs = np.sqrt(J_RESULT.shape[1]-1)*np.std(J_RESULT[line, :, temp, 2])
        deltas[temp, :] = [delta_bin, delta_rs]
    res_plus_del = np.append(RESULT[line, :, :], deltas, axis=1)
    FINAL_RESULT[line, :, :] = res_plus_del

for line in range(FINAL_RESULT.shape[0]):
    l1 = str(int(FINAL_RESULT[line, 0, 3]))
    binpath = settings.foutput_path + settings.model + "/threeL/bin/" + l1 + SAVENAME + ".dat"
    rspath = settings.foutput_path + settings.model + "/threeL/rs/" + l1 + SAVENAME + ".dat"
    fileWriter.writeQuant(binpath, FINAL_RESULT[line, :, :], [0, 1, 7, 6])
    fileWriter.writeQuant(rspath, FINAL_RESULT[line, :, :], [0, 2, 8, 6])
