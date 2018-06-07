import numpy as np
import sys

from analysis import testIntersection
import settings
import anaFuncs

# takes datatable as input, i.e. already calculated averages.
def findIntersection(dt1, dt2):
    if settings.model == "3DXY":
        idx = anaFuncs.get3DXYIndex()
        b_result = []
        r_result = []
        for i in range(dt1.shape[0] - 1):
            T1 = dt1[i, idx["T"]]
            T2 = dt1[i + 1, idx["T"]]
            tind = idx["T"]
            bind = idx["B"][0]
            rind = idx["RS"][0]
            p1 = np.array([dt1[i, tind], dt1[i, bind]])
            p2 = np.array([dt1[i + 1, tind], dt1[i + 1, bind]])
            q1 = np.array([dt2[i, tind], dt2[i, bind]])
            q2 = np.array([dt2[i + 1, tind], dt2[i + 1, bind]])
            b_isc = testIntersection.seg_intersect(p1, p2, q1, q2)
            if (b_isc[0] > T1) and (b_isc[0] < T2):
                b_result.append(b_isc)
            p1 = np.array([dt1[i, tind], dt1[i, rind]])
            p2 = np.array([dt1[i + 1, tind], dt1[i + 1, rind]])
            q1 = np.array([dt2[i, tind], dt2[i, rind]])
            q2 = np.array([dt2[i + 1, tind], dt2[i + 1, rind]])
            r_isc = testIntersection.seg_intersect(p1, p2, q1, q2)
            if (r_isc[0] > T1) and (r_isc[0] < T2):
                r_result.append(r_isc)
        b_result = np.array(b_result)
        r_result = np.array(r_result)
        return [b_result, r_result]
