import numpy as np
import matplotlib.pyplot as plt
import settings
from analysis import intersectionFinder


# load binder from datatables
DT_LIST = [
#    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]
PLOT_DURING = False
QUANT_IDX = 22


def closeness(omega, b_range, quant_idx=QUANT_IDX):
    temp_num = DT_LIST[0][:, 0].shape[0]
    close_vs_b = np.empty((b_range.shape[0], 2))

    for b_idx, B in enumerate(b_range):
        if PLOT_DURING:
            plt.figure(figsize=(18, 8))
            plt.title("omega = " + str(omega) + " b = " + str(B))
            plt.xlabel("Temperature")
            plt.ylabel(r"B - b*L^{-omega}")
        lines = np.empty((len(DT_LIST), 2, temp_num))

        for i, DT in enumerate(DT_LIST):
            Y = DT[:, quant_idx]
            Y = Y - np.ones(Y.shape) * (B * pow(DT[0, 0], -OMEGA))

            if PLOT_DURING:
                plt.errorbar(
                    DT[:, 1], Y, yerr=DT[:, quant_idx + 30], label=str(DT[0, 0])
                )
            lines[i, 0, :] = DT[:, 1]
            lines[i, 1, :] = Y[:]
        ints = []
        ints[:] = []

        for i in range(0, lines.shape[0] - 1):
            x = lines[i, 0, :]
            y1 = lines[i, 1, :]
            y2 = lines[i + 1, 1, :]
            current_intersection = intersectionFinder.findIntersection(x, y1, y2)

            if current_intersection.any():
                ints.append(current_intersection)

        if len(ints) > 1:
            close_vs_b[b_idx, :] = [B, intersectionFinder.findCloseness(ints)[0]]

            if PLOT_DURING:
                asdf = np.squeeze(np.array(ints))
                plt.scatter(asdf[:, 0], asdf[:, 1], marker="x")
        else:
            close_vs_b[b_idx, :] = [np.nan, np.nan]

        if PLOT_DURING:
            plt.figlegend()
            plt.show(block=True)

    return close_vs_b


# ansatz : B - bL^{-omega} = a
OMEGA = 0.78
B_RANGE = np.linspace(-0.200, -0.05, 500)
omega_best_res = closeness(OMEGA, B_RANGE)

OMEGA = 1
omega_one_res = closeness(OMEGA, B_RANGE)

OMEGA = 1.2
omega_two_res = closeness(OMEGA, B_RANGE)

plt.figure(figsize=(18, 8))
plt.title("closeness of intersection points")
plt.xlabel("b")
plt.ylabel("closeness")
plt.plot(omega_best_res[:, 0], omega_best_res[:, 1], "rx", label="omega = 0.78")
plt.plot(omega_one_res[:, 0], omega_one_res[:, 1], "bx", label="omega = 1")
plt.plot(omega_two_res[:, 0], omega_two_res[:, 1], "gx", label="omega = 1.2")
plt.figlegend()
plt.show(block=False)

one_min_b = omega_one_res[np.nanargmin(omega_one_res[:, 1])][0]
best_min_b = omega_best_res[np.nanargmin(omega_best_res[:, 1])][0]

PLOT_DURING = True
closeness(0.78, np.linspace(best_min_b * 0.9, best_min_b * 1.1, 3))
closeness(1, np.linspace(one_min_b * 0.9, one_min_b * 1.1, 3))
input()
