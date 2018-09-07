import numpy as np
import matplotlib.pyplot as plt
import settings
from analysis import twoLomega
from analysis import intersectionFinder
from plotting import fileWriter

def prune_nan(not_pruned_X, not_pruned_Y):
    result = []
    for idx_size in range(not_pruned_X.shape[0]):
        if not np.isnan(not_pruned_X[idx_size]):
            result.append([not_pruned_X[idx_size], not_pruned_Y[idx_size]])
    return result

TAG = 'jul_26_final_zoom'
DATLIST = [
    np.load(settings.pickles_path + "2Lquant/jul_26_final4_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final8_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final16_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final32_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final64_128.npy"),
]
JACKLIST = [
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final4_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final8_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final16_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final32_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final64_128.npy"),
]

# for range of omega, rescale and find intersection between sequentially larger system sizes
OMEGA_RANGE = np.linspace(0.7, 0.9, 30)
RESULT = np.empty((OMEGA_RANGE.shape[0], len(DATLIST)-1, 5))
J_SIZE = JACKLIST[0].shape[0]
J_RESULT = np.empty((J_SIZE, OMEGA_RANGE.shape[0], len(DATLIST) - 1, 5))
print('rescaling and finding intersections')
for size_idx, (q1, q2) in enumerate(zip(DATLIST[:-1], DATLIST[1:])):
    print('size', size_idx,"/",len(DATLIST)-1)
    for om_idx, omega in enumerate(OMEGA_RANGE):
        print('omega',om_idx,"/",30) 
        bothresult = twoLomega.intersections_for_given_omega(q1, q2, omega)
        temp_bin, temp_rho = bothresult[0], bothresult[1]
        RESULT[om_idx, size_idx, :] = [omega, *temp_bin, *temp_rho]

        for j_idx in range(JACKLIST[0].shape[0]):
            jbres = twoLomega.intersections_for_given_omega(
                JACKLIST[size_idx][j_idx, :, :], JACKLIST[size_idx+1][j_idx, :, :], omega)
            temp_bin, temp_rho = jbres[0], jbres[1]
            J_RESULT[j_idx, om_idx, size_idx, :] = [omega, *temp_bin, *temp_rho]

# calculate intersection closeness
bin_close_result = np.empty((0, 7))
rho_close_result = np.empty((0, 7))
print('finding intersections')
for om_idx, omega in enumerate(OMEGA_RANGE):
    print(om_idx,"/",30)
    #prune nan's
    bin_pts_X = RESULT[om_idx, :, 1]
    bin_pts_Y = RESULT[om_idx, :, 2]
    rho_pts_X = RESULT[om_idx, :, 3]
    rho_pts_Y = RESULT[om_idx, :, 4]
    bin_pruned = prune_nan(bin_pts_X, bin_pts_Y)
    rho_pruned = prune_nan(rho_pts_X, rho_pts_Y)


    if len(bin_pruned) > 2:
        jbin_pruned = []
        jbin_pruned[:] = []
        j_res = []
        for j_idx in range(J_SIZE):
            jbin_pts_x = J_RESULT[j_idx, om_idx, :, 1]
            jbin_pts_y = J_RESULT[j_idx, om_idx, :, 2]
            jbin_pruned = prune_nan(jbin_pts_x, jbin_pts_y)
            if len(jbin_pruned) > 2:
                j_res.append(intersectionFinder.findCloseness([jbin_pruned]))
        j_res = np.array(j_res)
        j_res = [
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 0]),
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 1]),
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 2])
            ]
        close_bin = intersectionFinder.findCloseness([bin_pruned])
        row = np.array([[omega, *close_bin, *j_res]])
        bin_close_result = np.append(bin_close_result, row, axis=0)

    if len(rho_pruned) > 2:
        jrho_pruned = []
        jrho_pruned[:] = []
        j_res = []
        for j_idx in range(J_SIZE):
            jrho_pts_x = J_RESULT[j_idx, om_idx, :, 3]
            jrho_pts_y = J_RESULT[j_idx, om_idx, :, 4]
            jrho_pruned = prune_nan(jrho_pts_x, jrho_pts_y)
            if len(jrho_pruned) > 2:
                j_res.append(intersectionFinder.findCloseness([jrho_pruned]))
        j_res = np.array(j_res)
        j_res = [
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 0]),
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 1]),
            pow(j_res.shape[0], 0.5)*np.std(j_res[:, 2])
            ]
        close_rho = intersectionFinder.findCloseness([rho_pruned])
        row = np.array([[omega, *close_rho, *j_res]])
        rho_close_result = np.append(rho_close_result, row, axis=0)
### weird 3d plot
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot(bin_close_result[:, 0], bin_close_result[:,1], zs=bin_close_result[:, 2])
#ax.plot(rho_close_result[:,0],rho_close_result[:,1], zs=rho_close_result[:, 2])
#ax.set_xlabel('omega')
#ax.set_ylabel('closeness')
#ax.set_zlabel('Tc')
int_path = settings.foutput_path + settings.model+ "/twoL/intersection/"
tc_path = settings.foutput_path + settings.model + "/twoL/tc/"
fileWriter.writeQuant(int_path + TAG + "bin.dat", bin_close_result, [0, 1, 4])
fileWriter.writeQuant(int_path + TAG + "rho.dat", rho_close_result, [0, 1, 4])
fileWriter.writeQuant(tc_path + TAG + "bin.dat", bin_close_result, [0, 2, 5])
fileWriter.writeQuant(tc_path + TAG + "rho.dat", rho_close_result, [0, 2, 5])
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(bin_close_result[:, 0], bin_close_result[:, 1], label='binder')
ax1.plot(rho_close_result[:, 0], rho_close_result[:, 1], label='rho')
ax2.plot(bin_close_result[:, 0], bin_close_result[:, 2], label='binder')
ax2.plot(rho_close_result[:, 0], rho_close_result[:, 2], label='rho')
plt.figlegend()
plt.show(block=False)
input()
