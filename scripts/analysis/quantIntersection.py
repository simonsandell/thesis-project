import numpy as np
import sys

import testIntersection
import anaFuncs

# takes datatable as input, i.e. already calculated averages.
def findIntersection(dt1,dt2,model="3DXY"):
    if (model == "3DXY"):
        idx = anaFuncs.get3DXYIndex();
        b_result = [];
        r_result = [];
        for i in range(dt1.shape[0]-1):
            T1 = dt1[i,idx["T"]];
            T2 = dt1[i+1,idx["T"]];
            tind = idx["T"];
            bind = idx["B"][0];
            rind = idx["RS"][0];
            p1 = np.array([dt1[i,tind],dt1[i,bind]]);
            p2 = np.array([dt1[i+1,tind],dt1[i+1,bind]]);
            q1 = np.array([dt2[i,tind],dt2[i,bind]]);
            q2 = np.array([dt2[i+1,tind],dt2[i+1,bind]]);
            print(T1)
            print(T2)
            print(p1)
            print(p2)
            print(q1)
            print(q2)

            b_isc = testIntersection.seg_intersect(p1,p2,q1,q2);
            print(b_isc)
            if ((b_isc[0] > T1) and (b_isc[0] < T2)):
                b_result.append(b_isc);
            p1 = np.array([dt1[i,tind],dt1[i,rind]]);
            p2 = np.array([dt1[i+1,tind],dt1[i+1,rind]]);
            q1 = np.array([dt2[i,tind],dt2[i,rind]]);
            q2 = np.array([dt2[i+1,tind],dt2[i+1,rind]]);
            r_isc = testIntersection.seg_intersect(p1,p2,q1,q2);
            if ((r_isc[0] > T1) and (r_isc[0] < T2)):
                r_result.append(r_isc);
        b_result = np.array(b_result);
        r_result = np.array(r_result);
        return [b_result,r_result];

file1 = sys.argv[1];
file2 = sys.argv[2];
model = sys.argv[3];

dat1 = np.load("./pickles/datatable_"+file1+model+".npy");
dat2 = np.load("./pickles/datatable_"+file2+model+".npy");
print(dat1.shape);
print(dat2.shape)

iscs = findIntersection(dat1,dat2);
print(iscs[0])
print(len(iscs[0]))
print(iscs[1])
print(len(iscs[1]))


