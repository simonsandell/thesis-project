#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

void whr( long double L,long double N_equil,long double N_samp,bool cold, long double* Temps,int N_temps){
	int nRuns = N_temps/2;
	int index = N_temps/4;
	for (int i = 0; i< nRuns; ++i){
		index++;
		wolffHistRun(L,N_equil,N_samp,cold,Temps,N_temps,Temps[index]);
	}
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
	
	cout.precision(dbl::max_digits10 + 2);

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
	long double *Trange = getTrange(startT,endT,int(Ntemps));
	//determine runtype and run
	if (runType == 0.0L) {
		wr(L,Neq,Nsamp,cold,Trange,Ntemps);
	}
	else if (runType == 1.0L) {
		whr(L,Neq,Nsamp,cold,Trange,Ntemps);
	}
}
