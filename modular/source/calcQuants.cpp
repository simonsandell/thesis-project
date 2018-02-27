#include <cmath>
#include <iostream>

#include "calcQuants.h"
#include "latticeOps.h"
#include "latticeStruct.h"



long double calcSinX(long double ***lattice,long double  L){
	long double sum = 0.0L;
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
	long double sum = 0.0L;
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
	long double sum = 0.0L;
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
	long double ret = 0.0L;
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
	long double ret = 0.0L;
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
	long double en = 0.0L;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(lattice,L,i,j,k);
			}
		}
	}
	en = 0.5L*en;
	return en;
}

void testConsistent(Lattice lat){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testSinX = calcSinX(lat.theLattice,lat.L);
	long double testSinY = calcSinY(lat.theLattice,lat.L);
	long double testSinZ = calcSinZ(lat.theLattice,lat.L);
	long double testEn = calcEn(lat.theLattice,lat.L);
	long double testXMag = calcXMag(lat.theLattice,lat.L);
	long double testYMag = calcYMag(lat.theLattice,lat.L);
	long double& TotEn = lat.energy;
	long double& TotXMag= lat.xmag;
	long double& TotYMag= lat.ymag;
	long double& TotSinX= lat.sinx;
	long double& TotSinY = lat.siny;
	long double& TotSinZ = lat.sinz;
	std::cout <<std::fixed<< TotEn - testEn << "  E    "<< TotEn << " "<< testEn << std::endl;
	std::cout <<std::fixed<< TotXMag - testXMag << "  X    "<< TotXMag << " "<< testXMag << std::endl;
	std::cout <<std::fixed<< TotYMag - testYMag << "  Y    "<< TotYMag << " "<< testYMag << std::endl;
	std::cout <<std::fixed<< TotSinX - testSinX << "  Sx    "<< TotSinX << " "<< testSinX << std::endl;
	std::cout <<std::fixed<< TotSinY - testSinY << "  Sy    "<< TotSinY << " "<< testSinY << std::endl;
	std::cout <<std::fixed<< TotSinZ - testSinZ << "  Sz    "<< TotSinZ << " "<< testSinZ << std::endl;
	//new test of magnetization
	long double sitemag;
	long double accum = 0.0L;
	for (int i = 0; i< lat.L; ++i){
		for (int j = 0; j< lat.L; ++j){
			for (int k = 0; k<lat.L; ++k){	
				sitemag = std::pow(sin(lat.theLattice[i][j][k]),2.0L) + 
					std::pow(cos(lat.theLattice[i][j][k]),2.0L);
				std::cout << std::fixed << sitemag << std::endl;
				accum += std::abs(sitemag - 1.0L);
			}
		}
	}
	std::cout << std::fixed << accum << std::endl;
}
