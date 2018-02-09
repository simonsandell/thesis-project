#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

void whr( long double L,long double N_equil,long double N_samp,bool cold, long double* Temps,int N_temps,long double runTemp){
	wolffHistRun(L,N_equil,N_samp,cold,Temps,N_temps,runTemp);
}
void wr( long double L,long double N_equil,long double N_samp,bool cold, long double* Temps,int N_temps){
	//regular run
	long double Temp;
	for (int i = 0; i< N_temps; ++i){
		Temp = Temps[i];
		wolffRun(L,N_equil,N_samp,cold,Temp);
	}
}
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
	typedef numeric_limits<long double> dbl;

	cout.precision(dbl::max_digits10 + 5);

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
	//determine runtype and run
	long double* Trange;
	if (abs(Ntemps - 1) < 0.1) {
		Trange = new long double[1];
		Trange[0] = startT;
	}
	else {
		Trange = getTrange(startT,endT,int(Ntemps));
	}

	if (runType == 0.0L) {
		wr(L,Neq,Nsamp,cold,Trange,Ntemps);
	}
	else if (runType == 1.0L) {
		//long double runTemp = 2.2020L;
		long double runTemp = Trange[(int)(Ntemps/2)];
		whr(L,Neq,Nsamp,cold,Trange,Ntemps,runTemp);
	}
}
