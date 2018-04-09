#ifndef LATTICESTRUCT_H
#define LATTICESTRUCT_H
#include "../ioHandle.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

#include <string>


struct LatticeIsing3D{
	RandStruct rand;
	Cluster clust;
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,NTotSweeps;
	long int Neqclusts,NTotClusts;	
	bool coldstart,warmedUp;
	std::string maxEPath;
	long double maxE;



	long double beta;

	long double energy,mag;

	long double calcEn();
	long double calcMag();

	long double *** newLatticeI3D(long double L,bool cold);
	LatticeIsing3D(int L, bool cold,long double Beta,RandStruct r, Cluster c,std::string pathMaxE);
	LatticeIsing3D();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	void testConsistent();

	long double PROB; 

	outPutter oPer;

	};
#endif
