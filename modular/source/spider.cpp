#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "ioFuncs.h"
#include "calcQuants.h"
#include "latticeOps.h"
#include "latticeStruct.h"
#include "metroRun.h"
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


	long double	startT=			2.20150L;
	long double	endT=			2.20350L;
	int 		Ntemps=			21.0L;

	long double 	L =			4.0L;
	long double	Neq=			10000.0L;
	bool 		cold=			false;

	long double	Nsamp=			1000.0L;
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
	bool save = false;
	//
	//End of parameters
	//
	
	
	Lattice lat(L,cold);
	printLattice(lat.theLattice,lat.L);
	saveLattice(lat);

	lat = getLattice((int)L);
	testConsistent(lat);
	printLattice(lat.theLattice,lat.L);

	wolffHistRun(lat,Nsamp,Trange,Ntemps,runTemp);
	printLattice(lat.theLattice,lat.L);

	testConsistent(lat);








}

