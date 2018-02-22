#include <cmath>
#include <string>
#include <unistd.h>
#include <sys/syscall.h>
#include <random>

#include "calcQuants.h"
#include "wolff.h"
#include "ioFuncs.h"

//clear the cluster
//calculate energy of site
long double siteEnergy(long double *** lattice,long double &L, int &s1, int &s2, int &s3){
	long double sum = 0.0L;
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
long double sinX(long double ***lattice,long double &L, int &s1, int &s2, int &s3,long double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lattice[nm][s2][s3] - angle) + sin(angle - lattice[np][s2][s3]);
	return ret;
}
long double sinY(long double ***lattice,long double &L, int &s1, int &s2, int &s3,long double &angle){
	int np = (s2 + 1) %(int)L;
	int nm = (s2 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lattice[s1][nm][s3] - angle) + sin(angle - lattice[s1][np][s3]);
	return ret;
}
long double sinZ(long double ***lattice,long double &L, int &s1, int &s2, int &s3,long double &angle){
	int np = (s3 + 1) %(int)L;
	int nm = (s3 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lattice[s1][s2][nm] - angle) + sin(angle - lattice[s1][s2][np]);
	return ret;
}

