
#include "3DXY/3DXYio.h"
#include "3DXY/3DXYlattice.h"
#include "3DXY/3DXYrunMetro.h"
#include "3DXY/3DXYmetro.h"
#include "3DXY/3DXYrunWolff.h"
#include "3DXY/3DXYwolff.h"
#include "3DXY.h"
#include "clusterStruct.h"
#include "randStruct.h"




void _3DXY::warmup(Lattice3DXY& lat,Cluster&clust,long double beta,RandStruct& rand,int N){
	long double Nspins = lat.L*lat.L*lat.L;
	long double fliptries = 0;
	long double clusts = 0;
	while ((fliptries/Nspins) < N){
		clusts += 1.0L;
		fliptries +=(long double) cluster3DXY(lat,clust,beta,rand);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = clusts;
		lat.Neqsweeps = ((long double)fliptries)/((long double)Nspins);
		lat.warmedUp = true;
	}
}
void _3DXY::warmupMetro(Lattice3DXY& lat,long double beta,RandStruct&rand,int N){
	for (int i = 0; i < N; i++){
		metrosweep3DXY(lat,beta,rand);
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

void _3DXY::wolffHistJob(long double L){
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
	int 		Nruns=			1;
	Lattice3DXY lat(L,cold);
	Cluster clust(L);
	RandStruct rand;
	long double beta = 1.0L/runTemp;
	warmup(lat,clust,beta,rand,(Neq));
	for (int i=0; i< Nruns; ++i){	
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
		warmup(lat,clust,beta,rand,Nbetw);
	}

}
void _3DXY::metroJob(long double L){

	long double 	runTemp = 		2.20200000000000L;
	int 		Neq=			20000;
	bool 		cold=			true;
	long double	Nsamp=			1000.0L;
	int 		Nbetw=			100;
	int 		Nruns=			1000;
	Lattice3DXY lat(L,cold);
	RandStruct rand;
	long double beta = 1.0L/runTemp;
	warmupMetro(lat,beta,rand,(Neq-Nbetw));
	for (int i=0; i< Nruns; ++i){	
		warmupMetro(lat,beta,rand,Nbetw);
		metroRun3DXY(lat,Nsamp,runTemp);
	}
}
