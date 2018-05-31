import numpy as np
import sys

from analysis import testIntersection
import settings
import anaFuncs

# takes X, Y1, Y2 as input and finds and returns intersections
# can return multiple intersections
def findIntersection(X,Y1,Y2):
    result = [];
    for i in range(X.shape[0]-1):
        T1 = X[i];
        T2 = X[i+1];
        p1 = np.array([X[i],Y1[i]]);
        p2 = np.array([X[i+1],Y1[i+1]]);
        q1 = np.array([X[i],Y2[i]]);
        q2 = np.array([X[i+1],Y2[i+1]]);
# returns [x,y] value of intersection of the lines through the points
        isc = testIntersection.seg_intersect(p1,p2,q1,q2);
# if x val of int is between the two x values of the points, add this intersection to result
        if ((isc[0] > T1) and (isc[0] < T2)):
            result.append(isc);
    result = np.array(result);
    return result;



# takes intersectionpoints as input, calcultes closeness
def findCloseness(pts):
    #calculate average x and y
    #calculate mean distance to average
    avgx=0;avgy=0;
    n_pts = 0;
    for pt in pts:
        for p in pt:
            n_pts+=1;
            avgx+=p[0];
            avgy+=p[1];
    dist =[];
    avgx /=float(n_pts);
    avgy /=float(n_pts);
    for pt in pts:
        for p in pt:
            dx = abs(p[0] - avgx);
            dy = abs(p[1] - avgy);
            dist.append(pow((dx**2) + (dy**2),0.5));
    return [np.mean(dist),avgx,avgy];


