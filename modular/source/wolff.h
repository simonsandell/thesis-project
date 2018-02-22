#ifndef WOLFF_H
#define WOLFF_H

#include <random>
#include "latticeStruct.h"
#include "randStruct.h"
#include "clusterStruct.h"

int growCluster(Lattice& lat,Cluster& cluster, long double beta,RandStruct& randgen);



#endif
