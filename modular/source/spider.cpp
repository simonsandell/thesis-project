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
	// input args :: 'wolff'/'hist' L startT endT Tnum Neq Nsamp Cold
	long double runType ;
	long double L;
	long double startT;
	long double endT;
	long double Ntemps;
	long double Neq;
	long double Nsamp;
	long double icold;
	// 
	//set precision of cout
	if (argc != 10){
		//cout << "wrong number of arguments" << endl;
		//exit(-1);
		runType = 1.0L;
		L= 4.0L;
		startT=2.201L;
		endT=2.203L;
		Ntemps=30.0L;
		Neq=6000.0L;
		Nsamp=20000.0L;
		icold=1.0L;
	}
	else{

		runType = stod(argv[1]);
		L= stod(argv[2]);
		startT= stod(argv[3]);
		endT= stod(argv[4]);
		Ntemps= stod(argv[5]);
		Neq= stod(argv[6]);
		Nsamp= stod(argv[7]);
		icold= stod(argv[8]);
	}
	//set cold start bool
	bool cold = false;
	if (icold == 1.0L){
		cold = true;
	}
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
	//warmup for 6000 sweeps
	warmup(L,Neq,cold,runTemp,true);
	long double Neqsw;
	long double Neqcl;
	long double *** lattice;
	for (int i = 0; i< 5; ++i){
		lattice = getLattice(L,Neqsw,Neqcl);
		wolffHistRun(L,lattice,Neqsw,Neqcl,Nsamp,cold,Trange,Ntemps,runTemp);
	}
	L = 8.0L;
	warmup(L,Neq,cold,runTemp,true);
	for (int i = 0; i< 10000; ++i){
		lattice = getLattice(L,Neqsw,Neqcl);
		wolffHistRun(L,lattice,Neqsw,Neqcl,Nsamp,cold,Trange,Ntemps,runTemp);
	}




	// determine if saving warmup, loading warmup, or warming up and running.
	/*
	std::string argwarmup= argv[9];
	if (argwarmup == "save") {
		warmup(L,Neq,cold,runTemp,true);
	}
	else if (argwarmup == "load"){
		long double N_equil_sweeps;
		long double N_equil_clusters;
		long double ***lattice = getLattice(L,N_equil_sweeps,N_equil_clusters);
		if (runType == 1.0L){
			wolffHistRun(L,lattice,N_equil_sweeps,N_equil_clusters,Nsamp,cold,Trange,Ntemps,runTemp);
		}
	}
	*/
}
