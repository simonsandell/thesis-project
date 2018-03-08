#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>
#include <vector>
#include <chrono>

#include "ThreadPool.h"
#include "ioFuncs.h"
#include "latticeStruct.h"
#include "clusterStruct.h"
#include "randStruct.h"
#include "metroRun.h"
#include "metropolis.h"
#include "wolffHistRun.h"
#include "wolff.h"

using namespace std;

void warmup(Lattice& lat,Cluster&clust,long double beta,RandStruct&rand,int N){
	long double Nspins = lat.L*lat.L*lat.L;
	long double fliptries = 0;
	long double clusts = 0;
	while ((fliptries/Nspins) < N){
		clusts += 1.0L;
		fliptries +=(long double) growCluster(lat,clust,beta,rand);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = clusts;
		lat.Neqsweeps = ((long double)fliptries)/((long double)Nspins);
		lat.warmedUp = true;
	}
}
void warmupMetro(Lattice& lat,long double beta,RandStruct&rand,int N){
	for (int i = 0; i < N; i++){
		metrosweep(lat,beta,rand);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = 0;
		lat.Neqsweeps =(long double)N;
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

void wolffHistJob(long double L){
	long double runTemp = 2.20260000000000L;

	long double	startT=			2.20200L;
	long double	endT=			2.20320L;
	int 		Ntemps=			21;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrange(startT,endT,int(Ntemps));
	}
	int 		Neq=			100000;
	bool 		cold=			true;
	long double	Nsamp=			100000.0L;
	int 		Nbetw=			100;
	int 		Nruns=			100;
	Lattice lat(L,cold);
	Cluster clust(L);
	RandStruct rand;
	long double beta = 1.0L/runTemp;
	warmup(lat,clust,beta,rand,(Neq));
	for (int i=0; i< Nruns; ++i){	
		wolffHistRun(lat,Nsamp,Trange,Ntemps,runTemp);
		warmup(lat,clust,beta,rand,Nbetw);
	}

}
void metroJob(long double L){

	long double 	runTemp = 		2.20200000000000L;
	int 		Neq=			20000;
	bool 		cold=			true;
	long double	Nsamp=			1000.0L;
	int 		Nbetw=			100;
	int 		Nruns=			1000;
	Lattice lat(L,cold);
	RandStruct rand;
	long double beta = 1.0L/runTemp;
	warmupMetro(lat,beta,rand,(Neq-Nbetw));
	for (int i=0; i< Nruns; ++i){	
		warmupMetro(lat,beta,rand,Nbetw);
		metroRun(lat,Nsamp,runTemp);
	}
}

//main
//
int main(){
	ThreadPool pool(12);
	std::vector< std::future<void> > results;
	for(int i = 0; i < 100; ++i) {
		results.emplace_back(
				pool.enqueue([i] {
					wolffHistJob(32.0L);
					})
				);
	}
}

