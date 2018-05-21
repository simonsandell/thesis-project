import numpy as np
import os
import sys
import fileWriter

def getIntersections(view):
    res = np.empty((0,view.shape[1])); 
    for x in range(view.shape[0]):
        if !(np.isnan(view[x,1])):
            res.append(view[x,:]);
    return res;
def getCloseness(ints):
    avgx = np.mean(ints[:,1]);
    avgy = np.mean(ints[:,2]);
    o = np.ones(np[:,0].shape);
    dx = np[:,1] - o*avgx;
    dy = np[:,2] - o*avgx;
    dist = np.pow(dx,o*2) + np.pow(dy,o*2);
    res = np.mean(dist);
    return res;

# format;
# omega, int_x, int_y, L1, L2
#     0     1     2   3   4


filename = sys.argv[1];
model = sys.argv[2];
savename = sys.argv[3];
dat = np.empty((0,9));
for filename in os.listdir(dirname):
    ld = np.load(filename);
    dat = np.append(dat,ld,axis=0);
dat = dat[dat[:,0].argsort()];

ov,oi = np.unique(dat[:,0],return_index=True);
oi = np.append(oi,dat.shape[0]);

result = [];
for i1,i2 in zip(oi[:-1],oi[1:]):
    omview = dat[i1:i2,:];
    ints = getIntersections(omview);

    if (len(ints)>2):
        closeness = getCloseness(ints);
        result.append([ov[i1],closeness]);
print(result)
fileWriter.writeOmegaVsClose(savename,model,result);


