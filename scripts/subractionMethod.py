import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import settings
from plotting import fileWriter
#
#A_r_guess = 1.115775
#A_b_guess = 1.24805

DATLIST = [
    np.load(settings.datatables_path + "June_18_2018/datatable_4.0jun_153DXY.npy"),
    np.load(settings.datatables_path + "June_18_2018/datatable_8.0jun_153DXY.npy"),
    np.load(settings.datatables_path + "June_18_2018/datatable_16.0jun_153DXY.npy"),
    np.load(settings.datatables_path + "June_18_2018/datatable_32.0jun_153DXY.npy"),
    np.load(settings.datatables_path + "June_18_2018/datatable_64.0jun_153DXY.npy"),
    np.load(settings.datatables_path + "June_18_2018/datatable_128.0jun_153DXY.npy"),
]
JACKLIST = [
    np.load(settings.datatables_path + "June_18_2018/jackknife/4combined_nf.npy"),
    np.load(settings.datatables_path + "June_18_2018/jackknife/8combined_nf.npy"),
    np.load(settings.datatables_path + "June_18_2018/jackknife/16combined_nf.npy"),
    np.load(settings.datatables_path + "June_18_2018/jackknife/32combined_nf.npy"),
    np.load(settings.datatables_path + "June_18_2018/jackknife/64combined_nf.npy"),
    np.load(settings.datatables_path + "June_18_2018/jackknife/128combined_nf.npy"),
]

# prune T's
for DAT in DATLIST:
    DAT = DAT[50:76, :]
for JDAT in JACKLIST:
    JDAT = JDAT[:, 50:76, :]


for a_const in np.linspace(1.1,1.3,10):
    for t_idx in range(DATLIST[0].shape[0]):

