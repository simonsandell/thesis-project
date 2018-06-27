#ifndef CLUSTERSTRUCT_H
#define CLUSTERSTRUCT_H


struct Cluster{
	bool *** theCluster;
	int L;
	
	Cluster(int L);
	Cluster();

	void emptyCluster();
        void print_cluster();




};

#endif
