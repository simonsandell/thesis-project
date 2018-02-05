#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <thread>
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include "threadpool/boost/threadpool.hpp"
#include <ctime>

#include "wolffRun.h"
#include "wolffHistRun.h"

using namespace std;
using namespace boost::threadpool;
//
//public variables 
//Parameters
//
double L;
double N_equil;
double N_sampl;
bool cold;
int index_temp;
double *Temps;
int N_temps;
//
//
void wr(){
	wolffRun(L,N_equil,N_sampl,cold,Temps[index_temp]);
}

void whr(){
	wolffHistRun(L,N_equil,N_sampl,cold,Temps,N_temps);
}

double * getTrange(double start, double end, int N){
	double dt = (end-start)/((double)N-1.0);
	double *T = new double[N];
	for (int i =0; i< N; ++i){
		T[i] = start + (double)i*dt;
	}
	return T;
}

void doThreadPool(){
	unsigned concurentThreadsSupported = std::thread::hardware_concurrency();
	cout << concurentThreadsSupported << endl;
	pool tp(concurentThreadsSupported);
	int N_runs = 1;
	for (int i = 0; i <N_runs; ++i){
		for (int j = 0; j< N_temps;++j){
			index_temp = j;
			tp.schedule(&wr);
		}
	}
}
void doThreadPool2(){
	pool tp(1);
	int N_runs = 1;
	for (int i = 0; i <N_runs; ++i){
		for (int j = 0; j< N_temps;++j){
			index_temp = j;
			tp.schedule(&wr);
		}
	}
}

//main
int main(int argc, char* argv[]){
	struct timespec start,middle, finish;
	double elapsed, elapsed2;
	clock_gettime(CLOCK_MONOTONIC,&start);
	//initialize parameters
	L = 8.0;
	N_equil = 2000.0;
	N_sampl = 3000.0;
	cold =false;
	index_temp = 0;
	N_temps = 8;
	Temps = getTrange(2.2,2.22,N_temps);
	//
	cout.precision(17);

	doThreadPool();
	clock_gettime(CLOCK_MONOTONIC,&middle);
	elapsed = (middle.tv_sec - start.tv_sec);
	elapsed += (middle.tv_nsec - start.tv_nsec)/1000000000.0;
	cout << elapsed << endl;
	doThreadPool2();
	clock_gettime(CLOCK_MONOTONIC,&finish);
	elapsed2 = (finish.tv_sec - middle.tv_sec);
	elapsed2 += (finish.tv_nsec - middle.tv_nsec)/1000000000.0;
	cout << elapsed2 << endl;
}
