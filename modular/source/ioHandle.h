#ifndef IOHANDLE_H
#define IOHANDLE_H
#include <string>
#include <vector>

struct outPutter {
	std::vector<std::string> outputLines;
	void addLine(std::string ln);
	void printData();
};
#endif

