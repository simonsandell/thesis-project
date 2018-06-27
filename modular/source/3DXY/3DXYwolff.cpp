#include <cmath>
#include <random>
#include <utility>
#include <tuple>
#include <vector>
#include <iostream>

#include "3DXYlattice.h"
#include "../randStruct.h"
#include "../clusterStruct.h"

std::tuple<int,int,int> kToXYZ(unsigned long int K, int int_L){
	int x = K % int_L;
	int yL = (K-x)%(int_L*int_L);
	int zLL = (K-x-yL);
	int y = int((yL+0.1)/int_L);
	int z = int((zLL+0.1)/(int_L*int_L));
	std::tuple<int,int,int> ret = std::make_tuple(x,y,z);
	return ret;
}

long double getProb(long double u, long double angleParent, long double angle,long double beta){
    long double prob = 1.0L - exp(2.0L*beta*cos(angleParent - u)*cos(angle -u));
    if (prob < 0.0L){ 
        return 0.0L;
    }
    else if (prob > 1.0L){
        return 1.0L;
    }
    return prob;
}

void updateVals(Lattice3DXY& lat,
        long double e0,long double e1,
        long double a0,long double a1,
        long double sx0,long double sx1,
        long double sy0,long double sy1,
        long double sz0,long double sz1){

    lat.energy+= e1;
    lat.energy += -e0;
    lat.xmag+= cos(a1);
    lat.xmag+= -cos(a0);
    lat.ymag+= sin(a1);
    lat.ymag+= -sin(a0);
    lat.sinx+= sx1;
    lat.sinx+= -sx0;
    lat.siny+= sy1;
    lat.siny+= -sy0;
    lat.sinz+= sz1;
    lat.sinz+= -sz0;
}

void print_spin_id(int x, int y, int z){
    //std::cout << x << y << z << std::endl;
}

