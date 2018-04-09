#ifndef ISING3D_H
#define ISING3D_H
#include "Ising3D/Ising3Dlattice.h"
#include "clusterStruct.h"
#include "randStruct.h"
namespace Ising3D{
	void warmup(LatticeIsing3D& lat,long double N);
	void wolffHistJob(long double L);
	void teqRun(long double L,bool cold);
};
#endif
