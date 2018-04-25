#include <mpi.h>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>

#include "ioHandle.h"
void outPutter::addLine(std::string ln){
	outputLines.emplace_back(ln);
	if (outputLines.size() > 4){
		printData(0);
	}
}

void outPutter::printData(int tag){
	int sz = outputLines.size();
	std::stringstream sstrm;
	for (int i = 0; i<sz; ++i){
		sstrm << outputLines[i];
	}
	std::string bigstr = sstrm.str();
	MPI_Send(bigstr.c_str(),bigstr.size(),MPI_CHAR,0,tag,MPI_COMM_WORLD);
	outputLines.clear();
}

