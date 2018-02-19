#include <cmath>
#include <iostream>

#include "calcQuants.h"
#include "latticeOps.h"

//print lattice
void printLattice(long double ***lattice,long double  L){
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			for(int k =0; k<L; ++k){
				std::cout << lattice[i][j][k];
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}
}


long double calcSinX(long double ***lattice,long double  L){
	long double sum = 0.0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[(i+1)%(int)L][j][k]);
			}
		}
	}
	return sum;
}
long double calcSinY(long double ***lattice,long double  L){
	long double sum = 0.0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[i][(j+1)%(int)L][k]);
			}
		}
	}
	return sum;
}
long double calcSinZ(long double ***lattice,long double  L){
	long double sum = 0.0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[i][j][(k+1)%(int)L]);
			}
		}
	}
	return sum;
}

long double calcXMag(long double ***lattice,long double L){
	long double ret = 0.0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[i][j][k]);
			}
		}
	}
	return ret;
}
long double calcYMag(long double ***lattice,long double L){
	long double ret = 0.0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[i][j][k]);
			}
		}
	}
	return ret;
}

long double calcMag(long double ***lattice,long double L){
	long double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

long double calcEn(long double ***lattice,long double L){
	long double en = 0.0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(lattice,L,i,j,k);
			}
		}
	}
	en = 0.5*en;
	return en;
}

void testConsistent(long double ***lattice,long double L,long double TotEn,long double TotXMag,long double TotYMag,long double TotSinX,long double TotSinY,long double TotSinZ){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testSinX = calcSinX(lattice,L);
	long double testSinY = calcSinY(lattice,L);
	long double testSinZ = calcSinZ(lattice,L);
	long double testEn = calcEn(lattice,L);
	long double testXMag = calcXMag(lattice,L);
	long double testYMag = calcYMag(lattice,L);
	std::cout <<std::fixed<< TotEn - testEn << " E"<< TotEn << " "<< testEn << std::endl;
	std::cout <<std::fixed<< TotXMag - testXMag << " X"<< TotXMag << " "<< testXMag << std::endl;
	std::cout <<std::fixed<< TotYMag - testYMag << " Y"<< TotYMag << " "<< testYMag << std::endl;
	std::cout <<std::fixed<< TotSinX - testSinX << " Sx"<< TotSinX << " "<< testSinX << std::endl;
	std::cout <<std::fixed<< TotSinY - testSinY << " Sy"<< TotSinY << " "<< testSinY << std::endl;
	std::cout <<std::fixed<< TotSinZ - testSinZ << " Sz"<< TotSinZ << " "<< testSinZ << std::endl;
}
