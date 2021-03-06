#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>
#include <iostream>

#include "3DXYio.h"
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

int cluster3DXY(Lattice3DXY& lat,Cluster& cluster,long double beta,RandStruct& randgen){

	printLattice3DXY(lat.theLattice,lat.L);
	int time = 1;
	//select random plane and random staring spin
	long double u = -(long double)M_PI + 2.0L*((long double)M_PI)*randgen.rnd();
	int s1 = lat.L*randgen.rnd();
	int s2 = lat.L*randgen.rnd();
	int s3 = lat.L*randgen.rnd();
	// save angle and energy before flipping
	long double angleBefore = lat.theLattice[s1][s2][s3];
	long double enBefore = lat.siteEnergy(s1,s2,s3);
	long double angleAfter = (long double)M_PI + 2.0L*u - angleBefore;
	//reflect spin and mark as part of cluster
	lat.theLattice[s1][s2][s3] = angleAfter;
	cluster.theCluster[s1][s2][s3] = true;
	printLattice3DXY(lat.theLattice,lat.L);
	//update energy, mag etc..
	long double enAfter = lat.siteEnergy(s1,s2,s3);
	long double sxBef = lat.sinX(s1,s2,s3,angleBefore);
	long double sxAft = lat.sinX(s1,s2,s3,angleAfter);
	long double syBef = lat.sinY(s1,s2,s3,angleBefore);
	long double syAft = lat.sinY(s1,s2,s3,angleAfter);
	long double szBef = lat.sinZ(s1,s2,s3,angleBefore);
	long double szAft = lat.sinZ(s1,s2,s3,angleAfter);
	updateVals(lat,
			enBefore,enAfter,
			angleBefore,angleAfter,
			sxBef,sxAft,
			syBef,syAft,
			szBef,szAft);
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)lat.L )%(int)lat.L;
	int n1p = (s1 +1 + (int)lat.L )%(int)lat.L;
	int n2m = (s2 -1 + (int)lat.L )%(int)lat.L;
	int n2p = (s2 +1 + (int)lat.L )%(int)lat.L;
	int n3m = (s3 -1 + (int)lat.L )%(int)lat.L;
	int n3p = (s3 +1 + (int)lat.L )%(int)lat.L;
	std::tuple<int,int,int,long double> neig1 = std::make_tuple(n1m,s2,s3,angleAfter);
	std::tuple<int,int,int,long double> neig2 = std::make_tuple(n1p,s2,s3,angleAfter);
	std::tuple<int,int,int,long double> neig3 = std::make_tuple(s1,n2m,s3,angleAfter);
	std::tuple<int,int,int,long double> neig4 = std::make_tuple(s1,n2p,s3,angleAfter);
	std::tuple<int,int,int,long double> neig5 = std::make_tuple(s1,s2,n3m,angleAfter);
	std::tuple<int,int,int,long double> neig6 = std::make_tuple(s1,s2,n3p,angleAfter);

	//make a list for perimeter spins
	std::vector<std::tuple<int,int,int,long double>> perimeter;
	//add neighbours to list
	perimeter.push_back(neig1);
	perimeter.push_back(neig2);
	perimeter.push_back(neig3);
	perimeter.push_back(neig4);
	perimeter.push_back(neig5);
	perimeter.push_back(neig6);
	int n = 6;

	std::tuple<int,int,int,long double> current;
	long double prob = 0.0L;
	long double rand = 0.0L;
	bool flip = false;
	while (n > 0){
		//pick out the last element 
		current = perimeter.back();
		perimeter.pop_back();
		n -= 1;
		//test that it is not already part of cluster
		if (!cluster.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)]){

			//increase time for every tested spin
			//
			++time;

			//get its current angle;
			//
			angleBefore = lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];

			//calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
			prob = getProb(u,std::get<3>(current) ,angleBefore,beta);
			rand = randgen.rnd();
			if ( rand < prob) {
				flip = true;
			} //if rand is so close to prob that floating point precision considers them equal, flip in 50 % of those cases
			//
			else if ( std::abs(rand-prob) < std::abs(std::min(rand,prob)*std::numeric_limits<long double>::epsilon())){
				rand = randgen.rnd();
				if (rand < 0.50L){
					flip = true;
				}
				else{ flip = false;
				}
			} 
			else 
			{
				flip = false;
			}
			if (flip) {
				//get energy before reflecting
				//
				enBefore = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));

				//get new angle
				angleAfter = (long double)M_PI + 2.0L*u - angleBefore;

				//reflect and mark as added to cluster
				lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = angleAfter;
				cluster.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = true;

				//update energy and magnetization
				enAfter = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));
				sxBef = lat.sinX(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
				sxAft = lat.sinX(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
				syBef = lat.sinY(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
				syAft = lat.sinY(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
				szBef = lat.sinZ(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
				szAft = lat.sinZ(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
				updateVals(lat,
						enBefore,enAfter,
						angleBefore,angleAfter,
						sxBef,sxAft,
						syBef,syAft,
						szBef,szAft);
				//find indices of neighbours
				neig1 = std::make_tuple(
						(std::get<0>(current) + 1) % (int)lat.L, 
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				neig2 = std::make_tuple(
						(std::get<0>(current) + (int)lat.L - 1) % (int)lat.L,
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				neig3 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + 1) % (int)lat.L,
						std::get<2>(current),
						angleAfter);
				neig4 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + (int)lat.L - 1) % (int)lat.L,
						std::get<2>(current),
						angleAfter);
				neig5 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + 1) % (int)lat.L,
						angleAfter);
				neig6 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + (int)lat.L - 1)%(int)lat.L,
						angleAfter);
				//if a neighbour is not already part of the cluster, add it to perimeter list
				if (!cluster.theCluster[std::get<0>(neig1)][std::get<1>(neig1)][std::get<2>(neig1)] ){
					perimeter.push_back(neig1);
					n = n + 1;
				}
				if (!cluster.theCluster[std::get<0>(neig2)][std::get<1>(neig2)][std::get<2>(neig2)] ){
					perimeter.push_back(neig2);
					n = n + 1;
				}
				if (!cluster.theCluster[std::get<0>(neig3)][std::get<1>(neig3)][std::get<2>(neig3)] ){
					perimeter.push_back(neig3);
					n = n + 1;
				}
				if (!cluster.theCluster[std::get<0>(neig4)][std::get<1>(neig4)][std::get<2>(neig4)] ){
					perimeter.push_back(neig4);
					n = n + 1;
				}
				if (!cluster.theCluster[std::get<0>(neig5)][std::get<1>(neig5)][std::get<2>(neig5)] ){
					perimeter.push_back(neig5);
					n = n + 1;
				}
				if (!cluster.theCluster[std::get<0>(neig6)][std::get<1>(neig6)][std::get<2>(neig6)] ){
					perimeter.push_back(neig6);
					n = n + 1;
				}
			printLattice3DXY(lat.theLattice,lat.L);
			}
		}
	}
	//empty the cluster
	cluster.emptyCluster();	
	//return # of tested spins
	lat.NTotSweeps += ((long double)time/lat.Nspins);
	lat.NTotClusts += 1;
	return time;
}
