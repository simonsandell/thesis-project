#include <cmath>
#include <iostream>

#include "latticeOps.h"



//print lattice
void printLattice(double ***lattice,double &L){
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


//testing functions
double calcSinX(double ***lattice,double &L){
	double sum = 0.0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[(i+1)%(int)L][j][k]);
			}
		}
	}
	return sum;
}

double calcXMag(double ***lattice,double&L){
	double ret = 0.0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[i][j][k]);
			}
		}
	}
	return ret;
}
double calcYMag(double ***lattice,double&L){
	double ret = 0.0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[i][j][k]);
			}
		}
	}
	return ret;
}

double calcMag(double ***lattice,double&L){
	double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

double calcEn(double ***lattice,double&L){
	double en = 0.0;
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

void testConsistent(double ***lattice,double&L,double&TotEn,double&TotXMag,double&TotYMag,double&TotSinX){

	   double tSinX = calcSinX(lattice,L);
	   double testEn = calcEn(lattice,L);
	   double testXMag = calcXMag(lattice,L);
	   double testYMag = calcYMag(lattice,L);
	   double testMag = calcMag(lattice,L);
	   std::cout << TotEn - testEn << " E" << std::endl;
	   std::cout << TotXMag - testXMag << " X" << std::endl;
	   std::cout << TotYMag - testYMag << " Y" << std::endl;
	   std::cout << TotSinX - tSinX << " S" << std::endl;
}
