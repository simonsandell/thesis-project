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
Tint_b = [];
Tint_r = [];
int_b = [];
int_r = [];
for dat1,dat2 in zip(datalist[:-1],datalist[1:]):
    # result format [b_result, r_result],
    # b_result = [[x,y],...]
    biscs,riscs = quantIntersection.findIntersection((dat1),(dat2));
    for bint in biscs:
        Tint_b.append([(1.0/float(dat1[0,0])),bint[0],0.0]);
        int_b.append([(1.0/float(dat1[0,0])),bint[1],0.0]);
    for rint in riscs:
        Tint_r.append([(1.0/float(dat1[0,0])),rint[0],0.0]);
        int_r.append([(1.0/float(dat1[0,0])),rint[1],0.0]);

fileWriter.writeQuantInt(savename+"_bin_T",Tint_b);
fileWriter.writeQuantInt(savename+"_rho_T",Tint_r);

fileWriter.writeQuantInt(savename+"_bin",int_b);
fileWriter.writeQuantInt(savename+"_rho",int_r);
    


