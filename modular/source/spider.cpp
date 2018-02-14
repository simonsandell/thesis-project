#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "ioFuncs.h"
#include "latticeOps.h"
#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

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
	long double 	Nreps = 		10000.0L;
	long double	startT=			2.200L;
	long double	endT=			2.204L;
	long double	Ntemps=			30.0L;
	long double	Neq=			6000.0L;
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
	long double runTemp = Trange[(int)(Ntemps/2)];

	bool save;
	long double ***lattice;

	//Initial warmups
	if (runNumber == "saveWarmup"){
		lattice = newLattice(4.0L,cold);	
		save = true;
		warmup(L,lattice,Neq,runTemp,save);
		L = 8.0L;
		lattice = newLattice(L,cold);
		warmup(L,lattice,Neq,runTemp,save);
		exit(0);
	}

	long double Neqsw;
	long double Neqcl;

	save = false;
	L = 4.0L;
	lattice = getLattice(L,Neqsw,Neqcl);
	for (int i = 0; i< Nreps; ++i){
		warmup(L,lattice,100,runTemp,save);
		wolffHistRun(L,lattice,Neqsw,Neqcl,Nsamp,cold,Trange,Ntemps,runTemp);
	}
	L = 8.0L;
	lattice = getLattice(L,Neqsw,Neqcl);
	for (int i = 0; i< Nreps; ++i){
		warmup(L,lattice,100,runTemp,save);
		wolffHistRun(L,lattice,Neqsw,Neqcl,Nsamp,cold,Trange,Ntemps,runTemp);
	}
}
