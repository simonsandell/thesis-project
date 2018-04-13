#ifndef _3DXYLATTICE_H 
#define _3DXYLATTICE_H

#include <string>

#include "../ioHandle.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

struct Lattice3DXY{
	RandStruct rand;
	Cluster clust;
	long double *** theLattice;
	long double runTemp,beta;
	long double L,Nspins,Neqsweeps,NTotSweeps;
	long int Neqclusts,NTotClusts,int_L;
	bool coldstart,warmedUp;
	std::string warmLatPath;
	std::string maxEPath;
	long double maxE;

	long double energy,xmag,ymag,sinx,siny,sinz;

	long double*** newLattice(long double L,bool cold);
	Lattice3DXY(int L,long double rT, bool cold,RandStruct r, Cluster c,std::string pathMaxE,std::string warmLatPath);
	Lattice3DXY();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	long double sinX( int &s1, int &s2, int &s3,long double &angle);
	long double sinY( int &s1, int &s2, int &s3,long double &angle);
	long double sinZ( int &s1, int &s2, int &s3,long double &angle);

	void testConsistent();

	
	outPutter oPer;
	void saveLattice();
	void saveLatticeAs(std::string name);
	void loadLattice();

	};
#endif
