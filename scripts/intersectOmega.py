import os
import numpy as np
import math
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
    for i in range(len(X1)-1):
        intersection = intersects(X1[i:i+2],Y1[i:i+2],X2[i:i+2],Y2[i:i+2]);
        if (intersection[0] != -1):
            ret.append(intersection);
    return ret;

def sigmaIntersect(directory):
    fdat = [];
    intersections = [];
    intersections2 = [];
    measures= [];
    measures2=[];
    for subdir in sorted(os.listdir(directory)):
        bigmat = np.array([]);
        #each subdir should generate one sigma
        omega = -1;
        for filename in sorted(os.listdir(os.path.join(directory,subdir))):
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
                if (bigmat.shape[0] == 0):
                    bigmat = far;
                else:
                    bigmat = np.append(bigmat,far,axis=1);

        #now all lines for one omega are in bigmat
        intersections[:] = [];
        intersections2[:] = [];
        xinds = [x for x in range(bigmat.shape[1]) if ((x % 2) == 0)];
        yinds = [x for x in range(bigmat.shape[1]) if ((x % 2) == 1)];
        for i in range(len(xinds)-1):
            x2= xinds[i+1:];
            y2= yinds[i+1:];
            for j in range(len(x2)):
                intersections.append(findIntersection(bigmat[:,xinds[i]],bigmat[:,yinds[i]],
                        bigmat[:,x2[j]],bigmat[:,y2[j]]));
        for i in range(len(xinds)-2):
            x2= xinds[i+2:];
            y2= yinds[i+2:];
            for j in range(len(x2)):
                intersections2.append(findIntersection(bigmat[:,xinds[i+1]],bigmat[:,yinds[i+1]],
                        bigmat[:,x2[j]],bigmat[:,y2[j]]));
        #now intersections are found
        #remove empty listst;
        intersections = [x for x in intersections if x != []];
        intersections2 = [x for x in intersections2 if x != []];
        if (len(intersections) == 3 or len(intersections) == 6 or len(intersections) == 10):
            measures.append([omega,findDist(intersections)]);
        if (len(intersections2) == 3 or len(intersections2) == 6 or len(intersections2) == 10):
            measures2.append([omega,findDist(intersections2)]);

    fullpath= getDirName(directory);
    filename = os.path.join(fullpath,"std.dat");
    filename2 = os.path.join(fullpath,"std_wo4.dat");
    writeToFile(measures,filename);
    writeToFile(measures2,filename2);
