import os
import sys
import math
import numpy as np
#import plot stuff and make a figure
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as ax3d
from matplotlib import animation
def diff(x1,y1,x2,y2):
    return pow(pow(x1-x2,2) + pow(y1-y2,2),0.5);
def initCols(n):
    cols = [];
    for i in range(3*n):
        cols.append((0,0,0))
    cols = np.array(cols);
    return cols;
def colSel(n):
    coldict = {
            0:      (0,     0,      1      ),
            1:      (0,     1,      0      ),
            2:      (1,     0,      0      ),
            3:      (1,     0.5,    0      ),
            4:      (1,     0,      0.5    ),
            5:      (0,     1,      0.5    )}
    return coldict[n];

def getCol(new,old,cols,c):
    narrows = new.shape[0]
    for index in range(narrows):
        d = diff(new[index,3],new[index,4],old[index,3],old[index,4]);
        d = d/pow(2,0.5);
        if  d>1.0:
            d =1;
        if (d> 0.00000000001):
            cols[index,:] = c[:];
            cols[int(narrows +2*index ),:] = c[:];
            cols[int(narrows +2*index+1),:] = c[:];
    return cols;

def loadData(filename):
    datafile = open(filename,"r")
    frame = [];
    data = [];
    clusts = [];
    first = True
    for ln in datafile:
        if "newclust" in ln:
            clusts.append(np.array(data[:]));
            data[:] = []
        elif "newframe" in ln:
            data.append(frame[:]);
            frame[:] = [];
        else:
            strln = ln.rsplit(" ");
            del(strln[-1])
            flln = [float(x) for x in strln];
            flln[3] = flln[3]*0.5;
            flln[4] = flln[4]*0.5;
            frame.append(flln);
    
    return clusts;

def updDat(index,data):
    return data[index,:,:];
        
clust_list= loadData("./lattices/"+sys.argv[1]);
cols = initCols(clust_list[0].shape[1]);
ax1 = plt.subplot(111,projection='3d')
plt.ion()
plt.show()
for n_clust in range(len(clust_list)):
    plt.suptitle('Number of clusters: ' + str(1+ n_clust));
    data = clust_list[n_clust];
    c = colSel(n_clust);
    for index in range(data.shape[0]):
        if n_clust ==  0 and index == 0:
            currDat =updDat(index,data);
            oldDat = currDat
            x = currDat[:,0];
            y = currDat[:,1];
            z = currDat[:,2];
            u = currDat[:,3];
            v = currDat[:,4];
            w = np.zeros(v.shape);
            cols = getCol(oldDat,currDat,cols,c);
            linecol = ax1.quiver(x,y,z,u,v,w,colors=cols);
            dots = ax1.scatter(x,y,z,c='black',marker='o')
            plt.savefig('./png/'+sys.argv[1]+'Frame%03i.png'%index);
        else:
            ax1.collections.remove(linecol);
            oldDat = currDat;
            currDat =updDat(index,data);
            x = currDat[:,0];
            y = currDat[:,1];
            z = currDat[:,2];
            u = currDat[:,3];
            v = currDat[:,4];
            w = np.zeros(v.shape);
            cols = getCol(oldDat,currDat,cols,c);
            linecol = ax1.quiver(x,y,z,u,v,w,colors=cols);
            plt.savefig('./png/'+sys.argv[1]+'Frame%03i.png'%index);
            plt.draw()
plt.ioff();
plt.show()
