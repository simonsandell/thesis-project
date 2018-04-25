import os
import subprocess
import sys
import math
import numpy as np
#import plot stuff and make a figure
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as ax3d

def circles(X,Y,Z):
    phi = np.linspace(0,2*np.pi,100);
    rel_x =np.array([])
    rel_y =np.array([])
    for r in np.linspace(0,0.5,10):
        rel_x = np.concatenate((rel_x,r*np.cos(phi)),axis=0);
        rel_y = np.concatenate((rel_y,r*np.sin(phi)),axis=0);
    for x in np.unique(X):
        for y in np.unique(Y):
            for z in np.unique(Z):
                xx,yy = np.meshgrid(x+rel_x,y+rel_y);
                plt.gcf().gca().plot_surface(x+rel_x,y+ rel_y,z,color='b',alpha=0.7);

def dashedLines(X,Y,Z):
    for x in np.unique(X):
        for y in np.unique(Y):
            for z in np.unique(Z):
                plt.gcf().gca().plot([x-1,x+1],[y,y],[z,z],color='tab:grey',alpha=0.2);
                plt.gcf().gca().plot([x,x],[y-1,y+1],[z,z],color='tab:grey',alpha=0.2);
                plt.gcf().gca().plot([x,x],[y,y],[z-1,z+1],color='tab:grey',alpha=0.2);


def planes(X,Y,Z):
    xmax = X.max() +1;
    xmin = X.min() -1;
    ymax = Y.max() +1;
    ymin = Y.min() -1;
    xx,yy = np.meshgrid(np.linspace(xmin,xmax,100),np.linspace(ymin,ymax,100));
    for z in np.unique(Z):
        plt.gcf().gca().plot_surface(xx,yy,z,alpha = 0.5,color='green');


def diff(x1,y1,x2,y2):
    return pow(pow(x1-x2,2) + pow(y1-y2,2),0.5);
def initCols(n):
    cols = [];
    for i in range(3*n):
        cols.append(mplc.to_rgb('#000000'))
    cols = np.array(cols);
    return cols;
def colSel(n):
    n = n%6;
    coldict = {
            0:      mplc.to_rgb('tab:blue'),
            1:      mplc.to_rgb('tab:orange'),
            2:      mplc.to_rgb('tab:green'),
            3:      mplc.to_rgb('tab:red'),
            4:      mplc.to_rgb('tab:purple'),
            5:      mplc.to_rgb('tab:brown')}
    return coldict[n];

def getCol(new,old,cols,c):
    narrows = new.shape[0]
    for index in range(narrows):
        d = diff(new[index,3],new[index,4],old[index,3],old[index,4]);
        d = d/pow(2,0.5);
        if  d>1.0:
            d =1;
        if (d> 0.00000000001):
            cols[index] = c;
            cols[int(narrows +2*index )] = c[:];
            cols[int(narrows +2*index+1)] = c[:];
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
def saveFigure(pngindex):
    fig = plt.gcf();
    fig.set_size_inches(15,15);
    plt.savefig('./png/'+sys.argv[1]+'Frame%03i'%pngindex +'.png',bbox_inches='tight');
    return pngindex +1;
clust_list= loadData("./lattices/"+sys.argv[1]);
cols = initCols(clust_list[0].shape[1]);
ax1 = plt.subplot(111,projection='3d')
ax1.grid(False)
pngindex = 0;
for n_clust in range(len(clust_list)):
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
            w = np.zeros(u.shape);
            cols = getCol(oldDat,currDat,cols,c);
            linecol = ax1.quiver(x,y,z,u,v,w,colors=cols);
            dots = ax1.scatter(x,y,z,c='black',marker='o')
            #circles(x,y,z);
            dashedLines(x,y,z);
            #planes(x,y,z);
            pngindex =saveFigure(pngindex);
        else:
            ax1.collections.remove(linecol);
            oldDat = currDat;
            currDat =updDat(index,data);
            x = currDat[:,0];
            y = currDat[:,1];
            z = currDat[:,2];
            u = currDat[:,3];
            v = currDat[:,4];
            w = np.zeros(u.shape);
            cols = getCol(oldDat,currDat,cols,c);
            linecol = ax1.quiver(x,y,z,u,v,w,colors=cols);
            pngindex =saveFigure(pngindex);
    pngindex =saveFigure(pngindex);
    pngindex =saveFigure(pngindex);
    pngindex =saveFigure(pngindex);
subprocess.call(['ffmpeg','-framerate','3','-y','-i',r'./png/fourFrame%03d.png','-c:v','libx264',sys.argv[1]+'.mp4'])
