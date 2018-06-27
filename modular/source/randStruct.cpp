#include <random>
#include <iostream>
#include <sys/syscall.h>
#include <functional>
#include <unistd.h>
#include <ctime>
#include <mpi.h>

#include "randStruct.h"
RandStruct::RandStruct(){
	//get and set seed
	//syscall(SYS_getrandom,&seed,sizeof(unsigned long int),0);	
	//
	//
	int rank;
	int nulltime = time(NULL);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	srand((unsigned)nulltime*rank);
	seed = rand();
	std::cout << "SEED " << seed << std::endl;
	std::uniform_real_distribution<long double> temp_dist(0.0L,1.0L);
	dist = temp_dist;
	std::mt19937_64 temp_eng; 
	eng = temp_eng;
	eng.seed(seed);
}
RandStruct::RandStruct(unsigned long int s){

    seed = s;
    std::cout << "SEED " << seed << std::endl;
    std::uniform_real_distribution<long double> temp_dist(0.0L,1.0L);
    dist = temp_dist;
    std::mt19937_64 temp_eng;
    eng = temp_eng;
    eng.seed(seed);
}

long double RandStruct::rnd(){
    long double ret = dist(eng);
    //std::cout << "randStruct gives " <<  ret << std::endl;
    return ret;
}
