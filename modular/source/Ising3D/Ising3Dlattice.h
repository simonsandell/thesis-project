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
	long int Neqclusts,NTotClusts,int_L;
	bool coldstart,warmedUp;
	std::string warmLatPath;
	std::string maxEPath;
	long double maxE;



	long double beta;

	long double energy,mag;

	long double calcEn();
	long double calcMag();

	long double *** newLatticeI3D(long double L,bool cold);
	LatticeIsing3D(long double L, bool cold,long double Beta,RandStruct r, Cluster c,std::string pathMaxE,std::string pathWarmLat);
	LatticeIsing3D();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	void testConsistent();

	long double PROB; 

	outPutter oPer;
	void saveLattice();
	void saveLatticeAs(std::string name);
	void loadLattice();
	void printVals();
	};
#endif
