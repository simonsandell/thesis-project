#ifndef WOLFF_H
#define WOLFF_H

#include "Ising3Dlattice.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

int clusterIsing3D(LatticeIsing3D& lat,Cluster& cluster, long double beta,RandStruct& randgen);



#endif
