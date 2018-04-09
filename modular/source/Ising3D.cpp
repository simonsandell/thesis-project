#include <string>
#include "Ising3D.h"
#include "Ising3D/Ising3Dio.h"
#include "Ising3D/Ising3Dlattice.h"
#include "Ising3D/Ising3DrunWolff.h"
#include "Ising3D/Ising3Dwolff.h"

#include "clusterStruct.h"
#include "randStruct.h"

void Ising3D::warmup(LatticeIsing3D& lat,long double N){
	long double steps = 0.0L;
	long double NClusts = 0.0L;
	long double NSweeps = 0.0L;
	while (NSweeps < N){
		steps =(long double) clusterIsing3D(lat);
		NClusts+= 1.0L;
		NSweeps += (steps/lat.Nspins);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = NClusts;
		lat.Neqsweeps = NSweeps;
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

void Ising3D::wolffHistJob(long double L,std::string maxepath,std::string warmlatpath){
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
	long double 	Neq=			100000.0L;
	bool 		cold=			true;
	long double	Nsamp=			100000.0L;
	long double 	Nbetw=			100;
	int 		Nruns=			100;
	long double beta = 1.0L/runTemp;

	Cluster clust(L);
	RandStruct rand;

	LatticeIsing3D lat(L,cold,beta,rand,clust,maxepath,warmlatpath);
	warmup(lat,(Neq));
	for (int i=0; i< Nruns; ++i){	
		wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps,runTemp);
		warmup(lat,Nbetw);
	}
}
void Ising3D::teqRun(long double L, bool cold){
	long double runTemp = 4.50000000000000L;

	int 		Ntemps=			1;
	long double* Trange;
	Trange = new long double[1];
	Trange[0] = runTemp;
	long double	Nsamp=			2.0L;
	int 		Ndoubles=		18;
	long double beta = 1.0L/runTemp;
	Cluster clust(L);
	RandStruct rand;
	LatticeIsing3D lat(L,cold,beta,rand,clust,"/cfs/klemming/scratch/s/simsan/maxE/Ising3D/","");
	wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps,runTemp);
	for (int i=0; i< Ndoubles; ++i){	
		wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps,runTemp);
		Nsamp = Nsamp*2;
	}

}















