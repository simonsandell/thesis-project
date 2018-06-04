import multiprocessing
import numpy as np
import sys
import settings

#returns the jackknife estimations of the given func
def jackknife(mat,func,result_size,blocks=100):
    N = mat.shape[0];
    indices = np.arange(N);
    indBlocks= np.array_split(indices,blocks);
    try:
        a = indBlocks[-1][0];
    except:
        print(mat[0,:]);
        print(N);
        print("not enough mcavgs");
        sys.exit(1);
    N_blocks = len(indBlocks);
    res = np.zeros((N_blocks,result_size));
    for i in range(N_blocks):
        xstart = indBlocks[i][0];
        xend =indBlocks[i][-1]+1;
        r_mat = np.concatenate((mat[:xstart,:],mat[xend:,:]));
        res[i,:]=(func(r_mat));
    return res;

#returns the jackknife estimations of the given func(mat1,mat2)
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
        sys.exit(1);

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

#returns the jackknife estimations of the given func(mat1,mat2,mat3)
def jackknife_3(mat1,mat2,mat3,func,result_size,blocks=100):
    N1 = mat1.shape[0];
    N2 = mat2.shape[0];
    N3 = mat3.shape[0];
    ind1 = np.arange(N1);
    ind2 = np.arange(N2);
    ind3 = np.arange(N3);
    indBlocks1= np.array_split(ind1,blocks);
    indBlocks2= np.array_split(ind2,blocks);
    indBlocks3= np.array_split(ind3,blocks);
    try:
        a = indBlocks1[-1][0];
        b = indBlocks2[-1][0];
        c = indBlocks3[-1][0];
    except:
        print(indBlocks1);
        print(indBlocks2);
        print(indBlocks3);
        sys.exit(1);

    if (len(indBlocks1) != len(indBlocks2) or (len(indBlocks2) != len(indBlocks3))):
        print(indBlocks1);
        print(indBlocks2);
        print(indBlocks3);
        print("not equal number of blocks");
        sys.exit(1);
    N_blocks = len(indBlocks1);
    res = np.zeros((N_blocks,result_size));
    for i in range(N_blocks):
        i1start = indBlocks1[i][0];
        i1end =indBlocks1[i][-1]+1;
        i2start = indBlocks2[i][0];
        i2end =indBlocks2[i][-1]+1;
        i3start = indBlocks3[i][0];
        i3end =indBlocks3[i][-1]+1;
        r_mat1 = np.concatenate((mat1[:i1start,:],mat1[i1end:,:]));
        r_mat2 = np.concatenate((mat2[:i2start,:],mat2[i2end:,:]));
        r_mat3 = np.concatenate((mat3[:i3start,:],mat3[i3end:,:]));
        res[i,:]=(func(r_mat1,r_mat2,r_mat3));
    return res;
