import numpy as np

def jackknife(mat,func,blocks=100):
    N = mat.shape[0];
    blocksize = int(N/blocknumber);
    if (blocksize < 1):
        blocksize  = 1;
    indices = np.arange(N);
    indBlocks= np.array_split(indices,blocksize);
    res = 0.0;
    for x in indBlocks:
        res += (func(mat[[x for x in indices if x not in x],:])/float(len(indices)));







def jackknife_delta(mat,func,blocks=100):
    # mat = numpy array
    # bin the indices into 100 blocks

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
        result.append(func(tempmat));

    result = np.array(result);
    sqrtN=pow(N_blocks,0.5); 
    deltas = [];
    if (result.ndim >1):
        for x in range(result.shape[1]):
            deltas.append(sqrtN*np.std(result[:,x]));
    else:
        deltas.append(sqrtN*np.std(result));
    return deltas;

