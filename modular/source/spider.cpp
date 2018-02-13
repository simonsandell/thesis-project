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
	// 
	//set precision of cout
	if (argc != 10){
		cout << "wrong number of arguments" << endl;
		exit(-1);
	}

	long double runType = stod(argv[1]);
	long double L= stod(argv[2]);
	long double startT= stod(argv[3]);
	long double endT= stod(argv[4]);
	long double Ntemps= stod(argv[5]);
	long double Neq= stod(argv[6]);
	long double Nsamp= stod(argv[7]);
	long double icold= stod(argv[8]);
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
	// determine if saving warmup, loading warmup, or warming up and running.
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
}
