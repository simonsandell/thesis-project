#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "ioFuncs.h"
#include "calcQuants.h"
#include "latticeOps.h"
#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;
//warmup and save to file
void warmupandsave(long double L,long double Neq,bool cold,long double runTemp){
	long double ***lattice = newLattice(L,cold);
	bool save = true;
	long double Ncl;
	warmup(L,lattice,Neq,Ncl,runTemp,save);
}
//runhist
void runhist(long double L,long double***lattice,long double Neqsw,long double Neqcl,long double Nsamp,bool cold,long double*Trange,long double Ntemps,long double runTemp,long double Nreps,long double Nwarmup){
	long double Ncl;
	bool save = false;
	for (int i = 0; i< Nreps; ++i){
		cout << i << endl;
		warmup(L,lattice,Nwarmup,Ncl,runTemp,save);
		wolffHistRun(L,lattice,Neqsw,Neqcl,Nsamp,cold,Trange,Ntemps,runTemp);
	}
}
//runteq
void runteq(long double L,bool cold,long double runTemp){
	long double Nwarms= 4.0L;
	long double Neqsw;
	long double Neqcl;
	long double Nsamples = 1;
	bool save = false;

	long double ***lattice = newLattice(L,cold);
	for (int i =0; i<15; ++i){
		Neqsw = Nwarms;
		lattice= newLattice(L,cold);
		warmup(L,lattice,Neqsw,Neqcl,runTemp,save);
		wolffRun(L,lattice,Neqsw,Neqcl,Nsamples ,cold,runTemp);
		Nwarms *= 2.0L;
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
int main(int argc, char* argv[]){
	//
	//Set Run Parameters
	//
	//

	string runNumber = argv[1];

	long double 	L =			4.0L;
	long double	startT=			2.20150L;
	long double	endT=			2.20350L;
	long double	Ntemps=			21.0L;
	long double	Neq=			10000.0L;
	long double	Nsamp=			1000.0L;
	bool 		cold=			true;
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

	bool save;
	long double ***lattice;

	//Initial warmups
	if (runNumber == "saveWarmup"){
		L = 4.0L;
		warmupandsave(L,Neq,cold,runTemp);
		L = 8.0L;
		warmupandsave(L,Neq,cold,runTemp);
		L = 16.0L;
		warmupandsave(L,Neq,cold,runTemp);
		exit(0);
	}
	if (runNumber == "histRun"){
		long double Neqsw;
		long double Neqcl;
		long double Nreps = 1000.0L;
		long double Nwarmup = 100.0L;
		save = false;
		L = 4.0L;
		lattice = getLattice(L,Neqsw,Neqcl);
		runhist(L,lattice, Neqsw, Neqcl, Nsamp,cold,Trange, Ntemps, runTemp, Nreps, Nwarmup);
		L = 8.0L;
		lattice = getLattice(L,Neqsw,Neqcl);
		runhist(L,lattice, Neqsw, Neqcl, Nsamp,cold,Trange, Ntemps, runTemp, Nreps, Nwarmup);
	}
	if (runNumber == "teqRun"){
		bool cold;
		int N_teq = 100;
		for (int i = 0; i< N_teq; ++i){
			cold	= false;
			runteq(4.0L,cold,runTemp);
			runteq(8.0L,cold,runTemp);
			runteq(16.0L,cold,runTemp);
			cold = false;
			runteq(4.0L,cold,runTemp);
			runteq(8.0L,cold,runTemp);
			runteq(16.0L,cold,runTemp);
		}
	}
	if (runNumber == "normalRun"){
		long double Neqsw;
		long double Neqcl;
		long double Ncl;
		long double Nreps = 10000.0L;
		long double Nwarmup = 100.0L;
		L = 4.0L;
		lattice = getLattice(L,Neqsw,Neqcl);	
		for (int i = 0; i< Nreps; ++i){
			warmup(L,lattice,Nwarmup,Ncl,runTemp,save);
			wolffRun(L,lattice,Neqsw+Nwarmup,Neqcl+Ncl,Nsamp,cold,runTemp);
		}
		L = 8.0L;
		lattice = getLattice(L,Neqsw,Neqcl);	
		for (int i = 0; i< Nreps; ++i){
			warmup(L,lattice,Nwarmup,Ncl,runTemp,save);
			wolffRun(L,lattice,Neqsw+Nwarmup,Neqcl+Ncl,Nsamp,cold,runTemp);
		}
		L = 16.0L;
		lattice = getLattice(L,Neqsw,Neqcl);	
		for (int i = 0; i< Nreps; ++i){
			warmup(L,lattice,Nwarmup,Ncl,runTemp,save);
			wolffRun(L,lattice,Neqsw+Nwarmup,Neqcl+Ncl,Nsamp,cold,runTemp);
		}
	}
}

