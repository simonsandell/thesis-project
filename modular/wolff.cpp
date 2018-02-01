#include "wolff.h"
#include "latticeOps.h"
#include <tuple>
#include <cmath>
using namespace std;

int growCluster(double ***lattice,bool ***cluster, double &L,double &beta, auto &randgen,double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX){

	double u = 2*M_PI*randgen();
	int s1 = L*randgen();
	int s2 = L*randgen();
	int s3 = L*randgen();
	int time = 1;
	//reflect spin and mark as part of cluster
	// 
	double angleBefore = lattice[s1][s2][s3];
	double enBefore = siteEnergy(lattice,L,s1,s2,s3);
	double angleAfter = M_PI + 2*u - angleBefore;
	lattice[s1][s2][s3] = angleAfter;
	cluster[s1][s2][s3] = 1;
	TotEn += siteEnergy(lattice,L,s1,s2,s3) - enBefore;
	TotXMag += cos(angleAfter) - cos(angleBefore);
	TotYMag += sin(angleAfter) - sin(angleBefore);
	TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
	//
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//add them to perimeter list
	tuple<int,int,int,double> perimeter[(int)(L*L*L*6)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	perimeter[n] = make_tuple(n1m,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(n1p,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2m,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2p,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3m,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3p,angleAfter); n +=1;

	tuple<int,int,int,double> current;
	double prob = 0;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;

		//test that it is not already part of cluster
		if (cluster[get<0>(current)][get<1>(current)][get<2>(current)] == 0){

			//increase time for every tested spin
			++time;
			//get its current angle;
			angleBefore = lattice[get<0>(current)][get<1>(current)][get<2>(current)];
			//calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
			prob = 1 -exp(2*beta*cos(get<3>(current) - u)*cos(angleBefore -u));
			//add this perimeter spin to the cluster with probability prob
			if (randgen() < prob){
				//save angle and energy before reflecting
				angleBefore = lattice[get<0>(current)][get<1>(current)][get<2>(current)];
				enBefore = siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current));
				//get new angle
				angleAfter = M_PI + 2*u - angleBefore;
				//reflect and mark as added to cluster
				lattice[get<0>(current)][get<1>(current)][get<2>(current)] = angleAfter;
				cluster[get<0>(current)][get<1>(current)][get<2>(current)] = 1;
				//update energy and magnetization
				TotEn += siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current)) - enBefore;
				TotXMag += cos(angleAfter) - cos(angleBefore);
				TotYMag += sin(angleAfter) - sin(angleBefore);
				TotSinX += sinX(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleAfter) - sinX(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleBefore);

				//find indices of its neighbours
				tuple<int,int,int,double> neig1 = make_tuple(
						(get<0>(current) + 1) % (int)L, 
						get<1>(current),
						get<2>(current),
						angleAfter);
				tuple<int,int,int,double> neig2 = make_tuple(
						(get<0>(current) + (int)L - 1) % (int)L,
						get<1>(current),
						get<2>(current),
						angleAfter);
				tuple<int,int,int,double> neig3 = make_tuple(
						get<0>(current),
						(get<1>(current) + 1) % (int)L,
						get<2>(current),
						angleAfter);
				tuple<int,int,int,double> neig4 = make_tuple(
						get<0>(current),
						(get<1>(current) + (int)L - 1) % (int)L,
						get<2>(current),
						angleAfter);
				tuple<int,int,int,double> neig5 = make_tuple(
						get<0>(current),
						get<1>(current),
						(get<2>(current) + 1) % (int)L,
						angleAfter);
				tuple<int,int,int,double> neig6 = make_tuple(
						get<0>(current),
						get<1>(current),
						(get<2>(current) + (int)L - 1)%(int)L,
						angleAfter);
				//if it is not already part of the cluster, add it to perimeter list
				if (cluster[get<0>(neig1)][get<1>(neig1)][get<2>(neig1)] ==0){
					perimeter[n] = neig1;
					n = n + 1;
				}
				if (cluster[get<0>(neig2)][get<1>(neig2)][get<2>(neig2)] ==0){
					perimeter[n] = neig2;
					n = n + 1;
				}
				if (cluster[get<0>(neig3)][get<1>(neig3)][get<2>(neig3)] ==0){
					perimeter[n] = neig3;
					n = n + 1;
				}
				if (cluster[get<0>(neig4)][get<1>(neig4)][get<2>(neig4)] ==0){
					perimeter[n] = neig4;
					n = n + 1;
				}
				if (cluster[get<0>(neig5)][get<1>(neig5)][get<2>(neig5)] ==0){
					perimeter[n] = neig5;
					n = n + 1;
				}
				if (cluster[get<0>(neig6)][get<1>(neig6)][get<2>(neig6)] ==0){
					perimeter[n] = neig6;
					n = n + 1;
				}
			}
		}
	}
emptyCluster(cluster,L);
return time;
}


