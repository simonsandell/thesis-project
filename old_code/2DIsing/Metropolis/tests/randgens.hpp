#include <random>
#include <functional>
using namespace std;


	double rand_uni(){
		return gen();
	}
	int rand_int(int max){
		int i = max*gen();
		return i;
	}
