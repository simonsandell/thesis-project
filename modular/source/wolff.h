#ifndef WOLFF_H
#define WOLFF_H

#include <random>
#include "latticeStruct.h"

int growCluster(Lattice& lat,bool ***cluster, long double &beta,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng);



#endif
