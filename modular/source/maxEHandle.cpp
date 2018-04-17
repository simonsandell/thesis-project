#include <string>
#include <ctime>
#include <sstream>
#include <limits>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "maxEHandle.h"
long double getMaxE(std::string path,long double L){
	std::ostringstream mstream;
	mstream << path << L << "_maxE.txt";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	long double maxE;
	file >> std::fixed >> maxE;
	if (abs(maxE) < 1.0L){
		std::cout << maxE << std::endl;
		std::cout << path << std::endl;
		std::cout << L<< std::endl;
		std::cout << "failed to get MaxE" << std::endl;
		exit(1);
	}
	return maxE;
}
void setMaxE(std::string path,long double L,long double newE){

	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	mstream << path << L <<"_"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}
