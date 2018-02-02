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

	//generate random seed from system and initialize random number generator

	//set system size and temperature from input arguments
	if (argc < 2){
		cout << "input arguments: L N_eq N_samp coldStart T_1 T_2 T_3 ..." << endl;
		exit(0);
	}
	double L = stod(argv[1]);
	double N_equil_sweeps = stod(argv[2]);
	double N_samples = stod(argv[3]);
	double cold = stod(argv[4]);
	int N_temps = 1;
	double Temperatures[argc - 5] = {};
	N_temps = argc - 5;
	for (int i = 0; i< N_temps; ++i){
		Temperatures[i] = stod(argv[i+5]);
	}


	wolffHistRun(L, N_equil_sweeps, N_samples,cold,Temperatures,N_temps);
	wolffRun(L, N_equil_sweeps, N_samples,cold,Temperatures[0]);



}
