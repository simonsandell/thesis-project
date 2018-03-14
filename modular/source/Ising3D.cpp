
#include "Ising3D.h"
#include "Ising3D/Ising3Dio.h"
#include "Ising3D/Ising3Dlattice.h"
#include "Ising3D/Ising3DrunWolff.h"
#include "Ising3D/Ising3Dwolff.h"

#include "clusterStruct.h"
#include "randStruct.h"

void Ising3D::warmup(LatticeIsing3D& lat,Cluster&clust,RandStruct& rand,int N){
	long double Nspins = lat.L*lat.L*lat.L;
	long double fliptries = 0;
	long double clusts = 0;
	while ((fliptries/Nspins) < N){
		clusts += 1.0L;
		fliptries +=(long double) clusterIsing3D(lat,clust,rand);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = clusts;
		lat.Neqsweeps = ((long double)fliptries)/((long double)Nspins);
		lat.warmedUp = true;
	}
}

//generate range of temperatures
long double * getTrangeIsing3D(long double start, long double end, int N){
	long double dt = (end-start)/((long double)N-1.0L);
	long double *T = new long double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (long double)i*dt;
	}
	return T;
}

void Ising3D::wolffHistJob(long double L){
	long double runTemp = 4.50000000000000L;

	long double	startT=			4.48500L;
	long double	endT=			4.51500L;
	int 		Ntemps=			41;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrangeIsing3D(startT,endT,int(Ntemps));
	}
	int 		Neq=			100000;
	bool 		cold=			true;
	long double	Nsamp=			100000.0L;
	int 		Nbetw=			100;
	int 		Nruns=			100;
	long double beta = 1.0L/runTemp;

	LatticeIsing3D lat(L,cold,beta);
	Cluster clust(L);
	RandStruct rand;
	warmup(lat,clust,rand,(Neq));
	for (int i=0; i< Nruns; ++i){	
		wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps,runTemp);
		warmup(lat,clust,rand,Nbetw);
	}

}

