#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>

#include "latticeOps.h"
#include "randStruct.h"
#include "latticeStruct.h"

void metrosweep(Lattice lat,long double beta,RandStruct randgen){
	long double prob;
	long double u;
	int s1;
	int s2;
	int s3;
	long double angleBefore;
	long double angleAfter;
	long double enBefore;
	long double enAfter;
	for (int i = 0; i<lat.Nspins; ++i){
		//select random angle in the range [-PI,PI]
		u = -(long double)M_PI + 2.0L*(long double)M_PI*randgen.rnd(); 
		//select random spin
		s1 = lat.L*randgen.rnd();
		s2 = lat.L*randgen.rnd();
		s3 = lat.L*randgen.rnd();
		//calculate energy difference and probability of flipping
		//and try to flip
		angleBefore = lat.theLattice[s1][s2][s3];
		angleAfter = angleBefore + u;
		enBefore = siteEnergy(lat.theLattice,lat.L,s1,s2,s3);
		lat.theLattice[s1][s2][s3] = angleAfter;
		enAfter = siteEnergy(lat.theLattice,lat.L,s1,s2,s3);
		lat.theLattice[s1][s2][s3] = angleBefore;
		prob = exp(-beta*(enAfter - enBefore));
		if (randgen.rnd() < prob){
			lat.theLattice[s1][s2][s3] = angleAfter;
			lat.energy += enAfter - enBefore;
			lat.xmag += cos(angleAfter) - cos(angleBefore);
			lat.ymag += sin(angleAfter) - sin(angleBefore);
			lat.sinx += sinX(lat.theLattice,lat.L,s1,s2,s3,angleAfter) - sinX(lat.theLattice,lat.L,s1,s2,s3,angleBefore);
			lat.siny += sinY(lat.theLattice,lat.L,s1,s2,s3,angleAfter) - sinY(lat.theLattice,lat.L,s1,s2,s3,angleBefore);
			lat.sinz += sinZ(lat.theLattice,lat.L,s1,s2,s3,angleAfter) - sinZ(lat.theLattice,lat.L,s1,s2,s3,angleBefore);
		}
	}
}

