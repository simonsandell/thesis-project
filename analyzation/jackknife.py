import numpy as np

def getJackDelta(mat,calcMeans,blocks):
    N = len(mat);
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
        remblock = mat[:i]
        remblock.extend(mat[i2:]);
        javgs.append(calcMeans(remblock));
        if ((N-i2)< (2*blocksize)):
            N_blocks = N_blocks +1;
            i = i + blocksize;
            i2 = N-1;
            remblock = mat[:i]
            remblock.extend(mat[i2:]);
            javgs.append(calcMeans(remblock));
            cont = False;
        else:
            i = i+blocksize;
            i2 = i2+blocksize;
    javgs = np.array(javgs);
    deltas = [];
    sqrN = pow(N_blocks,0.5);
    if (javgs.ndim > 1):
        for x in range(javgs.shape[1]):
            deltas.append(sqrN*np.std(javgs[:,x]));
    else:
        deltas.append(sqrN*np.std(javgs));

    return deltas;


        


        
        
        
