#include <cmath>
#include <random>
#include <utility>
#include <tuple>

#include "latticeOps.h"

int growCluster(double ***lattice,bool ***cluster, double &L,double &beta, double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX,std::uniform_real_distribution<double> &dist,std::mt19937_64 &eng){

	int time = 1;
	//select random plane and random staring spin
	double u = 2.0*M_PI*dist(eng);
	int s1 = L*dist(eng);
	int s2 = L*dist(eng);
	int s3 = L*dist(eng);
	// save angle and energy before flipping
	double angleBefore = lattice[s1][s2][s3];
	double enBefore = siteEnergy(lattice,L,s1,s2,s3);
	double angleAfter = M_PI + 2.0*u - angleBefore;
	//reflect spin and mark as part of cluster
	lattice[s1][s2][s3] = angleAfter;
	cluster[s1][s2][s3] = true;
	//update energy, mag etc..
	TotEn += siteEnergy(lattice,L,s1,s2,s3) - enBefore;
	TotXMag += cos(angleAfter) - cos(angleBefore);
	TotYMag += sin(angleAfter) - sin(angleBefore);
	TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//make a list for perimeter spins
	std::tuple<int,int,int,double> perimeter[(int)(L*L*L*6)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	//add neighbours to list
	perimeter[n] = std::make_tuple(n1m,s2,s3,angleAfter); n +=1;
	perimeter[n] = std::make_tuple(n1p,s2,s3,angleAfter); n +=1;
	perimeter[n] = std::make_tuple(s1,n2m,s3,angleAfter); n +=1;
	perimeter[n] = std::make_tuple(s1,n2p,s3,angleAfter); n +=1;
	perimeter[n] = std::make_tuple(s1,s2,n3m,angleAfter); n +=1;
	perimeter[n] = std::make_tuple(s1,s2,n3p,angleAfter); n +=1;

	std::tuple<int,int,int,double> current;
	double prob = 0.0;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;
		//test that it is not already part of cluster
		if (!cluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)]){

			//increase time for every tested spin
			++time;
			//get its current angle;
			angleBefore = lattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];
			//calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
			prob = 1.0 -exp(2.0*beta*cos(std::get<3>(current) - u)*cos(angleBefore -u));
			//add this perimeter spin to the cluster with probability prob
			if (dist(eng) < prob){
				//save angle and energy before reflecting
				angleBefore = lattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];
				enBefore = siteEnergy(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current));
				//get new angle
				angleAfter = M_PI + 2.0*u - angleBefore;
				//reflect and mark as added to cluster
				lattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = angleAfter;
				cluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = true;
				//update energy and magnetization
				TotEn += siteEnergy(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current)) - enBefore;
				TotXMag += cos(angleAfter) - cos(angleBefore);
				TotYMag += sin(angleAfter) - sin(angleBefore);
				TotSinX += sinX(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter) - sinX(lattice,L,std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);

				//find indices of neighbours
				std::tuple<int,int,int,double> neig1 = std::make_tuple(
						(std::get<0>(current) + 1) % (int)L, 
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				std::tuple<int,int,int,double> neig2 = std::make_tuple(
						(std::get<0>(current) + (int)L - 1) % (int)L,
						std::get<1>(current),
						std::get<2>(current),
						angleAfter);
				std::tuple<int,int,int,double> neig3 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + 1) % (int)L,
						std::get<2>(current),
						angleAfter);
				std::tuple<int,int,int,double> neig4 = std::make_tuple(
						std::get<0>(current),
						(std::get<1>(current) + (int)L - 1) % (int)L,
						std::get<2>(current),
						angleAfter);
				std::tuple<int,int,int,double> neig5 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + 1) % (int)L,
						angleAfter);
				std::tuple<int,int,int,double> neig6 = std::make_tuple(
						std::get<0>(current),
						std::get<1>(current),
						(std::get<2>(current) + (int)L - 1)%(int)L,
						angleAfter);
				//if a neighbour is not already part of the cluster, add it to perimeter list
				if (!cluster[std::get<0>(neig1)][std::get<1>(neig1)][std::get<2>(neig1)] ){
					perimeter[n] = neig1;
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig2)][std::get<1>(neig2)][std::get<2>(neig2)] ){
					perimeter[n] = neig2;
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig3)][std::get<1>(neig3)][std::get<2>(neig3)] ){
					perimeter[n] = neig3;
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig4)][std::get<1>(neig4)][std::get<2>(neig4)] ){
					perimeter[n] = neig4;
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig5)][std::get<1>(neig5)][std::get<2>(neig5)] ){
					perimeter[n] = neig5;
					n = n + 1;
				}
				if (!cluster[std::get<0>(neig6)][std::get<1>(neig6)][std::get<2>(neig6)] ){
					perimeter[n] = neig6;
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
