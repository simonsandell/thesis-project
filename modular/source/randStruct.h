#ifndef RANDSTRUCT_H
#define RANDSTRUCT_H

#include <random>


struct RandStruct{
	std::mt19937_64 eng;
	std::uniform_real_distribution<long double> dist;	
	unsigned long int seed;

	RandStruct();
        RandStruct(unsigned long int s);

	long double rnd();

};

#endif
