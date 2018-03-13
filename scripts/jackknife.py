import numpy as np



def getJackDelta(mat,calcMeans,blocks):
    N = mat.shape[0];
    if(N < blocks*10):
        blocksize = 1;
    else:
        blocksize =int(N/blocks);
    i = 0;
    i2 = i + blocksize;
    cont = True;
    javgs = [];
    N_blocks = 0;
    while (cont):
        N_blocks = N_blocks +1;
        remblock = np.concatenate((mat[:i,:],mat[i2:,:]));
        javgs.append(calcMeans(remblock));
        if ((N-i2)< (2*blocksize)):
            N_blocks = N_blocks +1;
            i = i + blocksize;
            i2 = N-1;
            remblock = np.concatenate((mat[:i,:],mat[i2:,:]));
            javgs.append(calcMeans(remblock));
            cont = False;
        else:
            i = i+blocksize;
            i2 = i2+blocksize;
    
    javgs = np.array(javgs);
    deltas = [];
    sqrN = pow(N_blocks,0.5);
    for x in range(javgs.shape[1]):
        deltas.append(sqrN*np.std(javgs[:,x]));
    return deltas;


        


        
        
        
