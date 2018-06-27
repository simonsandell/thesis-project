#include "clusterStruct.h"
#include <tuple>
#include <iostream>
long unsigned int xyzToK_C( int x, int y , int z,long double L){
	long unsigned int ret = 0;
	ret += (long unsigned int) x;
	ret += (long unsigned int) (y*L);
	ret += (long unsigned int) (z*L*L);
	return ret;
}
Cluster::Cluster(int l){
	L = l;	
	Nspins = (long unsigned int)(L*L*L + 0.1L);
	theCluster = new bool[Nspins];
	for (unsigned int i = 0; i< Nspins;++i){
		theCluster[i] = false;
	}
};
Cluster::Cluster(){
};

void Cluster::emptyCluster(){
	for (unsigned int i = 0; i< Nspins; ++i){
		theCluster[i] = false;
	}
};
void Cluster::addToCl(int s1,int s2,int s3){
	long unsigned int k = xyzToK_C(s1,s2,s3,L);
	theCluster[k] = true;
}

bool Cluster::checkSpin(std::tuple<int,int,int,long double> spin){
	int s1 = std::get<0>(spin);
	int s2 = std::get<1>(spin);
	int s3 = std::get<2>(spin);
	long unsigned int k = xyzToK_C(s1,s2,s3,L);
	return theCluster[k];
}

void Cluster::print_cluster(){
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
                            std::cout << i << j << k << std::endl;
                            std::cout << theCluster[xyzToK_C(i,j,k,L)] << std::endl;
			}
		}
	}
}

