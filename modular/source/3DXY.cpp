#include <mpi.h>
#include <string>
#include <sstream>
#include <iostream>
#include <time.h>

#include "3DXY/3DXYio.h"
#include "3DXY/3DXYlattice.h"
#include "3DXY/3DXYrunMetro.h"
#include "3DXY/3DXYrunWolff.h"
#include "3DXY/3DXYwolff.h"
#include "3DXY/3DXYcorrelation.h"
#include "3DXY.h"
#include "clusterStruct.h"
#include "randStruct.h"

void _3DXY::printSettings(long double rT,long double sT,long double eT,int nT,long double nEQ,bool cold,long double nSamp,long double nBetw,long double L){
    std::stringstream sstrm;
    sstrm << "# SETTINGS \n# runtemp: ";
    sstrm << rT<< "\n# startT: ";
    sstrm << sT<< "\n# endT: ";
    sstrm << eT<< "\n# NumT: ";
    sstrm << nT<< "\n# initial EQ sweeps: ";
    sstrm << nEQ<< "\n# cold start: ";
    sstrm << cold << "\n# sample sweeps: ";
    sstrm << nSamp << "\n# between sweeps: ";
    sstrm << nBetw<< "\n# system size: ";
    sstrm << L << "\n";
    std::string settings = sstrm.str();
    int tag = 0;
    MPI_Send(settings.c_str(),settings.size(),MPI_CHAR,0,tag,MPI_COMM_WORLD);



}

void _3DXY::warmup(Lattice3DXY& lat,long double N){
    long double steps;
    long double NClusts = 0;
    long double NSweeps = 0;
    while (NSweeps < N){
        steps = cluster3DXY(lat);
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

void _3DXY::wolffHistJob(long double L,std::string maxepath,std::string warmlatpath,bool doPrint){
    long double runTemp = 2.20184000000000L;

    long double	startT=			2.20160L;
    long double	endT=			2.20200L;
    int 		Ntemps=			101;
    long double* Trange;
    if (Ntemps < 2) {
        Trange = new long double[1];
        Trange[0] = runTemp;
    }
    else {
        Trange = getTrange(startT,endT,Ntemps);
    }
    long double 	Neq=			1000.0L;
    bool 		cold=			true;
    long double	Nsamp=			1000.0L;
    long double 	Nbetw=			100.0L;
    if (doPrint){
        printSettings( runTemp, startT, endT,Ntemps, Neq ,cold, Nsamp, Nbetw, L);
    }
    Cluster c(L);
    RandStruct r;
    Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
    lat.testConsistent();
    lat.loadLattice();
    warmup(lat,100.0L);
    for (int i = 0; i<5;++i){
        wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
        warmup(lat,Nbetw);
    }
    lat.testConsistent();
}
void _3DXY::warmupJob(long double L, std::string maxepath,std::string warmlatpath){
    long double runTemp = 2.201840000000000L;
    bool cold = true;
    Cluster c(L);
    RandStruct r;
    Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
    //lat.loadLattice();
    long double Neq = 1000.0L;
    while (lat.NTotSweeps < 100000.0L){
        warmup(lat,Neq);
        lat.saveLatticeAs("t_220184");
    }
}

void _3DXY::teqJob(long double L,bool cold,std::string maxepath,std::string warmlatpath){
    long double runTemp = 2.201840000000000L;
    Cluster c(L);
    RandStruct r;
    Lattice3DXY lat(L,runTemp,cold,r,c,maxepath,warmlatpath);
    lat.maxE *= 2.0L;

    int Ntemps = 1;
    long double Trange[1] = {runTemp};
    long double Nsamp = 2;
    wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
    wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
    for (int i = 0; i< 10; ++i){
        Nsamp *= 2.0L;
        wolffHistRun3DXY(lat,Nsamp,Trange,Ntemps);
    }
    if (lat.oPer.outputLines.size() > 0){
        lat.oPer.printData(0);
    }
}
void _3DXY::loadAndPrint(long double L,std::string maxepath,std::string warmlatpath){
    long double runTemp = 2.2018400000000L;
    Cluster c(L);
    RandStruct r;
    Lattice3DXY lat(L,runTemp,true,r,c,maxepath,warmlatpath);
    lat.loadLattice();
    lat.printVals();
}
void _3DXY::cputime_vs_delta(std::string maxepath, std::string warmlatpath){
    long double runTemp = 2.201840000000000L;
    long double system_sizes[4] = {4.0L,8.0L,16.0L,32.0L};
    long double Trange[1] = {runTemp};
    int Ntemps = 1;
    int Nsamp = 100000;
    RandStruct r;
    clock_t time;
    clock_t passed;
    for (unsigned int i = 0; i < 4; i++){
        std::cout << system_sizes[i] << std::endl << i << std::endl;
        Cluster c(system_sizes[i]);
        Lattice3DXY lat(system_sizes[i], runTemp, true, r, c, maxepath, warmlatpath);
        time = clock();
        for (int j = 0; j < 10; j++){
            wolffHistRun3DXY(lat, Nsamp, Trange, Ntemps);
            warmup(lat, 100);
        }
        passed = clock() - time;
        std::ostringstream ss;
        ss << "passed time: " << passed << std::endl;
        lat.oPer.addLine(ss.str());
        lat.oPer.printData(0);
    }
}

void _3DXY::correlationRun(std::string maxepath, std::string warmlatpath, long double L)
{
    long double runTemp = 2.2018400000000000L;
    Cluster c(L);
    RandStruct r;
    Lattice3DXY lat(L, runTemp, true, r, c, maxepath, warmlatpath);
    lat.loadLattice();
    long int N_clusts = 10000000;
    for (int i =0; i < 1; i++) 
    {
        computeWolffCorrelation(lat, N_clusts, i);
    }
}

