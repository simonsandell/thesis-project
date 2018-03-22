#include <iostream>
#include <cmath>
#include <utility>
#include <tuple>
#include <limits>
#include <vector>
#include <chrono>

#include "ThreadPool.h"
#include "clusterStruct.h"
#include "randStruct.h"

#include "Ising3D.h"
#include "3DXY.h"
using namespace std;


//main
//
int main(){
	ThreadPool pool(1);
	std::vector< std::future<void> > results;
	for(int i = 0; i < 1; ++i) {
		results.emplace_back(
				pool.enqueue([i] {
					_3DXY::wolffHistJob(5.0L);
					})
				);
	}
}

