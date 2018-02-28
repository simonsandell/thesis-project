#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "ioFuncs.h"
#include "latticeStruct.h"
#include "avgStruct.h"

//print lattice
void printLattice(long double ***lattice,long double  L){
	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			for(int k =0; k<L; ++k){
				std::cout << lattice[i][j][k] << " ";
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}
}

std::string get_selfpath(){
	char buff[PATH_MAX];
	ssize_t len = ::readlink("/proc/self/exe",buff,sizeof(buff)-1);
	if (len != -1) {
		buff[len] = '\0';
		std::string strbuff = std::string(buff);
		const size_t lastslash = strbuff.rfind('/');
		strbuff = strbuff.substr(0,lastslash);
		return strbuff;
	}
	else {
		std::cout << "selfpath fail" << std::endl;
		exit(-1);
	}
}
void printOutput(Lattice lat, long double T,avgStruct avgs, long double bin, long double dbdt, long double xi, long double c){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);
	std::stringstream sstrm;
	sstrm.precision(dbl::max_digits10 + 5);

	sstrm << std::fixed << lat.L << " ";				// L	0
	sstrm << std::fixed << T << " ";				// T	1
	sstrm << std::fixed << lat.Neqsweeps << " ";			// n	2
	sstrm << std::fixed << lat.Neqclusts << " ";			// n	3
	sstrm << std::fixed << lat.Nsmsweeps << " ";			// n	4
	sstrm << std::fixed << lat.Nsmclusts << " ";			// n	5
	sstrm << std::fixed << lat.coldstart << " ";			// cold	6
	sstrm << std::fixed << avgs.e	<< " ";				// e	7
	sstrm << std::fixed << avgs.e2	<< " ";				// e2	8
	sstrm << std::fixed << avgs.m	<< " ";				// m	9
	sstrm << std::fixed << avgs.m2	<< " ";				// m2	10
	sstrm << std::fixed << avgs.m4	<< " ";				// m4	11
	sstrm << std::fixed << avgs.m2e	<< " ";				// m2e	12
	sstrm << std::fixed << avgs.m4e	<< " ";				// m4e	13
	sstrm << std::fixed << bin	<< " ";				// b	14
	sstrm << std::fixed << dbdt	<< " ";				// dbdt	15
	sstrm << std::fixed << xi	<< " ";				// xi	16
	sstrm << std::fixed << c	<< " ";				// c	17
	sstrm << std::fixed << avgs.exp << " ";				// exp 	18 
	sstrm << std::endl;				
	std::cout << sstrm.str();
}

long double getMaxE(long double L){
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/maxE/XY/" << L << "_XYmaxE.txt";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	long double maxE;
	file >> std::fixed >> maxE;
	return maxE;
}
void setMaxE(long double L,long double newE){

	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath<< "/maxE/XY/" << L <<"_XY"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}

void saveLattice(Lattice lat){

	int L = lat.L;
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath<< "/warmLattice/" << L <<"_warm.lat";
	std::string fname = mstream.str();
	FILE* output;
	output = std::fopen(fname.c_str(),"wb");
	fwrite(&lat,sizeof(lat),1,output);
	fclose(output);

}

Lattice getLattice(int l){
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/warmLattice/" << l << "_warm.lat";
	std::string fname = mstream.str();

	Lattice lat;
	FILE* input;

	input = fopen(fname.c_str(),"rb");


	fread(&lat,sizeof(lat),1,input);

	fclose(input);

	return lat;
}

