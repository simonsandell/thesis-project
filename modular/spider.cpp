#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <thread>
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include "threadpool/boost/threadpool.hpp"

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;
using namespace boost::threadpool;
class makeRunFuncs {
	bool hist;
	double L, N_equil, N_samp;
	bool cold;
	double T;
	double *Temps;
	int N_temps;
	public:
	  void setParams(bool,double,double,double,bool,double,double*,int);
	  void wolff();
	  void histWolff();
};
void makeRunFuncs::setParams(bool h,double l,double neq,double nsam,bool c,double t,double* tmps,int ntmps){
	L=l; N_equil=neq; N_samp=nsam;
	cold=c;
	T = t;
	Temps= tmps;
	N_temps = ntmps;
}
void makeRunFuncs::wolff(){
	wolffRun(L,N_equil,N_samp,cold,T);
}
void makeRunFuncs::histWolff(){
	wolffHistRun(L,N_equil,N_samp,cold,Temps,N_temps);
}


double * getTrange(double start, double end, int N){
	double dt = (end-start)/((double)N-1.0);
	double *T = new double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (double)i*dt;
	}
	return T;
}

//main
int main(int argc, char* argv[]){

	//
	cout.precision(17);
	makeRunFuncs mrf;
	unsigned concurentThreadsSupported = std::thread::hardware_concurrency();
	pool tp(concurentThreadsSupported);

	//PARAMS
	int N_runs = 10;
	int N_temps= 10;
	double* Temps = getTrange(2.2,2.22,N_temps);
	double L = 8;

	for (int i = 0; i <N_runs; ++i){
		for (int j = 0; j< N_temps;++j){
			mrf.setParams(false,L,2000,2000,true,Temps[0],Temps,N_temps);
			boost::function<void()> asdf(boost::bind(&makeRunFuncs::wolff, mrf));
			tp.schedule(&asdf);
		}
	}
}
