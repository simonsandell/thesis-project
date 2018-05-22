import numpy as np
import sys

import jackknife
import modelAvgs
import fileWriter
import settings

#calculates the L^{w} ( Q(2L) - Q(L)) quantity
#for a single temperature
def scalingMethod(view1,view2,model="3DXY"):
    if (view1[0,1] != view2[0,1]):
        print(view1[0,1]);
        print(view2[0,1]);
        print("not equal T's");
        exit(1);
    T = view1[0,1];
    if (model=="3DXY"):
        result = np.zeros(2);
        b1 = modelAvgs.getBin(np.mean(view1[:,10]),np.mean(view1[:,11]),np.mean(view1[:,21]));
        b2 = modelAvgs.getBin(np.mean(view2[:,10]),np.mean(view2[:,11]),np.mean(view2[:,21]));
        r1 = modelAvgs.getRs(np.mean(view1[:,7]),
                np.mean(view1[:,14]),
                np.mean(view1[:,15]),
                np.mean(view1[:,16]),
                np.mean(view1[:,21]),
                view1[0,0],view1[0,1]);
        r2 = modelAvgs.getRs(np.mean(view2[:,7]),
                np.mean(view2[:,14]),
                np.mean(view2[:,15]),
                np.mean(view2[:,16]),
                np.mean(view2[:,21]),
                view2[0,0],view2[0,1]);
        result[0] = b2 -b1;
        result[1] = r2 -r1;
        return result;

# take two datasets for 2 L's, calculates a structure containing L^omega(Q[2L] - Q[L])    
# saves to .npy in pickles folder
# writes to txt file
def twoLomega(data1,data2,model,savename):
    ind1 = np.lexsort((data1[:,4],data1[:,1]),axis=0);
    ind2 = np.lexsort((data2[:,4],data2[:,1]),axis=0);
    data1 = data1[ind1];
    data2 = data2[ind2];
    
    L1 = data1[0,0];
    L2 = data2[0,0];
    if (L2 != (2*L1)):
        print(L1)
        print(L2)
        print("not factor 2")
        exit(1);
    
    #temp loop
    tv1,ti1 = np.unique(data1[:,1],return_index=True);
    ti1 = np.append(ti1,data1.shape[0]);
    tv2,ti2 = np.unique(data2[:,1],return_index=True);
    ti2 = np.append(ti2,data2.shape[0]);
    if (ti1.shape[0] != ti2.shape[0]):
        print("not equal number of temps");
        exit(1);
                                   # 2 L's, one T, 2 results, 2 Nmcavg, 2 deltas = 9
    result = np.zeros((ti1.shape[0]-1,2+1+2+2+2));
    for i in range(ti1.shape[0] -1):
        view1= data1[ti1[i]:ti1[(i+1)],:];
        view2 = data2[ti2[i]:ti2[(i+1)],:];
        b_res,r_res = scalingMethod(view1,view2,model);
        jackres = jackknife.jackknife_2(view1,view2,scalingMethod,2);
        b_jack = jackres[:,0]; 
        r_jack = jackres[:,1];
        b_delta = (np.std(b_jack))*np.sqrt(b_jack.shape[0]-1);
        r_delta = (np.std(r_jack))*np.sqrt(r_jack.shape[0]-1);
        result[i,:] = [L1,L2,view1[0,1],b_res,r_res,view1.shape[0],view2.shape[0],b_delta,r_delta];
    np.save(settings.pickles_path+str(L1)+"_"+str(L2)+"_2Lquant",result);
    fileWriter.write2LData(savename,model,result);
    return result;
