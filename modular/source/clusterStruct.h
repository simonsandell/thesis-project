#ifndef CLUSTERSTRUCT_H
#define CLUSTERSTRUCT_H

#include <tuple>

struct Cluster{
	bool* theCluster;
	int L;
	long unsigned int Nspins;
	
	Cluster(int L);
	Cluster();

	void emptyCluster();
	void addToCl(int s1,int s2,int s3);
	bool checkSpin(std::tuple<int,int,int,long double> spin);

};

#endif
