#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

void whr(int reps, double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	for ( int i = 0; i< reps;++i){
		wolffHistRun(L,N_equil,N_samp,cold,Temps,N_temps);
	}
}
void wr(int reps, double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	//regular run
	double Temp;
	for (int j = 0;j< reps; ++j){
		for (int i = 0; i< N_temps; ++i){
			Temp = Temps[i];
			wolffRun(L,N_equil,N_samp,cold,Temp);
		}
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

	//set precision of cout
	cout.precision(17);

	// set up run paramters
	//void whr(int reps, double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	//void wr(int reps, double L,double N_equil,double N_samp,bool cold, double* Temps,int N_temps){
	double *Trange = getTrange(2.2,2.22,32);
	whr(1,8,2000,3000,false,Trange,32);


}