long double cluster3DXY(Lattice3DXY& lat){

    long double time = 1.0L;
    //select random plane and random staring spin
    long double u = -(long double)M_PI + 2.0L*((long double)M_PI)*lat.rand.rnd();
    unsigned long int kstart = lat.Nspins*lat.rand.rnd();
    std::tuple<int,int,int> xyz_tup = kToXYZ(kstart, lat.int_L);
    int s1 = std::get<0>(xyz_tup);
    int s2 = std::get<1>(xyz_tup);
    int s3 = std::get<2>(xyz_tup);
    print_spin_id(s1,s2,s3);
    // save angle and energy before flipping
    long double angleBefore = lat.theLattice[s1][s2][s3];
    long double enBefore = lat.siteEnergy(s1,s2,s3);
    long double angleAfter = (long double)M_PI + 2.0L*u - angleBefore;
    //reflect spin and mark as part of cluster
    lat.theLattice[s1][s2][s3] = angleAfter;
    lat.clust.theCluster[s1][s2][s3] = true;
    //update energy, mag etc..
    long double enAfter = lat.siteEnergy(s1,s2,s3);
    long double sxBef = lat.sinX(s1,s2,s3,angleBefore);
    long double sxAft = lat.sinX(s1,s2,s3,angleAfter);
    long double syBef = lat.sinY(s1,s2,s3,angleBefore);
    long double syAft = lat.sinY(s1,s2,s3,angleAfter);
    long double szBef = lat.sinZ(s1,s2,s3,angleBefore);
    long double szAft = lat.sinZ(s1,s2,s3,angleAfter);
    updateVals(lat,
            enBefore,enAfter,
            angleBefore,angleAfter,
            sxBef,sxAft,
            syBef,syAft,
            szBef,szAft);
    //find indices of nearest neighbours
    int n1m = (s1 -1 + lat.int_L )%lat.int_L;
    int n1p = (s1 +1 + lat.int_L )%lat.int_L;
    int n2m = (s2 -1 + lat.int_L )%lat.int_L;
    int n2p = (s2 +1 + lat.int_L )%lat.int_L;
    int n3m = (s3 -1 + lat.int_L )%lat.int_L;
    int n3p = (s3 +1 + lat.int_L )%lat.int_L;
    std::tuple<int,int,int,long double> neig1 = std::make_tuple(n1m,s2,s3,angleAfter);
    std::tuple<int,int,int,long double> neig2 = std::make_tuple(n1p,s2,s3,angleAfter);
    std::tuple<int,int,int,long double> neig3 = std::make_tuple(s1,n2m,s3,angleAfter);
    std::tuple<int,int,int,long double> neig4 = std::make_tuple(s1,n2p,s3,angleAfter);
    std::tuple<int,int,int,long double> neig5 = std::make_tuple(s1,s2,n3m,angleAfter);
    std::tuple<int,int,int,long double> neig6 = std::make_tuple(s1,s2,n3p,angleAfter);

    //make a list for perimeter spins
    std::vector<std::tuple<int,int,int,long double>> perimeter;
    //add neighbours to list
    perimeter.push_back(neig1);
    perimeter.push_back(neig2);
    perimeter.push_back(neig3);
    perimeter.push_back(neig4);
    perimeter.push_back(neig5);
    perimeter.push_back(neig6);
    int n = 6;

    std::tuple<int,int,int,long double> current;
    long double prob = 0.0L;
    long double rand = 0.0L;
    while (n > 0){
        //pick out the last element 
        current = perimeter.back();
        print_spin_id(std::get<0>(current),std::get<1>(current),std::get<2>(current));
        
        perimeter.pop_back();
        n -= 1;
        //test that it is not already part of cluster
        if (!lat.clust.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)]){

            //increase time for every tested spin
            //
            time = time +1.0L;

            //get its current angle;
            //
            angleBefore = lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)];

            //calculate prob of freezing, == 1 -exp(2*beta( parent_spin * U)( this_spin*U)) 
            prob = getProb(u,std::get<3>(current) ,angleBefore,lat.beta);
            rand = lat.rand.rnd();
            if ( rand < prob) {
                //get energy before reflecting
                //
                enBefore = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));

                //get new angle
                angleAfter = (long double)M_PI + 2.0L*u - angleBefore;

                //reflect and mark as added to cluster
                lat.theLattice[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = angleAfter;
                lat.clust.theCluster[std::get<0>(current)][std::get<1>(current)][std::get<2>(current)] = true;

                //update energy and magnetization
                enAfter = lat.siteEnergy(std::get<0>(current),std::get<1>(current),std::get<2>(current));
                sxBef = lat.sinX(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
                sxAft = lat.sinX(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
                syBef = lat.sinY(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
                syAft = lat.sinY(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
                szBef = lat.sinZ(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleBefore);
                szAft = lat.sinZ(std::get<0>(current),std::get<1>(current),std::get<2>(current),angleAfter);
                updateVals(lat,
                        enBefore,enAfter,
                        angleBefore,angleAfter,
                        sxBef,sxAft,
                        syBef,syAft,
                        szBef,szAft);
                //find indices of neighbours
                neig1 = std::make_tuple(
                        (std::get<0>(current) + lat.int_L - 1) % lat.int_L,
                        std::get<1>(current),
                        std::get<2>(current),
                        angleAfter);
                neig2 = std::make_tuple(
                        (std::get<0>(current) + 1) % lat.int_L, 
                        std::get<1>(current),
                        std::get<2>(current),
                        angleAfter);
                neig3 = std::make_tuple(
                        std::get<0>(current),
                        (std::get<1>(current) + lat.int_L - 1) % lat.int_L,
                        std::get<2>(current),
                        angleAfter);
                neig4 = std::make_tuple(
                        std::get<0>(current),
                        (std::get<1>(current) + 1) % lat.int_L,
                        std::get<2>(current),
                        angleAfter);
                neig5 = std::make_tuple(
                        std::get<0>(current),
                        std::get<1>(current),
                        (std::get<2>(current) + lat.int_L - 1)%lat.int_L,
                        angleAfter);
                neig6 = std::make_tuple(
                        std::get<0>(current),
                        std::get<1>(current),
                        (std::get<2>(current) + 1) % lat.int_L,
                        angleAfter);
                //if a neighbour is not already part of the cluster, add it to perimeter list
                if (!lat.clust.theCluster[std::get<0>(neig1)][std::get<1>(neig1)][std::get<2>(neig1)] ){
                    perimeter.push_back(neig1);
                    n = n + 1;
                }
                if (!lat.clust.theCluster[std::get<0>(neig2)][std::get<1>(neig2)][std::get<2>(neig2)] ){
                    perimeter.push_back(neig2);
                    n = n + 1;
                }
                if (!lat.clust.theCluster[std::get<0>(neig3)][std::get<1>(neig3)][std::get<2>(neig3)] ){
                    perimeter.push_back(neig3);
                    n = n + 1;
                }
                if (!lat.clust.theCluster[std::get<0>(neig4)][std::get<1>(neig4)][std::get<2>(neig4)] ){
                    perimeter.push_back(neig4);
                    n = n + 1;
                }
                if (!lat.clust.theCluster[std::get<0>(neig5)][std::get<1>(neig5)][std::get<2>(neig5)] ){
                    perimeter.push_back(neig5);
                    n = n + 1;
                }
                if (!lat.clust.theCluster[std::get<0>(neig6)][std::get<1>(neig6)][std::get<2>(neig6)] ){
                    perimeter.push_back(neig6);
                    n = n + 1;
                }
            }
        }
    }
    //empty the cluster
    lat.clust.emptyCluster();	
    //return # of tested spins
    lat.NTotSweeps += time/lat.Nspins;
    lat.NTotClusts += 1;
    std::cout << "time " << time << std::endl;
    return time;
}
