#ifndef ISING3D_H
#define ISING3D_H
#include "Ising3D/Ising3Dlattice.h"
#include "clusterStruct.h"
#include "randStruct.h"

#include <string>
namespace Ising3D{
	void warmup(LatticeIsing3D& lat,long double N);
	void wolffHistJob(long double L,std::string maxepath,std::string warmlatpath);
	void teqJob(long double L,bool cold,std::string maxepath,std::string warmlatpath);
	void warmupJob(long double L,std::string maxepath,std::string warmlatpath);
	void loadandPrint(long double L,std::string maxepath,std::string warmlatpath);
};
#endif
