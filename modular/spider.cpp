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
	double N_samples = 1500.0;
	bool coldStart = true;
	int N_runs = 1;

	double T = 	2.200;
	double dT = 	0.001;
	int N_temps = 20;
	double Temps[20] = {2.2010,2.2020,2.2030,2.2040,2.2050,2.2060,2.2070,2.2080,2.2090,2.2100,2.2110,2.2120,2.2130,2.2140,2.2150,2.2160,2.2170,2.2180,2.2190,2.2200
	};
	double regTemps[8] = {1.8000,1.9000,2.0000,2.1000,2.2000,2.3000,2.4000,2.5000};

	for ( int i = 0; i< N_runs; ++i){
		//regular run
//		for (int j = 0;j< 8; ++j){
//			wolffRun(L,N_equil_sweeps,N_samples,coldStart,regTemps[j]);
//			wolffRun(8.0,N_equil_sweeps,N_samples,coldStart,regTemps[j]);
		//	wolffRun(16.0,N_equil_sweeps,N_samples,coldStart,regTemps[j]);
//		}
		wolffHistRun(4.0,N_equil_sweeps,N_samples,coldStart,Temps,N_temps);
		wolffHistRun(8.0,N_equil_sweeps,N_samples,coldStart,Temps,N_temps);
		//wolffHistRun(16.0,N_equil_sweeps,N_samples,coldStart,Temps,N_temps);

	}
}
