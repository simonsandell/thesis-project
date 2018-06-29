import numpy as np
import settings
from analysis import jackknife

# returns avgerage magnetization
def calc_mag(mat):
    return [np.mean(mat[:, 9]) / np.mean(mat[:, 21])]


def get_mag_and_delta(mat):
    avgM = calc_mag(mat)[0]
    Jackknife_estimates = jackknife.jackknife(mat, calc_mag, 1, 500)
    delM = np.sqrt(Jackknife_estimates.shape[0] - 1) * np.std(Jackknife_estimates)
    return [avgM, delM]


# now we have data for only interesting temp, separete N_sweeps and print
def do_nsweep_binning(mat, openfile):
    startI = 0
    high_N = 4.0
    avgPrev = 0.0
    avgCurr = 0.0

    for i in range(mat.shape[0]):
        # increase index until Nsweeps is higher than next cutoff
        if mat[i, 4] > high_N:
            # calculate mean Nsweeps of current bin
            avgCurr = np.mean(mat[startI:i, 4])
            avg_mag, delta_mag = get_mag_and_delta(mat[startI:i], openfile, 0.5 * (avgCurr + avgPrev))
            avgPrev = avgCurr
            high_N = high_N * 2
            startI = i
    avgCurr = np.mean(mat[startI:, 4])
    writeLine(mat[startI:, :], openfile, 0.5 * (avgCurr + avgPrev))
# load all teq data
all_data = np.load(settings.pickles_path + 'equilibration_t_2.202.npy')

# separate cold and warm
sort_ind = np.lexsort((all_data[:, 0], all_data[:, 6]))
all_data = all_data[sort_ind]

coldstart, cold_ind = np.unique(all_data[:, 6], return_index=True)
cold_data = all_data[cold_ind[1]:, :]
warm_data = all_data[:cold_ind[1], :]

# sort by system size
cold_lval, cold_lind = np.unique(cold_data[:, 0], return_index=True)
warm_lval, warm_lind = np.unique(warm_data[:, 0], return_index=True)
cold_lind.append(cold_data.shape[0])
warm_lind.append(warm_data.shape[0])

# do Nsweeps binning and calculate avgM deltaM for each system size
for idx1, idx2 in zip(cold_lind[:-1],cold_lind[1:]):
