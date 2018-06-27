#ifndef _3DXY_H
#define _3DXY_H
#include "3DXY/3DXYlattice.h"
#include "clusterStruct.h"
#include "randStruct.h"
#include <string>

namespace _3DXY {
	void printSettings(long double rT,long double sT,long double eT,int nT,long double nEQ,bool cold,long double nSamp,long double nBetw,long double L);
	void warmup(Lattice3DXY& lat,long double N);
	void wolffHistJob(long double L,std::string maxepath,std::string warmlatpath,bool printSettings);
	void warmupJob(long double L,std::string maxepath,std::string warmlatpath);
	void teqJob(long double L,bool cold,std::string maxepath,std::string warmlatpath);
	void loadAndPrint(long double L,std::string maxepath,std::string warmlatpath);
	void cputime_vs_delta(std::string maxepath, std::string warmlatpath);
        void full_output(long double L,std::string maxepath,std::string warmlatpath,bool doPrint);
};
#endif
