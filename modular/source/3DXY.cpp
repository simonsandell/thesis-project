#include <string>
#include <iostream>
#include "3DXY/3DXYio.h"
#include "3DXY/3DXYlattice.h"
#include "3DXY/3DXYrunMetro.h"
#include "3DXY/3DXYrunWolff.h"
#include "3DXY/3DXYwolff.h"
#include "3DXY.h"
#include "clusterStruct.h"
#include "randStruct.h"

void _3DXY::warmup(Lattice3DXY& lat,long double N){
	long double steps;
	long double NClusts = 0;
	long double NSweeps = 0;
	while (NSweeps < N){
		steps = cluster3DXY(lat);
		NClusts += 1.0L;
		NSweeps += (steps/lat.Nspins);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = NClusts;
		lat.Neqsweeps = NSweeps;
		lat.warmedUp = true;
	}
}

//generate range of temperatures
long double * getTrange(long double start, long double end, int N){
	long double dt = (end-start)/((long double)N-1.0L);
	long double *T = new long double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (long double)i*dt;
	}
	return T;
}

void _3DXY::wolffHistJob(long double L,std::string maxepath,std::string warmlatpath){

	long double runTemp = 2.20200000000000L;

	long double	startT=			2.20100L;
	long double	endT=			2.20350L;
	int 		Ntemps=			101;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrange(startT,endT,Ntemps);
	}
	long double 	Neq=			1000.0L;
	bool 		cold=			true;
	long double	Nsamp=			100000.0L;
	long double 	Nbetw=			100.0L;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
	lat.loadLattice();
	warmup(lat,Neq);
	for (int i = 0; i < 1000; ++i){
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
		warmup(lat,Nbetw);
	}

}
void _3DXY::warmupJob(long double L, std::string maxepath,std::string warmlatpath){
	long double runTemp = 2.202000000000000L;
	bool cold = true;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
	lat.loadLattice();
	long double Neq = 1000.0L;
	while (lat.NTotSweeps < 100000.0L){
		warmup(lat,Neq);
		lat.saveLatticeAs("latest");
	}
}
	
void _3DXY::teqJob(long double L,bool cold,std::string maxepath,std::string warmlatpath){
	long double runTemp = 2.201850000000000L;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
	lat.maxE *= 2.0L;
	
	int Ntemps = 1;
	long double Trange[1] = {runTemp};
	long double Nsamp = 2;
	wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
	wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
	for (int i = 0; i< 10; ++i){
		Nsamp *= 2.0L;
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
	}
	if (lat.oPer.outputLines.size() > 0){
		lat.oPer.printData(0);
	}
}
void _3DXY::loadandPrint(long double L,std::string maxepath,std::string warmlatpath){
	long double runTemp = 2.2020000000000L;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,true,r,c,maxepath,warmlatpath);
	lat.loadLattice();
	lat.printVals();
}
