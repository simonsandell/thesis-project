import numpy as np

import settings
from plotting import fileWriter

FILES = [
    settings.datatables_path + "cputime/4_cputime_delta.npy",
    settings.datatables_path + "cputime/8_cputime_delta.npy",
    settings.datatables_path + "cputime/16_cputime_delta.npy",
    settings.datatables_path + "cputime/32_cputime_delta.npy"
]
TIMES = []
with open(settings.datatables_path + "cputime/time.txt", "r") as timefile:
    TIMES = timefile.readlines()
RESULT = []
for i, F in enumerate(FILES):
    data = np.load(F)
    delta = np.std(data[:, 9])/np.sqrt(data.shape[0]-1)
    size = data[0, 0]
    frac = float(TIMES[i])/data.shape[0] # get cpuhours per data_amount
    RESULT.append([size, frac, 0.0, delta, float(TIMES[i])])
RESULT = np.array(RESULT)
np.save(settings.datatables_path + "cputime/cputime", RESULT)
fileWriter.writeQuant(
    settings.foutput_path+settings.model+"/vsL/delta/cputime.dat",
    RESULT, [0, 1, 2, 3, 4]
    )
