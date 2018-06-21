import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import settings
from analysis import twoLomega
from analysis import intersectionFinder



DATLIST = [
    #np.load(settings.pickles_path + "2Lquant/jun_184_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_188_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1816_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1832_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1864_128.npy"),
]

# for range of omega, resultcale and find intersection between sequentially larger system sizes
OMEGA_RANGE = np.linspace(0.6, 0.9, 300)
RESULT = np.empty((OMEGA_RANGE.shape[0], len(DATLIST)-1, 5))

for size_idx, (q1, q2) in enumerate(zip(DATLIST[:-1], DATLIST[1:])):
    for om_idx, omega in enumerate(OMEGA_RANGE):
        bothresult = twoLomega.intersections_for_given_omega(q1, q2, omega)
        temp_bin, temp_rho = bothresult[0], bothresult[1]
        RESULT[om_idx, size_idx, :] = [omega, *temp_bin, *temp_rho]


# calculate intersection closeness
bin_close_result = np.empty((0,4))
rho_close_result = np.empty((0,4))

for om_idx, omega in enumerate(OMEGA_RANGE):
    #prune nan's
    bin_pts_X = RESULT[om_idx, :, 1]
    bin_pts_Y = RESULT[om_idx, :, 2]

    rho_pts_X = RESULT[om_idx, :, 3]
    rho_pts_Y = RESULT[om_idx, :, 4]

    bin_pruned = []
    bin_pruned[:] = []

    rho_pruned = []
    rho_pruned[:] = []
    for size_idx in range(bin_pts_X.shape[0]):
        if not np.isnan(bin_pts_X[size_idx]):
            bin_pruned.append([bin_pts_X[size_idx], bin_pts_Y[size_idx]])

        if not np.isnan(rho_pts_X[size_idx]):
            rho_pruned.append([rho_pts_X[size_idx], rho_pts_Y[size_idx]])

    if len(bin_pruned) > 2:
        close_bin = intersectionFinder.findCloseness([bin_pruned])
        row = np.array([[omega, *close_bin]])
        bin_close_result = np.append(bin_close_result, row, axis=0)
    if len(rho_pruned) > 2:
        close_rho = intersectionFinder.findCloseness([rho_pruned])
        row =np.array([[omega, *close_rho]])
        rho_close_result = np.append(rho_close_result, row, axis=0)
### werid 3d plot
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot(bin_close_result[:, 0], bin_close_result[:,1], zs=bin_close_result[:, 2])
#ax.plot(rho_close_result[:,0],rho_close_result[:,1], zs=rho_close_result[:, 2])
#ax.set_xlabel('omega')
#ax.set_ylabel('closeness')
#ax.set_zlabel('Tc')
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(bin_close_result[:, 0], bin_close_result[:, 1], label='binder')
ax1.plot(rho_close_result[:,0],rho_close_result[:,1], label='rho')
ax2.plot(bin_close_result[:, 0], bin_close_result[:, 2], label='binder')
ax2.plot(rho_close_result[:,0],rho_close_result[:,2], label='rho')
plt.figlegend()
plt.show(block=False)
input()
