import jackknife

def openFile(fName,N):
    ofile = open("./foutput/3DXY/rhos_omega/" + str(N) + ".dat","a");
    return ofile;





def calculate(mat,i,ifirst,fName);
    omegarange = [];
    ostart = 0.5;
    oend = 1.0;
    N_omega = 21;
    for x in range(N_omega ):
        omegarange.append(ostart + (x/(N_omega -1.0))*(oend-ostart));
    for omega in omegarange:
        omegafile = openFile(fName,omega);



def analyze(mat,fName):
    ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,1],mat[:,0]));
    sortedMat = mat[ind];
    #form averages and print to file
    T = sortedMat[0,1];
    
    TOL = 0.000001;
    ifirst = 0;
    for i in range(sortedMat.shape[0]):
        if (sortedMat[i,1] != T):
            calculate(sortedMat,i,ifirst,fName);
            ifirst = i;
            T = sortedMat[i,1];
            
    #one final write
    calculate(sortedMat,i+1,ifirst,filelist,fName);
