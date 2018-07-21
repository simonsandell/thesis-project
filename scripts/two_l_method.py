import numpy as np

import settings
from plotting import fileWriter
from analysis import twoLana

# from analysis import twoLomegaVsGood


MODEL = settings.model
TAG = settings.TAG

DATAFILES = [
    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]
JACKFILES = [
    np.load(settings.JACKTABLES[0]),
    np.load(settings.JACKTABLES[1]),
    np.load(settings.JACKTABLES[2]),
    np.load(settings.JACKTABLES[3]),
    np.load(settings.JACKTABLES[4]),
    np.load(settings.JACKTABLES[5]),
]

# calculate the quantities, plain
N_TEMPS = JACKFILES[0].shape[1]
JACK_NUM = JACKFILES[0].shape[0]
print('N_TEMPS', N_TEMPS)
print('JACK_NUM', JACK_NUM)

TWO_L_QUANT = np.empty((len(DATAFILES) - 1, N_TEMPS, 7))

for index in range(len(DATAFILES) - 1):
    data1 = DATAFILES[index]
    data2 = DATAFILES[index+1]
    TWO_L_QUANT[index, :, :5] = twoLana.twoLomega(data1, data2)
    # jackknifing
    j_data = JACKFILES[index]
    j_data_2 = JACKFILES[index + 1]

    j_result = []
    j_result[:] = []

    for j_idx in range(JACK_NUM):
        j_result.append(
            twoLana.twoLomega(j_data[j_idx, :, :], j_data_2[j_idx, :, :])
        )

    j_result = np.array(j_result)
    np.save(
        settings.pickles_path
        + "/2Lquant/jackknife/jack_"
        + TAG
        + str(int(j_result[0, 0, 0]))
        + "_"
        + str(int(j_result[0, 0, 1])),
        j_result,
    )
    bin_delta = np.empty(N_TEMPS)
    rs_delta = np.empty(N_TEMPS)

    for i in range(N_TEMPS):
        bin_delta[i] = np.sqrt(JACK_NUM - 1) * (np.std(j_result[:, i, 3]))
        rs_delta[i] = np.sqrt(JACK_NUM - 1) * (np.std(j_result[:, i, 4]))
    TWO_L_QUANT[index, :, 5] = bin_delta
    TWO_L_QUANT[index, :, 6] = rs_delta

# TWO_L_QUANT dims = (DATAFILES,temps, quantities)
# TWO_L_QUANT format = [l1 , l2, t, b, rs, db, drs]

for i in range(len(DATAFILES) - 1):
    # save to npy
    np.save(
        settings.pickles_path
        + "/2Lquant/"
        + TAG
        + str(int(TWO_L_QUANT[i, 0, 0]))
        + "_"
        + str(int(TWO_L_QUANT[i, 0, 1])),
        TWO_L_QUANT[i, :, :],
    )
    fileWriter.writeQuant(
        settings.foutput_path
        + settings.model
        + "/twoL/bin/"
        + TAG
        + "_"
        + str(TWO_L_QUANT[i, 0, 0])
        + "_"
        + str(TWO_L_QUANT[i, 0, 1])
        + ".dat",
        TWO_L_QUANT[i, :, :],
        [2, 3, 5, 0],
    )
    fileWriter.writeQuant(
        settings.foutput_path
        + settings.model
        + "/twoL/rs/"
        + TAG
        + "_"
        + str(TWO_L_QUANT[i, 0, 0])
        + "_"
        + str(TWO_L_QUANT[i, 0, 1])
        + ".dat",
        TWO_L_QUANT[i, :, :],
        [2, 4, 6, 0],
    )
