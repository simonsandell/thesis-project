#include "clusterStruct.h"
Cluster::Cluster(int l){
	L = l;	
	theCluster = new bool**[L];
	for (int i = 0; i< L;++i){
		theCluster[i] = new bool*[L];
		for (int j =0;j<L;++j){
			theCluster[i][j] = new bool[L];
		}
	}
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				theCluster[i][j][k] = false;
			}
		}
	}
};

void Cluster::emptyCluster(){
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				theCluster[i][j][k] = false;
			}
		}
	}
};
