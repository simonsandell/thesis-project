"""
heres your goddamn docstring
"""
import numpy as np

import settings
from plotting import fileWriter
from analysis import twoLana

# from analysis import twoLomegaVsGood


MODEL = settings.model
DTSET = "June_18_2018"
TAG = "jun_18"

DATAFILES = [
    settings.datatables_path + DTSET + "/datatable_4.0jun_153DXY.npy",
    settings.datatables_path + DTSET + "/datatable_8.0jun_153DXY.npy",
    settings.datatables_path + DTSET + "/datatable_16.0jun_153DXY.npy",
    settings.datatables_path + DTSET + "/datatable_32.0jun_153DXY.npy",
    settings.datatables_path + DTSET + "/datatable_64.0jun_153DXY.npy",
    settings.datatables_path + DTSET + "/datatable_128.0jun_153DXY.npy",
]
JACKFILES = [
    settings.datatables_path + DTSET + "/jackknife/4combined.npy",
    settings.datatables_path + DTSET + "/jackknife/8combined.npy",
    settings.datatables_path + DTSET + "/jackknife/16combined.npy",
    settings.datatables_path + DTSET + "/jackknife/32combined.npy",
    settings.datatables_path + DTSET + "/jackknife/64combined.npy",
    settings.datatables_path + DTSET + "/jackknife/128combined.npy",
]

# calculate the quantities, plain
N_TEMPS = 101
JACK_NUM = 500
TWO_L_QUANT = np.empty((len(DATAFILES) - 1, N_TEMPS, 7))

for index, data1, data2 in zip(
        range(len(DATAFILES) - 1), DATAFILES[:-1], DATAFILES[1:]
):
    TWO_L_QUANT[index, :, :5] = twoLana.twoLomega(np.load(data1), np.load(data2))
    # jackknifing
    j_data = np.load(JACKFILES[index])
    j_data_2 = np.load(JACKFILES[index + 1])
    j_data = j_data[j_data[:, 1].argsort()]
    j_data_2 = j_data_2[j_data_2[:, 1].argsort()]
    j_result = []
    j_result[:] = []

    for i in range(JACK_NUM):
        j_result.append(
            twoLana.twoLomega(j_data[i::JACK_NUM, :], j_data_2[i::JACK_NUM, :])
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


## calculate how close intersections are for each omega and save to xmgrace file
# twoLomegaVsGood.twoLintersectionCloseness(bres, "bin", savename+"bind_good")
# twoLomegaVsGood.twoLintersectionCloseness(rres, "rs", savename+"rho_good")
## skipping smallest, do it again
# bres_ds = twoLomega.removeSmallestSize(bres)
# rres_ds = twoLomega.removeSmallestSize(rres)
# twoLomegaVsGood.twoLintersectionCloseness(bres_ds, "bin", savename+"_ds_bind_good")
# twoLomegaVsGood.twoLintersectionCloseness(rres_ds, "rs", savename+"_ds_rho_good")
