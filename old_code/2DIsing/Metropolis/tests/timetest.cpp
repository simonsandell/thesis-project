#include <iostream>
#include <iomanip>
#include <ctime>
#include <string>
#include <sstream>
using namespace std;
int main(){

	auto t = std::time(nullptr);
	auto tm = *localtime(&t);

	ostringstream oss;
	oss <<  put_time(&tm,"%Y-%m-%d %H:%M:%S");
	auto str = oss.str();
	cout << str << endl;

}
