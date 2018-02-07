#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>

#include "latticeOps.h"

long double getProb(long double u, long double angleParent, long double angle,long double beta){
	long double prob = 1.0L - exp(2.0L*beta*cos(angleParent - u)*cos(angle -u));
	if (prob < 0.0L){ return 0.0L;}
	return std::min((long double)1.0L,prob);
}

int growCluster(long double ***lattice,bool ***cluster, long double &L,long double &beta, long double& TotXMag,long double& TotYMag,long double& TotEn,long double &TotSinX,long double &TotSinY,long double &TotSinZ,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng){

	int time = 1;
	//select random plane and random staring spin
	long double u = 2.0L*((long double)M_PI)*dist(eng);
	int s1 = L*dist(eng);
	int s2 = L*dist(eng);
	int s3 = L*dist(eng);
	// save angle and energy before flipping
	long double angleBefore = lattice[s1][s2][s3];
	long double enBefore = siteEnergy(lattice,L,s1,s2,s3);
	long double angleAfter = (long double)M_PI + 2.0L*u - angleBefore;
	//reflect spin and mark as part of cluster
	lattice[s1][s2][s3] = angleAfter;
	cluster[s1][s2][s3] = true;
	//update energy, mag etc..
	TotEn += siteEnergy(lattice,L,s1,s2,s3) - enBefore;
	TotXMag += cos(angleAfter) - cos(angleBefore);
	TotYMag += sin(angleAfter) - sin(angleBefore);
	TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
	TotSinY += sinY(lattice,L,s1,s2,s3,angleAfter) - sinY(lattice,L,s1,s2,s3,angleBefore);
	TotSinZ += sinZ(lattice,L,s1,s2,s3,angleAfter) - sinZ(lattice,L,s1,s2,s3,angleBefore);
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
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
		if (!cluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)]){

			//increase time for every tested spin
			//
			++time;

			//get its current angle;
			//
			angleBefore = lattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];

			//calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
			prob = getProb(u,std::get<3>(current) ,angleBefore,beta);
			rand = dist(eng);
			if ( rand < prob) {
				flip = true;
			} //if rand is so close to prob that floating point precision considers them equal, flip in 50 % of those cases
			//
			else if ( std::abs(rand-prob) < std::abs(std::min(rand,prob)*std::numeric_limits<long double>::epsilon())){
				rand = dist(eng);
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
				enBefore = siteEnergy(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current));

				//get new angle
				angleAfter = (long double)M_PI + 2.0L*u - angleBefore;

				//reflect and mark as added to cluster
				lattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = angleAfter;
				cluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = true;

				//update energy and magnetization
				TotEn += siteEnergy(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current)) - enBefore;
				TotXMag += cos(angleAfter) - cos(angleBefore);
				TotYMag += sin(angleAfter) - sin(angleBefore);
				TotSinX += sinX(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter) - sinX(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
				TotSinY += sinY(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter) - sinY(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
				TotSinZ += sinZ(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter) - sinZ(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);

				//find indices of neighbours
				neig1 = std::make_tuple(
						(std::get<0>(current) + 1) % (int)L, 
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				neig2 = std::make_tuple(
						(std::get<0>(current) + (int)L - 1) % (int)L,
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				neig3 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + 1) % (int)L,
						std::get<2>(current),
						angleAfter);
				neig4 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + (int)L - 1) % (int)L,
						std::get<2>(current),
						angleAfter);
				neig5 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + 1) % (int)L,
						angleAfter);
				neig6 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + (int)L - 1)%(int)L,
						angleAfter);
				//if a neighbour is not already part of the cluster, add it to perimeter list
				if (!cluster[std::get<0>(neig1)][std::get<1>(neig1)][std::get<2>(neig1)] ){
					perimeter.push_back(neig1);
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig2)][std::get<1>(neig2)][std::get<2>(neig2)] ){
					perimeter.push_back(neig2);
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig3)][std::get<1>(neig3)][std::get<2>(neig3)] ){
					perimeter.push_back(neig3);
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig4)][std::get<1>(neig4)][std::get<2>(neig4)] ){
					perimeter.push_back(neig4);
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig5)][std::get<1>(neig5)][std::get<2>(neig5)] ){
					perimeter.push_back(neig5);
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig6)][std::get<1>(neig6)][std::get<2>(neig6)] ){
					perimeter.push_back(neig6);
					n = n + 1;
				}
			}
		}
	}
	//empty the cluster
	emptyCluster(cluster,L);
	//return # of tested spins
	return time;
}
