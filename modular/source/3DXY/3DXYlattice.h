#ifndef _3DXYLATTICE_H 
#define _3DXYLATTICE_H

#include <string>

#include "../ioHandle.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

struct Lattice3DXY{
	RandStruct rand;
	Cluster clust;
	long double* theLattice;
	unsigned long int ** Neighbours;
	long double runTemp,beta;
	long double L,Nspins,Neqsweeps,NTotSweeps;
	long int Neqclusts,NTotClusts,int_L;
	bool coldstart,warmedUp;
	std::string warmLatPath;
	std::string maxEPath;
	long double maxE;

	long double energy,xmag,ymag,sinx,siny,sinz;

	long double* newLattice(long double L,bool cold);
	unsigned long int ** generateNeighbours(int l);
	Lattice3DXY(int L,long double rT, bool cold,RandStruct r, Cluster c,std::string pathMaxE,std::string warmLatPath);
	Lattice3DXY();

	void updateQuants();

	long double siteEnergy(unsigned long int s1);
	long double sinX(unsigned long int &s1, long double &angle);
	long double sinY(unsigned long int &s1, long double &angle);
	long double sinZ(unsigned long int &s1, long double &angle);

	long double getAngle(int s1,int s2,int s3);
	void setAngle(int s1,int s2,int s3,long double newAng);

	void testConsistent();


	outPutter oPer;
	void saveLattice();
	void saveLatticeAs(std::string name);
	void loadLattice();
	void printVals();

};
#endif
