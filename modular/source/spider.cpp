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
	for(int i = 0; i < 96; ++i) {
		results.emplace_back(
				pool.enqueue([i] {
					Ising3D::teqRun(4.0L,false);
					Ising3D::teqRun(8.0L,false);
					Ising3D::teqRun(16.0L,false);
					Ising3D::teqRun(32.0L,false);
					Ising3D::teqRun(64.0L,false);
					})
				);
	}
}

