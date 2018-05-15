import numpy as np
import sys

fName = sys.argv[1];
model = sys.argv[2];
datatable = np.load("./pickles/datatable_"+fName+model+".npy");
