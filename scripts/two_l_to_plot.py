from plotting import datatableToPlots
import settings


NAMELIST = [
    "4.0_8.0_2Lquant.npy",
    "8.0_16.0_2Lquant.npy",
    "16.0_32.0_2Lquant.npy",
    "32.0_64.0_2Lquant.npy",
    "64.0_128.0_2Lquant.npy",
]
for n in NAMELIST:
    datatableToPlots.twoLtoPlot(settings.pickles_path + n, n.rstrip(".npy"))
