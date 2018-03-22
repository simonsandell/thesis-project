#include <random>
#include <sys/syscall.h>
#include <functional>
#include <unistd.h>

#include "randStruct.h"
RandStruct::RandStruct(){
	//get and set seed
	syscall(SYS_getrandom,&seed,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<long double> temp_dist(0.0L,1.0L);
	dist = temp_dist;
	std::mt19937_64 temp_eng; 
	eng = temp_eng;
	eng.seed(seed);
}

long double RandStruct::rnd(){
	return dist(eng);
}
