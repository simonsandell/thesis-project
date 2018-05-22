import numpy as np
import settings
import threeL

savename = "ts";
model = "3DXY";

datafiles = [settings.pickles_path+model+"ts_4.npy",
settings.pickles_path+model+"ts_8.npy",
settings.pickles_path+model+"ts_16.npy",
settings.pickles_path+model+"ts_32.npy",
settings.pickles_path+model+"ts_64.npy",
settings.pickles_path+model+"ts_128.npy"];
for i,f in enumerate(datafiles):
    datafiles[i] = np.load(f);

for d1,d2,d3 in zip(datafiles[:-2],datafiles[1:-1],datafiles[2:]):
    threeL.threeLmethod(d1,d2,d3,model,savename);

