#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>

#include "randStruct.h"
#include "3DXYlattice.h"

void updateValsM(Lattice& lat,long double e0,long double e1,
		long double a0,long double a1,
		long double sx0,long double sx1,
		long double sy0,long double sy1,
		long double sz0,long double sz1){

	lat.energy+= e1;
	lat.energy += -e0;
	lat.xmag+= cos(a1);
	lat.xmag+= -cos(a0);
	lat.ymag+= sin(a1);
	lat.ymag+= -sin(a0);
	lat.sinx+= sx1;
	lat.sinx+= -sx0;
	lat.siny+= sy1;
	lat.siny+= -sy0;
	lat.sinz+= sz1;
	lat.sinz+= -sz0;
}
void metrosweep(Lattice& lat,long double beta,RandStruct randgen){
	long double prob;
	long double u;
	int s1;
	int s2;
	int s3;
	long double angleBefore;
	long double angleAfter;
	long double enBefore;
	long double enAfter;
	long double sxBef,sxAft,syBef,syAft,szBef,szAft;
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
		enBefore = lat.siteEnergy(s1,s2,s3);
		lat.theLattice[s1][s2][s3] = angleAfter;
		enAfter = lat.siteEnergy(s1,s2,s3);
		lat.theLattice[s1][s2][s3] = angleBefore;
		prob = exp(-beta*(enAfter - enBefore));
		if (randgen.rnd() < prob){
			//flip spin
			lat.theLattice[s1][s2][s3] = angleAfter;
			sxBef =	 lat.sinX(s1,s2,s3,angleBefore);
			sxAft= lat.sinX(s1,s2,s3,angleAfter);
			syBef= lat.sinY(s1,s2,s3,angleBefore);
			syAft = lat.sinY(s1,s2,s3,angleAfter);
			szBef= lat.sinZ(s1,s2,s3,angleBefore);
			szAft = lat.sinZ(s1,s2,s3,angleAfter);
			updateValsM(lat,enBefore,enAfter,
					angleBefore,angleAfter,
					sxBef,sxAft,
					syBef,syAft,
					szBef,szAft);
			}

		}
	}

