#include <string>
#include <iostream>
#include "Ising3D/Ising3Dio.h"
#include "Ising3D/Ising3Dlattice.h"
#include "Ising3D/Ising3DrunWolff.h"
#include "Ising3D/Ising3Dwolff.h"
#include "Ising3D.h"
#include "clusterStruct.h"
#include "randStruct.h"

void Ising3D::warmup(LatticeIsing3D& lat,long double N){
	long double steps = 0.0L;
	long double NClusts = 0.0L;
	long double NSweeps = 0.0L;
	while (NSweeps < N){
		steps = clusterIsing3D(lat);
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
	long double runTemp = 4.51000000000000L;

	long double	startT=			4.49000L;
	long double	endT=			4.53000L;
	int 		Ntemps=			101;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrangeIsing3D(startT,endT,Ntemps);
	}
	long double 	Neq=			100000.0L;
	bool 		cold=			true;
	long double	Nsamp=			1000.0L;
	long double 	Nbetw=			100;
	long double beta = 1.0L/runTemp;

	Cluster clust(L);
	RandStruct rand;

	LatticeIsing3D lat(L,cold,beta,rand,clust,maxepath,warmlatpath);
	warmup(lat,Neq);
	while(true){	
		wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps);
		warmup(lat,Nbetw);
	}
}

void Ising3D::teqJob(long double L,bool cold,std::string maxepath,std::string warmlatpath){
	long double runTemp = 4.510000000000000L;
	long double beta = 1.0L/runTemp;
	Cluster c(L);
	RandStruct r;
	LatticeIsing3D lat(L,cold,beta,r,c,maxepath,warmlatpath);
	
	int Ntemps = 1;
	long double Trange[1] = {runTemp};
	long double Nsamp = 2;
	wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps);
	wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps);
	for (int i = 0; i< 18; ++i){
		Nsamp *= 2.0L;
		wolffHistRunIsing3D(lat,Nsamp,Trange,Ntemps);
	}
}

void Ising3D::warmupJob(long double L, std::string maxepath,std::string warmlatpath){
	long double runTemp = 4.5100000000000000L;
	long double beta = 1.0L/runTemp;
	bool cold = true;
	Cluster c(L);
	RandStruct r;
	LatticeIsing3D lat(L,cold,beta,r,c,maxepath,warmlatpath);
	//lat.loadLattice();
	long double Neq = 1000.0L;
	while (lat.NTotSweeps < 100000.0L){
		warmup(lat,Neq);
		lat.saveLatticeAs("latest");
		std::cout << lat.L << " energy " << lat.energy << std::endl;
		std::cout << lat.L << " NTotSweeps " << lat.NTotSweeps << std::endl;
	}
}













