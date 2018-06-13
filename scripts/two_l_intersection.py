import numpy as np

from analysis import intersectionFinder
import settings

NAMELIST = [
    settings.pickles_path + "2Lquant/jun_114_8.npy",
    settings.pickles_path + "2Lquant/jun_118_16.npy",
    settings.pickles_path + "2Lquant/jun_1116_32.npy",
    settings.pickles_path + "2Lquant/jun_1132_64.npy",
    settings.pickles_path + "2Lquant/jun_1164_128.npy",
]
JACKLIST = [
    settings.pickles_path + "2Lquant/jackknife/jack_jun_114_8.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_118_16.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1116_32.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1132_64.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1164_128.npy"
] 
