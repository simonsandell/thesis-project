import os
import numpy as np
def findIntersections(X1,Y1,X2,Y2):
    A = np.append(X1,Y1,axis=1);
    B = np.append(X2,Y2,axis=1);

    amin = lambda x1, x2: np.where(x1<x2, x1, x2)
    amax = lambda x1, x2: np.where(x1>x2, x1, x2)
    aall = lambda abools: np.dstack(abools).all(axis=2)
    slope = lambda line: (lambda d: d[:,1]/d[:,0])(np.diff(line, axis=0))

    x11, x21 = np.meshgrid(A[:-1, 0], B[:-1, 0])
    x12, x22 = np.meshgrid(A[1:, 0], B[1:, 0])
    y11, y21 = np.meshgrid(A[:-1, 1], B[:-1, 1])
    y12, y22 = np.meshgrid(A[1:, 1], B[1:, 1])

    m1, m2 = np.meshgrid(slope(A), slope(B))
    m1inv, m2inv = 1/m1, 1/m2

    yi = (m1*(x21-x11-m2inv*y21) + y11)/(1 - m1*m2inv)
    xi = (yi - y21)*m2inv + x21

    xconds = (amin(x11, x12) < xi, xi <= amax(x11, x12), 
              amin(x21, x22) < xi, xi <= amax(x21, x22) )
    yconds = (amin(y11, y12) < yi, yi <= amax(y11, y12),
              amin(y21, y22) < yi, yi <= amax(y21, y22) )

    return xi[aall(xconds)], yi[aall(yconds)]
def sigmaIntersect(directory):
    fdat = [];
    ints = [];
    intstds = [];
    for subdir in sorted(os.listdir(directory)):
        bigmat = np.array([]);
        #each subdir should generate one sigma
        omega = -1;
        for filename in os.listdir(os.path.join(directory,subdir)):
            if (os.stat(os.path.join(directory,subdir,filename)).st_size != 0):
                 #want to compare each line to 
                of = open(os.path.join(directory,subdir,filename),"r");
                fdat[:] = [];
                for ln in of:
                    strln = ln.rsplit("    ");
                    strln = [x.replace("\n","") for x in strln];
                    flln = [float(x) for x in strln];
                    x = flln[0];
                    y = flln[1];
                    if (omega == -1):
                        omega = flln[3];
                    fdat.append([x,y]);
                far = np.array(fdat);
                print(far.shape);
                print(bigmat.shape);
                if (bigmat.shape[0] == 0):
                    bigmat = far;
                else:
                    bigmat = np.append(bigmat,far,axis=1);

        #now all lines are in bigmat
        ints[:] = [];
        xinds = [x for x in range(bigmat.shape[1]) if x % 2 == 0)];
        yinds = [x for x in range(bigmat.shape[1]) if x % 2 == 1)];
        for i in range(len(xinds)-1):
            x2= xinds[i+1:];
            y2= yinds[i+1:];
            for j in range(len(x2)):
                ints.append(findIntersections(bigmat[:,xinds[i]],bigmat[:,yinds[i]],
                        bigmat[:,x2[j]],bigmat[:,y2[j]]));

        intstds.append([omega,np.std(ints)]);

    writeToFile(intstds);
