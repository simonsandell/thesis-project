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
void printOutput(Lattice lat, long double T, long double E, long double E2, long double M, long double M2, long double M4, long double M2E, long double M4E, long double SX2, long double SY2, long double SZ2, long double bin, long double dbdt, long double xi, long double rs, long double expFac){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);
	std::stringstream sstrm;
	sstrm.precision(dbl::max_digits10 + 5);

	sstrm << std::fixed << lat.L << " ";				
	sstrm << std::fixed << T << " ";				
	sstrm << std::fixed << lat.Neqsweeps << " ";			
	sstrm << std::fixed << lat.Neqclusts << " ";			
	sstrm << std::fixed << lat.Nsmsweeps << " ";			
	sstrm << std::fixed << lat.Nsmclusts << " ";			
	sstrm << std::fixed << lat.coldstart << " ";				
	sstrm << std::fixed << E << " ";				
	sstrm << std::fixed << E2 << " ";				
	sstrm << std::fixed << M << " ";				
	sstrm << std::fixed << M2 << " ";				
	sstrm << std::fixed << M4 << " ";				
	sstrm << std::fixed << M2E << " ";				
	sstrm << std::fixed << M4E << " ";				
	sstrm << std::fixed << SX2 << " ";				
	sstrm << std::fixed << SY2 << " ";				
	sstrm << std::fixed << SZ2 << " ";				
	sstrm << std::fixed << bin << " ";				
	sstrm << std::fixed << dbdt << " ";				
	sstrm << std::fixed << xi << " ";				
	sstrm << std::fixed << rs << " ";				
	sstrm << std::fixed << expFac << " ";			
	sstrm << std::endl;				
	std::cout << sstrm.str();
}

long double getMaxE(long double L){
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/maxE/" << L << "_maxE.txt";
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
	mstream << exePath<< "/maxE/" << L <<"_"<< buffer;
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

