#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>

#include "latticeOps.h"

void metrosweep(long double***lattice,long double&L,long double&beta,long double&TotXMag,long double&TotYMag,long double&TotEn,long double &TotSinX,long double &TotSinY,long double &TotSinZ,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng){
	long double prob;
	long double u;
	int s1;
	int s2;
	int s3;
	long double angleBefore;
	long double angleAfter;
	long double enBefore;
	long double enAfter;
	for (int i = 0; i<(L*L*L); ++i){
		//select random angle in the range [-PI,PI]
		u = -M_PI + 2.0*M_PI*dist(eng); 
		//select random spin
		s1 = L*dist(eng);
		s2 = L*dist(eng);
		s3 = L*dist(eng);
		//calculate energy difference and probability of flipping
		//and try to flip
		angleBefore = lattice[s1][s2][s3];
		angleAfter = angleBefore + u;
		enBefore = siteEnergy(lattice,L,s1,s2,s3);
		lattice[s1][s2][s3] = angleAfter;
		enAfter = siteEnergy(lattice,L,s1,s2,s3);
		lattice[s1][s2][s3] = angleBefore;
		prob = exp(-beta*(enAfter - enBefore));
		if (dist(eng) < prob){
			lattice[s1][s2][s3] = angleAfter;
			TotEn += enAfter - enBefore;
			TotXMag += cos(angleAfter) - cos(angleBefore);
			TotYMag += sin(angleAfter) - sin(angleBefore);
			TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
			TotSinY += sinY(lattice,L,s1,s2,s3,angleAfter) - sinY(lattice,L,s1,s2,s3,angleBefore);
			TotSinZ += sinZ(lattice,L,s1,s2,s3,angleAfter) - sinZ(lattice,L,s1,s2,s3,angleBefore);
		}
	}
}

