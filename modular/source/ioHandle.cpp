#include <iostream>
#include <vector>
#include <string>

#include "ioHandle.h"
void outPutter::addLine(std::string ln){
	outputLines.emplace_back(ln);
	if (outputLines.size() > 999){

		printData();
	}
}

void outPutter::printData(){
	int sz = outputLines.size();
	for (int i = 0; i<sz; ++i){
		std::cout << outputLines[i];
	}
	outputLines.clear();
}

