import numpy as np
import settings
import threeL

savename = "ts";
model = "3DXY";

datafiles = [
settings.pickles_path+"4combined_reduced.npy",
settings.pickles_path+"8combined_reduced.npy",
settings.pickles_path+"16combined_reduced.npy",
settings.pickles_path+"32combined_reduced.npy",
settings.pickles_path+"64combined_reduced.npy",
settings.pickles_path+"128combined_reduced.npy"];
for i,f in enumerate(datafiles):
    datafiles[i] = np.load(f);

for d1,d2,d3 in zip(datafiles[:-2],datafiles[1:-1],datafiles[2:]):
    threeL.threeLmethod(d1,d2,d3,model,savename);

