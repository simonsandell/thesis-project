#include <iostream>
#include "printOutput.h"

void printOutput(long double L,long double T, long double E, long double M, long double bin, long double dbdt,long double xi,long double rs, long double N_eq_sweeps, int N_eq_clusts){

	std::cout << std::fixed << L << " ";
	std::cout << std::fixed << T << " ";
	std::cout << std::fixed << E << " ";
	std::cout << std::fixed << M << " ";
	std::cout << std::fixed << bin << " ";
	std::cout << std::fixed << dbdt << " ";
	std::cout << std::fixed << xi << " ";
	std::cout << std::fixed << rs << " ";
	std::cout << std::fixed << N_eq_sweeps << " "; 
	std::cout << std::fixed << N_eq_clusts << " "; 
	std::cout << std::fixed << std::endl;
}

