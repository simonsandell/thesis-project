import numpy as np
import random
def getJackDelta(mat,function,blocknumber):
    N = len(mat);
    random.seed();#seeds with best available?
    random.shuffle(mat);

    blocksize = int(N/blocknumber);
    if (blocksize < 1):
        blocksize  = 1;
    ind = [0];
    i = 0;
    while (i < N):
        i += blocksize;
        if (i > N or i ==(N-1)):
            i = N;
        ind.append(i);
    N_blocks = 0;
    result =[];
    for i in range(len(ind)-1):
        N_blocks +=1;
        tempmat = mat[:];
        tempmat[ind[i]:ind[i+1]] = [];
        result.append(function(tempmat));

    result = np.array(result);
    sqrtN=pow(N_blocks,0.5); 
    deltas = [];
    if (result.ndim >1):
        for x in range(result.shape[1]):
            deltas.append(sqrtN*np.std(result[:,x]));
    else:
        deltas.append(sqrtN*np.std(result));
    return deltas;

