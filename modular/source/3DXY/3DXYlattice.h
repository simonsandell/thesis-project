#ifndef 3DXYLATTICE_H 
#define 3DXYLATTICE_H

struct Lattice{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	
	bool coldstart,warmedUp;

	long double energy,xmag,ymag,sinx,siny,sinz;

	Lattice(int L, bool cold);
	Lattice();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	long double sinX( int &s1, int &s2, int &s3,long double &angle);
	long double sinY( int &s1, int &s2, int &s3,long double &angle);
	long double sinZ( int &s1, int &s2, int &s3,long double &angle);

	void testConsistent();

	};
#endif
