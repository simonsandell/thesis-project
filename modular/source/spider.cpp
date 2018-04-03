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
	ThreadPool pool(12);
	std::vector< std::future<void> > results;
	for(int i = 0; i < 12; ++i) {
		results.emplace_back(
				pool.enqueue([i] {
					_3DXY::teqRun(4.0L,true);
					_3DXY::teqRun(8.0L,true);
					_3DXY::teqRun(16.0L,true);
					_3DXY::teqRun(32.0L,true);
					_3DXY::teqRun(64.0L,true);
					})
				);
	}
}

