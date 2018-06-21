import os
import numpy as np

data = np.empty((0, 29))
for filename in os.listdir("."):
    if ".npy" in filename:
        dt = np.load("./" + filename)
        data = np.append(data, dt, axis=0)

data = data[data[:,1].argsort()]
tval, tidx = np.unique(data[:, 1], return_index=True)
temp_num = 1
for ti in range(len(tval)-1):
    if abs(tval[ti+1] - tval[ti]) > 0.000001:
        temp_num += 1
jack_num = round(data.shape[0]/temp_num)
jdat = np.empty((jack_num, temp_num, 29))
print(jdat.shape)
print(data.shape)
for jidx in range(jack_num):
    jdat[jidx, :, :] = data[jidx::(jack_num), :]

pwd = os.path.abspath(os.curdir).split("/")[-1]
np.save("../" + pwd + "combined_nf", jdat)
