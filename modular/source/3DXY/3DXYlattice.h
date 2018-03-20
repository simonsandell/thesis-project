#ifndef _3DXYLATTICE_H 
#define _3DXYLATTICE_H

struct Lattice3DXY{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,NTotSweeps;
	int Neqclusts,NTotClusts;	
	bool coldstart,warmedUp;

	long double energy,xmag,ymag,sinx,siny,sinz;

	Lattice3DXY(int L, bool cold);
	Lattice3DXY();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	long double sinX( int &s1, int &s2, int &s3,long double &angle);
	long double sinY( int &s1, int &s2, int &s3,long double &angle);
	long double sinZ( int &s1, int &s2, int &s3,long double &angle);

	void testConsistent();

	};
#endif
