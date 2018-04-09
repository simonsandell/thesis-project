
#include "3DXY/3DXYio.h"
#include "3DXY/3DXYlattice.h"
#include "3DXY/3DXYrunMetro.h"
#include "3DXY/3DXYmetro.h"
#include "3DXY/3DXYrunWolff.h"
#include "3DXY/3DXYwolff.h"
#include "3DXY.h"
#include "clusterStruct.h"
#include "randStruct.h"




void _3DXY::warmup(Lattice3DXY& lat,long double N){
	long double steps;
	long double NClusts = 0;
	long double NSweeps = 0;
	while (NSweeps < N){
		steps =(long double) cluster3DXY(lat);
		NClusts += 1.0L;
		NSweeps += (steps/lat.Nspins);
	}
	if( !lat.warmedUp){
		lat.Neqclusts = NClusts;
		lat.Neqsweeps = NSweeps;
		lat.warmedUp = true;
	}
}

//generate range of temperatures
long double * getTrange(long double start, long double end, int N){
	long double dt = (end-start)/((long double)N-1.0L);
	long double *T = new long double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (long double)i*dt;
	}
	return T;
}

void _3DXY::wolffHistJob(long double L){

	long double runTemp = 2.20200000000000L;

	long double	startT=			2.20150L;
	long double	endT=			2.20300L;
	int 		Ntemps=			31;
	long double* Trange;
	if (Ntemps < 2) {
		Trange = new long double[1];
		Trange[0] = runTemp;
	}
	else {
		Trange = getTrange(startT,endT,int(Ntemps));
	}
	long double 	Neq=			10.0L;
	bool 		cold=			true;
	long double	Nsamp=			10.0L;
	long double 	Nbetw=			10.0L;
	int 		Nruns=			100;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,cold,r,c,"/cfs/klemming/scratch/s/simsan/maxE/3DXY/");
	warmup(lat,Neq);
	for (int i=0; i< Nruns; ++i){	
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
		warmup(lat,Nbetw);
	}
	if (lat.oPer.outputLines.size() > 0){
		lat.oPer.printData(1);
	}

}
void _3DXY::teqRun(long double L,bool cold){
	long double runTemp = 2.20200000000000L;
	int 		Ntemps=			1;
	long double* Trange;
	Trange = new long double[1];
	Trange[0] = runTemp;
	long double	Nsamp=			2.0L;
	int 		Ndoubles=		18;
	Cluster c(L);
	RandStruct r;
	Lattice3DXY lat(L,runTemp,cold,r,c,"/cfs/klemming/scratch/s/simsan/maxE/3DXY/");
	wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
	for (int i=0; i< Ndoubles; ++i){	
		wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps,runTemp);
		Nsamp = Nsamp*2;
	}


}
