import os
import numpy as np
import math

import matplotlib.pyplot as plt

def getDirName(directory):
    b =os.path.dirname(directory);
    a = (directory.replace(b,""))
    a = a.replace("/","");
    a = "std_" + a;
    a = os.path.join(os.path.dirname(directory),a);
    return a;
def writeToFile(data,fullpath):
    outfile = open(fullpath,"w");
    fstr = "{:30.30f}";
    for ls in data:
        outfile.write(fstr.format(ls[0]) + "    " + fstr.format(ls[1]) +"    " + "0.0"+ "\n");

def sgn(x):
    return x/abs(x);
def getK(x,y):
    return (y[1] - y[0])/(x[1] - x[0]);
def getM(x,y,k):
    return (y - x*k);
def xisec(k1,k2,m1,m2):
    return (m2-m1)/(k1-k2);
def getY(x,k,m):
    return x*k +m;
def intersects(x1,y1,x2,y2):
    diff = [y1[0] - y2[0],y1[1]-y2[1]];
    TOL = 0.01;
    if (abs(sgn(diff[0]) - sgn(diff[1]))> TOL): 
        k1 = getK(x1,y1)
        k2 = getK(x2,y2)
        m1 = getM(x1[0],y1[0],k1);
        m2 = getM(x2[0],y2[0],k2);
        
        xi = xisec(k1,k2,m1,m2);
        yi = getY(xi,k1,m1);
        return [xi,yi];
    else:
        return [-1,-1];

def dist(x1,y1,x2,y2):
    return pow(pow(x1-x2,2) + pow(y1-y2,2),0.5)

def findDist(intersections):
    npints = np.squeeze(np.array(intersections));
    avgX = np.mean(npints[:,0]);
    avgY = np.mean(npints[:,1]);
    dlist = [];
    for i in range(npints.shape[0]):
        dlist.append(dist(npints[i,0],npints[i,1],avgX,avgY));
    return np.mean(dlist);


    
def findIntersection(X1,Y1,X2,Y2):
    ret = [];
    for i in range(len(X1)-2):
        intersection = intersects(X1[i:i+2],Y1[i:i+2],X2[i:i+2],Y2[i:i+2]);
        if (intersection[0] != -1):
            ret.append(intersection);
    return ret;
def plot_lines(mat,linds,ints):
    for i in range(len(linds)-1):
        plt.plot(mat[linds[i]:linds[i+1],2],mat[linds[i]:linds[i+1],3]);
    x=[];
    y=[];
    for i in range(len(ints)):
        x.append(ints[i][0]);
        y.append(ints[i][1]);
    plt.scatter(x,y);
    plt.show();
def selectInt(ints, tc):
    reti = 0;
    minD = 1000;
    for i in range(len(ints)):
        D = np.abs(ints[i][0] - tc);
        if (D < minD):
            minD = D;
            reti = i;
    if (minD != 1000):
        return ints[reti];
    else:
        print("select int failed")
        exit(-1);

    

def sigmaIntersect(directory,skipsmallest,tcguess):
    filedata =[]; 
    intersections = [];
    test_intersections = [];
    measures=[];
    doPlot = input("plot?");
    #each file covers one omega
    for filename in sorted(os.listdir(directory)):
        if (os.stat(os.path.join(directory,filename)).st_size != 0):
            filedata[:] = [];
            of = open(os.path.join(directory,filename),"r");
            for ln in of:
                strln = ln.rsplit("    ");
                strln = [x.replace("\n","") for x in strln];
                flln = [float(x) for x in strln];
                filedata.append(flln); 
        data = np.array(filedata);
        omega = data[0,5];
        #sort by L,then T
        ind = np.lexsort((data[:,2],data[:,0]));
        data = data[ind];
        l_vals,l_inds = np.unique(data[:,0],return_index=True);
        l_inds = np.append(l_inds,-1);
        N_L = len(l_vals);
        if (skipsmallest):
            l_inds = l_inds[1:];
            N_L = N_L -1;
        intersections[:] = [];
        test_intersections[:] = [];
        for i in range(N_L-1):
            x1 = data[l_inds[i]:l_inds[i+1],2];
            y1 = data[l_inds[i]:l_inds[i+1],3];
            for j in range(N_L -1 -i):
                x2 = data[l_inds[i+j+1]:l_inds[i+j+2],2];
                y2 = data[l_inds[i+j+1]:l_inds[i+j+2],3];
                isec = findIntersection(x1,y1,x2,y2);
                for k in range(len(isec)):
                    test_intersections.append(isec[k]);
                if (len(isec)==1):
                    intersections.append(isec[0]);
                if (len(isec)>1):

                    intersections.append(selectInt(isec,tcguess));

        if (doPlot == "Y"):
            plot_lines(data,l_inds,test_intersections);
            plot_lines(data,l_inds,intersections);

        if (len(intersections) > 1):
            measures.append([omega,findDist(intersections)]);

    fullpath= getDirName(directory);
    filename = os.path.join(fullpath,"std.dat");
    if (skipsmallest): 
        filename = os.path.join(fullpath,"std_drop_2_smallest.dat");
    print(measures);
    measures = sorted(measures)
    print(measures);

    writeToFile(measures,filename);
