import numpy as np

def jackknife(mat,func,result_size,blocks=100):
    N = mat.shape[0];
    indices = np.arange(N);
    indBlocks= np.array_split(indices,blocks);
    try:
        a = indBlocks[-1][0];
    except:
        print(mat);
        print("not enough mcavgs");
        exit(1);
    N_blocks = len(indBlocks);
    res = np.zeros((N_blocks,result_size));
    for i in range(N_blocks):
        xstart = indBlocks[i][0];
        xend =indBlocks[i][-1]+1;
        r_mat = np.concatenate((mat[:xstart,:],mat[xend:,:]));
        res[i,:]=(func(r_mat));
    return res;

def jackknife_2(mat1,mat2,func,result_size,blocks=100):
    N1 = mat1.shape[0];
    N2 = mat2.shape[0];
    ind1 = np.arange(N1);
    ind2 = np.arange(N2);
    indBlocks1= np.array_split(ind1,blocks);
    indBlocks2= np.array_split(ind2,blocks);
    try:
        a = indBlocks1[-1][0];
        b = indBlocks2[-1][0];
    except:
        print(indBlocks1);
        print(indBlocks2);
        exit(1);

    if (len(indBlocks1) != len(indBlocks2)):
        print(indBlocks1);
        print(indBlocks2);
        print("not equal number of blocks");
        exit(1);
    N_blocks = len(indBlocks1);
    res = np.zeros((N_blocks,result_size));
    for i in range(N_blocks):
        i1start = indBlocks1[i][0];
        i1end =indBlocks1[i][-1]+1;
        i2start = indBlocks2[i][0];
        i2end =indBlocks2[i][-1]+1;
        r_mat1 = np.concatenate((mat1[:i1start,:],mat1[i1end:,:]));
        r_mat2 = np.concatenate((mat2[:i2start,:],mat2[i2end:,:]));
        res[i,:]=(func(r_mat1,r_mat2));
    return res;

