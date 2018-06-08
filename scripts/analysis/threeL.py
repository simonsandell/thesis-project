import sys
import numpy as np


def get_bin(mag2, mag4, exp):
    return mag4 * exp / (mag2 * mag2)


def get_rho_s(e, sx, sy, sz, exp, L, T):
    rho_s = -L * e - (L * L * L * L / T) * (sx + sy + sz)
    rho_s = rho_s / (3.0 * exp)

    return rho_s


def calc_omega_func(view1, view2, view3):
    temp = view1[1]
    size_1 = view1[0]
    size_2 = view2[0]
    size_3 = view3[0]
    bin_1 = get_bin(view1[10], view1[11], view1[21])
    bin_2 = get_bin(view2[10], view2[11], view2[21])
    bin_3 = get_bin(view3[10], view3[11], view3[21])
    rho_1 = get_rho_s(
        view1[7], view1[14], view1[15], view1[16],
        view1[21], size_1, temp
    )
    rho_2 = get_rho_s(
        view2[7], view2[14], view2[15], view2[16],
        view2[21], size_2, temp
    )
    rho_3 = get_rho_s(
        view3[7], view3[14], view3[15], view3[16],
        view3[21], size_3, temp
    )

    omegabin = -np.log((bin_3 - bin_2) / (bin_2 - bin_1))
    omegarho = -np.log((rho_3 - rho_2) / (rho_2 - rho_1))

    return [omegabin, omegarho]


# produce [T, omegabin, omegarho, L1, L2, L3]
def calculate_three_l_quant(view1, view2, view3):
    omegabin, omegarho = calc_omega_func(view1, view2, view3)
    temp = view1[1]
    size_1 = view1[0]
    size_2 = view2[0]
    size_3 = view3[0]
    return [temp, omegabin, omegarho, size_1, size_2, size_3]

# take datatables
def threeLmethod(data1, data2, data3):
    # sort by temperature
    data1 = data1[data1[:, 1].argsort()]
    data2 = data2[data2[:, 1].argsort()]
    data3 = data3[data3[:, 1].argsort()]
    l1, l2, l3 = data1[0, 0], data2[0, 0], data3[0, 0]

    if not ((l2 == 2*l1) and (l3 == 2*l2)):
        print(l1, l2, l2)
        print("not factors of 2")
        sys.exit(1)

    result = []

    for i in range(data1.shape[0]):
        result.append(calculate_three_l_quant(data1[i, :], data2[i, :], data3[i, :]))

    return result
