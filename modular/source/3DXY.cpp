
#include "3DXY/3DXYio.h"
#include "3DXY/3DXYlattice.h"
#include "3DXY/3DXYrunMetro.h"
#include "3DXY/3DXYmetro.h"
#include "3DXY/3DXYrunWolff.h"
#include "3DXY/3DXYwolff.h"
#include "3DXY.h"
#include "clusterStruct.h"
#include "randStruct.h"




void _3DXY::warmup(Lattice3DXY& lat,Cluster&clust,long double beta,RandStruct& rand,long double N){
	long double steps;
	long double NClusts = 0;
	long double NSweeps = 0;
	while (NSweeps < N){
		steps =(long double) cluster3DXY(lat,clust,beta,rand);
		NClusts += 1.0L;
		NSweeps += (steps/lat.Nspins);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = NClusts;
		lat.Neqsweeps = NSweeps;
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
	long double runTemp = 2.20200000000000L;

	long double	startT=			2.20150L;
	long double	endT=			2.20300L;
	int 		Ntemps=			31;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrange(startT,endT,int(Ntemps));
	}
	long double 	Neq=			100000.0L;
	bool 		cold=			true;
	long double	Nsamp=			100000.0L;
	long double 	Nbetw=			100.0L;
	int 		Nruns=			100;
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
void _3DXY::teqRun(long double L,bool cold){
	long double runTemp = 2.20200000000000L;
	int 		Ntemps=			1;
	long double* Trange;
	Trange = new long double[1];
	Trange[0] = runTemp;
	long double	Nsamp=			2.0L;
	int 		Ndoubles=		18;
	Lattice3DXY lat(L,cold);
	wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
	for (int i=0; i< Ndoubles; ++i){	
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
		Nsamp = Nsamp*2;
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
