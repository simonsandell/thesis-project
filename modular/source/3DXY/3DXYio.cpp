#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "3DXYio.h"
#include "3DXYlattice.h"
#include "../avgStruct.h"
#include "../randStruct.h"
#include "../clusterStruct.h"
#include "../ioHandle.h"

//print lattice
void printLattice3DXY(long double ***lattice,long double  L){
	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			for(int k =0; k<L; ++k){
				std::cout << lattice[i][j][k] << " ";
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}
}

void print3DXYOutput(Lattice3DXY &lat, long double T,avgStruct avgs, long double bin, long double dbdt, long double xi, long double rs){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);
	std::stringstream sstrm;
	sstrm.precision(dbl::max_digits10 + 5);

	sstrm << std::fixed << lat.L << " ";				//0
	sstrm << std::fixed << T << " ";				//1
	sstrm << std::fixed << lat.Neqsweeps << " ";			//2
	sstrm << std::fixed << lat.Neqclusts << " ";			//3
	sstrm << std::fixed << lat.NTotSweeps << " ";			//4
	sstrm << std::fixed << lat.NTotClusts << " ";			//5
	sstrm << std::fixed << lat.coldstart << " ";			//6
	sstrm << std::fixed << avgs.e	<< " ";				//7
	sstrm << std::fixed << avgs.e2	<< " ";				//8
	sstrm << std::fixed << avgs.m	<< " ";				//9
	sstrm << std::fixed << avgs.m2	<< " ";				//10
	sstrm << std::fixed << avgs.m4	<< " ";				//11
	sstrm << std::fixed << avgs.m2e	<< " ";				//12
	sstrm << std::fixed << avgs.m4e	<< " ";				//13
	sstrm << std::fixed << avgs.s2x	<< " ";				//14
	sstrm << std::fixed << avgs.s2y	<< " ";				//15
	sstrm << std::fixed << avgs.s2z << " ";				//16
	sstrm << std::fixed << bin	<< " ";				//17
	sstrm << std::fixed << dbdt	<< " ";				//18
	sstrm << std::fixed << xi	<< " ";				//19
	sstrm << std::fixed << rs	<< " ";				//20
	sstrm << std::fixed << avgs.exp << " ";				//21
	sstrm << std::endl;				
	lat.oPer.addLine(sstrm.str());
}



