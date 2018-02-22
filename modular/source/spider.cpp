#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "ioFuncs.h"
#include "calcQuants.h"
#include "latticeOps.h"
#include "latticeStruct.h"
#include "clusterStruct.h"
#include "randStruct.h"
#include "metroRun.h"
#include "wolffHistRun.h"
#include "wolff.h"

using namespace std;

void warmup(Lattice& lat,Cluster&clust,long double beta,RandStruct&rand,int N){
	int Nspins = lat.L*lat.L*lat.L;
	int fliptries = 0;
	while ((fliptries/Nspins) < N){
		fliptries += growCluster(lat,clust,beta,rand);
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

//main
int main(){
	//
	//Set Run Parameters
	//
	//

	//temperatures
	long double	startT=			2.20150L;
	long double	endT=			2.20350L;
	int 		Ntemps=			21.0L;
	//generate temperature range
	long double* Trange;
	if (abs(Ntemps - 1) < 0.1) {
		Trange = new long double[1];
		Trange[0] = startT;
	}
	else {
		Trange = getTrange(startT,endT,int(Ntemps));
	}
	long double runTemp = 2.20200000000000L;
	//system size
	long double 	L =			4.0L;
	//initial equilibration sweeps
	int 		Neq=			20000;
	//initial configuration
	bool 		cold=			true;
	//sample sweeps per run
	long double	Nsamp=			1000.0L;
	//eq sweeps between runs
	int 		Nbetw=			100;
	//number of total runs
	int 		Nruns=			1000;
	//
	//End of parameters
	//
	
	
	Lattice lat(L,cold);
	Cluster clust(L);
	RandStruct rand;
	//initial warmup
	long double beta = 1.0L/runTemp;
	warmup(lat,clust,beta,rand,(Neq-Nbetw));
	//sample
	for (int i=0; i< Nruns; ++i){	
		warmup(lat,clust,beta,rand,Nbetw);
		wolffHistRun(lat,Nsamp,Trange,Ntemps,runTemp);

	}

}

