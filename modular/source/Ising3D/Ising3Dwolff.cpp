#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>
#include <iostream>

#include "Ising3Dlattice.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

void updateVals(LatticeIsing3D& lat,long double addE,long double addM){
	lat.energy  += addE;
	lat.mag     += addM;
}

long double clusterIsing3D(LatticeIsing3D& lat){

	long double time = 1.0L;
	//select random staring spin
	int s1 = lat.L*lat.rand.rnd();
	int s2 = lat.L*lat.rand.rnd();
	int s3 = lat.L*lat.rand.rnd();
	// save spin and energy before flipping
	long double spinBefore = lat.theLattice[s1][s2][s3];
	long double enBefore = lat.siteEnergy(s1,s2,s3);
	long double spinAfter = -spinBefore;
	//reflect spin and mark as part of cluster
	lat.theLattice[s1][s2][s3] = spinAfter;
	lat.clust.theCluster[s1][s2][s3] = true;
	//update energy, mag etc..
	long double enAfter = lat.siteEnergy(s1,s2,s3);
	updateVals(lat,
			enBefore-enAfter,
			spinBefore-spinAfter);
	//find indices of nearest neighbours
	int n1m = (s1 -1 + lat.int_L )%lat.int_L;
	int n1p = (s1 +1 + lat.int_L )%lat.int_L;
	int n2m = (s2 -1 + lat.int_L )%lat.int_L;
	int n2p = (s2 +1 + lat.int_L )%lat.int_L;
	int n3m = (s3 -1 + lat.int_L )%lat.int_L;
	int n3p = (s3 +1 + lat.int_L )%lat.int_L;
	std::tuple<int,int,int,long double> neig1 = std::make_tuple(n1m,s2,s3,spinAfter);
	std::tuple<int,int,int,long double> neig2 = std::make_tuple(n1p,s2,s3,spinAfter);
	std::tuple<int,int,int,long double> neig3 = std::make_tuple(s1,n2m,s3,spinAfter);
	std::tuple<int,int,int,long double> neig4 = std::make_tuple(s1,n2p,s3,spinAfter);
	std::tuple<int,int,int,long double> neig5 = std::make_tuple(s1,s2,n3m,spinAfter);
	std::tuple<int,int,int,long double> neig6 = std::make_tuple(s1,s2,n3p,spinAfter);

	//make a list for perimeter spins
	std::vector<std::tuple<int,int,int,long double>> perimeter;
	//add neighbours to list
	perimeter.push_back(neig1);
	perimeter.push_back(neig2);
	perimeter.push_back(neig3);
	perimeter.push_back(neig4);
	perimeter.push_back(neig5);
	perimeter.push_back(neig6);
	unsigned long int n = 6;

	std::tuple<int,int,int,long double> current;
	long double rand = 0.0L;
	while (n > 0){
		//pick out the last element 
		current = perimeter.back();
		perimeter.pop_back();
		n -= 1;
		//test that it is not already part of cluster
		if (!lat.clust.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)]){

			//increase time for every tested spin
			//
			time += 1.0L;

			//get its current spin;
			//
			spinBefore = lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];

			// if this spin will be same as parent spin after flipping, try to add it to cluster
			if (std::get<3>(current) != spinBefore){
				rand = lat.rand.rnd();
				if ( rand < lat.PROB) {
					//get energy before reflecting
					//
					enBefore = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));

					//get new spin
					spinAfter = -spinBefore;

					//reflect and mark as added to cluster
					lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = spinAfter;
					lat.clust.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = true;

					//update energy and magnetization
					enAfter = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));
					updateVals(lat,
							enBefore-enAfter,
							spinBefore-spinAfter);
					//find indices of neighbours
					neig1 = std::make_tuple(
							(std::get<0>(current) + 1) % lat.int_L, 
							std::get<1>(current),
							std::get<2>(current),
							spinAfter);
					neig2 = std::make_tuple(
							(std::get<0>(current) + lat.int_L - 1) % lat.int_L,
							std::get<1>(current),
							std::get<2>(current),
							spinAfter);
					neig3 = std::make_tuple(
							std::get<0>(current),
							(std::get<1>(current) + 1) % lat.int_L,
							std::get<2>(current),
							spinAfter);
					neig4 = std::make_tuple(
							std::get<0>(current),
							(std::get<1>(current) + lat.int_L - 1) % lat.int_L,
							std::get<2>(current),
							spinAfter);
					neig5 = std::make_tuple(
							std::get<0>(current),
							std::get<1>(current),
							(std::get<2>(current) + 1) % lat.int_L,
							spinAfter);
					neig6 = std::make_tuple(
							std::get<0>(current),
							std::get<1>(current),
							(std::get<2>(current) + lat.int_L - 1)%lat.int_L,
							spinAfter);
					//if a neighbour is not already part of the cluster, add it to perimeter list
					if (!lat.clust.theCluster[std::get<0>(neig1)][std::get<1>(neig1)][std::get<2>(neig1)] ){
						perimeter.push_back(neig1);
						n = n + 1;
					}
					if (!lat.clust.theCluster[std::get<0>(neig2)][std::get<1>(neig2)][std::get<2>(neig2)] ){
						perimeter.push_back(neig2);
						n = n + 1;
					}
					if (!lat.clust.theCluster[std::get<0>(neig3)][std::get<1>(neig3)][std::get<2>(neig3)] ){
						perimeter.push_back(neig3);
						n = n + 1;
					}
					if (!lat.clust.theCluster[std::get<0>(neig4)][std::get<1>(neig4)][std::get<2>(neig4)] ){
						perimeter.push_back(neig4);
						n = n + 1;
					}
					if (!lat.clust.theCluster[std::get<0>(neig5)][std::get<1>(neig5)][std::get<2>(neig5)] ){
						perimeter.push_back(neig5);
						n = n + 1;
					}
					if (!lat.clust.theCluster[std::get<0>(neig6)][std::get<1>(neig6)][std::get<2>(neig6)] ){
						perimeter.push_back(neig6);
						n = n + 1;
					}
				}
			}
		}
	}
	//empty the cluster
	lat.clust.emptyCluster();
	//return # of tested spins
	lat.NTotClusts += 1;
	lat.NTotSweeps += time/lat.Nspins;
	return time;
}
