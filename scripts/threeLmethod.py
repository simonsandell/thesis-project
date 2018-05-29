import numpy as np
import settings
from analysis import threeL

model = settings.model;
savename = "combined_reduced";

datafiles = [
settings.pickles_path+"4"+savename+".npy",
settings.pickles_path+"8"+savename+".npy",
settings.pickles_path+"16"+savename+".npy",
settings.pickles_path+"32"+savename+".npy",
settings.pickles_path+"64"+savename+".npy",
settings.pickles_path+"128"+savename+".npy"];

for i,f in enumerate(datafiles):
    datafiles[i] = np.load(f);

for d1,d2,d3 in zip(datafiles[:-2],datafiles[1:-1],datafiles[2:]):
    threeL.threeLmethod(d1,d2,d3,model,savename);

