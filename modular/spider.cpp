#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

void whr( double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	int nRuns = N_temps/2;
	int index = N_temps/4;
	for (int i = 0; i< nRuns; ++i){
		index++;
		wolffHistRun(L,N_equil,N_samp,cold,Temps,N_temps,Temps[index]);
	}
}
void wr( double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	//regular run
	double Temp;
	for (int i = 0; i< N_temps; ++i){
		Temp = Temps[i];
		wolffRun(L,N_equil,N_samp,cold,Temp);
	}
}
double * getTrange(double start, double end, int N){
	double dt = (end-start)/((double)N-1.0);
	double *T = new double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (double)i*dt;
	}
	return T;
}


//main
int main(int argc, char* argv[]){
// input args :: 'wolff'/'hist' L startT endT Tnum Neq Nsamp Cold
// 
	//set precision of cout
	
	cout.precision(17);

	double runType = stod(argv[1]);
	double L= stod(argv[2]);
	double startT= stod(argv[3]);
	double endT= stod(argv[4]);
	double Ntemps= stod(argv[5]);
	double Neq= stod(argv[6]);
	double Nsamp= stod(argv[7]);
	double icold= stod(argv[8]);

	//set cold start bool
	bool cold = false;
	if (icold == 1.0){
		cold = true;
	}
	//generate temperature range
	double *Trange = getTrange(startT,endT,int(Ntemps));
	//determine runtype and run
	if (runType == 0.0) {
		wr(L,Neq,Nsamp,cold,Trange,Ntemps);
	}
	else if (runType == 1.0) {
		whr(L,Neq,Nsamp,cold,Trange,Ntemps);
	}
}
