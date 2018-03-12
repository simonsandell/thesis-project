#ifndef ISING3D_H
#define ISING3D_H
#include "Ising3D/Ising3Dlattice.h"
#include "clusterStruct.h"
#include "randStruct.h"
namespace Ising3D{
	void warmup(LatticeIsing3D& lat,Cluster&clust,RandStruct& rand,int N);
	void wolffHistJob(long double L);
};
#endif
