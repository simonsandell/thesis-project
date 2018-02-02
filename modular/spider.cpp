#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;

//main
int main(int argc, char* argv[]){

	//set precision of cout
	cout.precision(17);


	// set up run paramters
	//
	//wolffHistRun(double L,  double N_equil_sweeps,  double N_samples,  bool cold,  double *Temperatures, int N_temps );
	//wolffRun(    double L,  double N_equil_sweeps,  double N_samples,  bool cold,  double Temperature );
	//
		double L = 4.0;
		double N_equil_sweeps = 1000.0;
		double N_samples = 2000.0;
		bool coldStart = true;
		int N_runs = 100;

		double T = 	2.10;
		double dT = 	0.01;
		int N_temps = 10;
		double Temps[N_temps];
		for (int k = 0; k < N_temps; ++k){
			Temps[k] = T;
			T = T + dT;
		}

		for ( int i = 0; i< N_runs; ++i){
			//regular run
			
			for (int j = 0;j< N_temps; ++j){
				wolffRun(L,N_equil_sweeps,N_samples,coldStart,Temps[j]);
			}
			
			//hist run
			//wolffHistRun(L,N_equil_sweeps,N_samples,coldStart,Temps,N_temps);
		}



}
