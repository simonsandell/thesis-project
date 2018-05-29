#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>
#include <iostream>

#include "3DXYlattice.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

long double getProb(long double u, long double angleParent, long double angle,long double beta){
	long double prob = 1.0L - exp(2.0L*beta*cos(angleParent - u)*cos(angle -u));
	if (prob < 0.0L){ 
		return 0.0L;
	}
	else if (prob > 1.0L){
		return 1.0L;
	}
	return prob;
}

void updateVals(Lattice3DXY& lat,long double e0,long double e1,
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

long double cluster3DXY(Lattice3DXY& lat){

	long double time = 1.0L;
	//select random plane and random staring spin
	long double u = -(long double)M_PI + 2.0L*((long double)M_PI)*lat.rand.rnd();
	unsigned long int s1 = lat.Nspins*lat.rand.rnd();
	// save angle and energy before flipping
	long double angleBefore = lat.theLattice[s1];
	long double enBefore = lat.siteEnergy(s1);
	long double angleAfter = (long double)M_PI + 2.0L*u - angleBefore;
	//reflect spin and mark as part of cluster
	lat.theLattice[s1] = angleAfter;
	lat.clust.theCluster[s1] = true;
	//update energy, mag etc..
	long double enAfter = lat.siteEnergy(s1);
	long double sxBef = lat.sinX(s1,angleBefore);
	long double sxAft = lat.sinX(s1,angleAfter);
	long double syBef = lat.sinY(s1,angleBefore);
	long double syAft = lat.sinY(s1,angleAfter);
	long double szBef = lat.sinZ(s1,angleBefore);
	long double szAft = lat.sinZ(s1,angleAfter);
	updateVals(lat,
			enBefore,enAfter,
			angleBefore,angleAfter,
			sxBef,sxAft,
			syBef,syAft,
			szBef,szAft);
	//find indices of nearest neighbours
	//make a list for perimeter spins
	int n = 6;// number of neighbours, should add this as constant in Lattice3DXY...
	std::vector<std::tuple<unsigned long int,long double>> perimeter;
	std::tuple<unsigned long int,long double> neigh;
	for (int i = 0; i < 6; ++i){
		neigh = std::make_tuple(lat.Neighbours[s1][i],angleAfter);
		perimeter.push_back(neigh);
	}
	std::tuple<unsigned long int,long double> current;
	long double prob = 0.0L;
	long double rand = 0.0L;
	while (n > 0){
		//pick out the last element 
		current = perimeter.back();
		perimeter.pop_back();
		n -= 1;
		//test that it is not already part of cluster
		if (!lat.clust.theCluster[std::get<0>(current)]){

			//increase time for every tested spin
			//
			time = time +1.0L;

			//get its current angle;
			//
			angleBefore = lat.theLattice[std::get<0>(current)];

			//calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
			prob = getProb(u,std::get<1>(current) ,angleBefore,lat.beta);
			rand = lat.rand.rnd();
			if ( rand < prob) {
				//get energy before reflecting
				//
				enBefore = lat.siteEnergy(std::get<0>(current));

				//get new angle
				angleAfter = (long double)M_PI + 2.0L*u - angleBefore;

				//reflect and mark as added to cluster
				lat.theLattice[std::get<0>(current)] =angleAfter;
				lat.clust.theCluster[std::get<0>(current)] = true;

				//update energy and magnetization
				enAfter = lat.siteEnergy(std::get<0>(current));
				sxBef = lat.sinX(std::get<0>(current),angleBefore);
				sxAft = lat.sinX(std::get<0>(current),angleAfter);
				syBef = lat.sinY(std::get<0>(current),angleBefore);
				syAft = lat.sinY(std::get<0>(current),angleAfter);
				szBef = lat.sinZ(std::get<0>(current),angleBefore);
				szAft = lat.sinZ(std::get<0>(current),angleAfter);
				updateVals(lat,
						enBefore,enAfter,
						angleBefore,angleAfter,
						sxBef,sxAft,
						syBef,syAft,
						szBef,szAft);
				//go through neigbours of current
				for (int i = 0; i < 6; ++i){
					neigh = std::make_tuple(lat.Neighbours[std::get<0>(current)][i],angleAfter);
					//if a neighbour is not already part of the cluster, add it to perimeter list
					if (!lat.clust.theCluster[std::get<0>(neigh)] ){
						perimeter.push_back(neigh);
						n = n + 1;
					}
				}
			}
		}
	}
	//empty the cluster
	lat.clust.emptyCluster();	
	//return # of tested spins
	lat.NTotSweeps += time/lat.Nspins;
	lat.NTotClusts += 1;
	return time;
}
