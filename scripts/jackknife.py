import numpy as np

def jackknife(mat,func,blocks=100):
    N = mat.shape[0];
    indices = np.arange(N);
    indBlocks= np.array_split(indices,blocks);
    N_blocks = len(indBlocks);
    res = np.zeros((N_blocks,mat.shape[1]));
    for i in range(N_blocks):
        xstart = indBlocks[i][0];
        xend =indBlocks[i][-1]+1;
        r_mat = np.concatenate((mat[:xstart,:],mat[xend:,:]));
        res[i,:]=(func(r_mat));
    return res;

