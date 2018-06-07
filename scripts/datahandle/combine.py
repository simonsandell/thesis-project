import os
import numpy as np

data = np.empty((0, 29))
for filename in os.listdir("."):
    if ".npy" in filename:
        dt = np.load("./" + filename)
        data = np.append(data, dt, axis=0)
pwd = os.path.abspath(os.curdir).split("/")[-1]
np.save("../" + pwd + "combined", data)
