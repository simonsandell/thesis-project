#include "latticeOps.h"
#include <cmath>


//clear the cluster
void emptyCluster(bool***cluster,double &L){
	int steps = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				cluster[i][j][k] = 0;
			}
		}
	}
}
//calculate energy of site
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3){
	double sum = 0;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= cos(lattice[s1][s2][s3]-lattice[n1m][s2][s3]);
	sum -= cos(lattice[s1][s2][s3]-lattice[n1p][s2][s3]);
	sum -= cos(lattice[s1][s2][s3]-lattice[s1][n2m][s3]);
	sum -= cos(lattice[s1][s2][s3]-lattice[s1][n2p][s3]);
	sum -= cos(lattice[s1][s2][s3]-lattice[s1][s2][n3m]);
	sum -= cos(lattice[s1][s2][s3]-lattice[s1][s2][n3p]);
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
double sinX(double ***lattice,double &L, int &s1, int &s2, int &s3,double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	double ret = 0;
	ret = sin(lattice[nm][s2][s3] - angle) + sin(angle - lattice[np][s2][s3]);
	return ret;
}
