import numpy as np
import sys
import os
import time
import settings

from analysis import modelAvgs
from plotting import fileWriter
import anaFuncs


# calculates the L^{w} ( Q(2L) - Q(L)) quantity with omega =0
# for a single temperature
idx = anaFuncs.get3DXYIndex();
def scalingMethod(view1,view2,model="3DXY"):
    T = view1[1];
    if (model=="3DXY"):
        result = np.zeros(2);
        b1 = view1[idx["B"][0]];
        b2 = view2[idx["B"][0]];
        r1 = view1[idx["RS"][0]];
        r2 = view2[idx["RS"][0]];
        result[0] = b2 -b1;
        result[1] = r2 -r1;
        return result;

def mpfunction(views):
    view1,view2 = views;
    if (abs(view1[1]-view2[1])>0.0000001):
        print(view1[1],view2[1])
        print(view1.shape)
        print(view2.shape)
        sys.exit(1);
    b_res,r_res = scalingMethod(view1,view2);
    return [view1[0],view2[0],view1[1],b_res,r_res];

# take two datatable, jacknife or normal, for 2 L's, calculates a structure containing L^omega(Q[2L] - Q[L])    
# format [L1 L2 T bin rho]
# saves to .npy in pickles folder
def twoLomega(data1,data2,model,tag):
    #sort by temperature
    ind1 = np.lexsort((data1[:,4],data1[:,1]),axis=0);
    ind2 = np.lexsort((data2[:,4],data2[:,1]),axis=0);
    data1 = data1[ind1];
    data2 = data2[ind2];
    
    #check if L2 = 2*L1
    L1 = data1[0,0];
    L2 = data2[0,0];
    if (L2 != (2*L1)):
        print(L1)
        print(L2)
        print("not factor 2")
        exit(1);
    
    #check if same n of temps
    if (data1.shape[0] != data2.shape[0]):
        print("not equal number of temps");
        exit(1);
                                   # 2 L's, one T, 2 results, 2 Nmcavg, 2 deltas = 9
    #result = np.zeros((ti1.shape[0]-1,2+1+2+2+2));
    result = [];
    arglist =[]
    for i in range(data1.shape[0]):
        view1= data1[i,:];
        view2 = data2[i,:];
        result.append(mpfunction([view1,view2]));
    nproc = settings.nprocs;
    result = np.array(result);
    result = result[result[:,2].argsort()];
    savename = tag +"_"+str(L1)+"_"+str(L2);
    if not os.path.exists(settings.pickles_path+"2Lquant/"):
        os.makedirs(settings.pickles_path+"2Lquant/");
    if not (tag == "dontsave"):
        np.save(settings.pickles_path+"2Lquant/"+savename,result);
    return result;
