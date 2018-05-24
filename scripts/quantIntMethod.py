import numpy as np
import settings
from analysis import quantIntersection
from plotting import fileWriter

savename = input("savename: ");
model = input("model: ");
datalist =[
np.load(settings.root_path+"modular/datatables/combined/datatable_4combined3DXY.npy"),
np.load(settings.root_path+"modular/datatables/combined/datatable_8combined3DXY.npy"),
np.load(settings.root_path+"modular/datatables/combined/datatable_16combined3DXY.npy"),
np.load(settings.root_path+"modular/datatables/combined/datatable_32combined3DXY.npy"),
np.load(settings.root_path+"modular/datatables/combined/datatable_64combined3DXY.npy"),
np.load(settings.root_path+"modular/datatables/combined/datatable_128combined3DXY.npy")];
bresult = [];
rresult = [];
for dat1,dat2 in zip(datalist[:-1],datalist[1:]):
    # result format [b_result, r_result],
    # b_result = [[x,y],...]
    biscs,riscs = quantIntersection.findIntersection((dat1),(dat2));
    for bint in biscs:
        bresult.append([(1.0/float(dat1[0,0])),bint[1],0.0]);
    for rint in riscs:
        rresult.append([(1.0/float(dat1[0,0])),rint[1],0.0]);

fileWriter.writeQuantInt(savename+"_bin",model,bresult);
fileWriter.writeQuantInt(savename+"_rho",model,rresult);

    


