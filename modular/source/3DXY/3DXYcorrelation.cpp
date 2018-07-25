#include <iostream>
#include <sstream>

#include "3DXYcorrelation.h"
#include "3DXYlattice.h"
#include "3DXYwolff.h"


void print_line(Lattice3DXY &lat, long double time, long int n_cl, int jnum)
{
    //prepare one string will all lines
    // send to output via lat.oPer.addLine()
    // L runTemp xmag ymag 
    typedef std::numeric_limits<long double> dbl;
    std::cout.precision(dbl::max_digits10 + 5);
    std::stringstream sstrm;
    sstrm.precision(dbl::max_digits10 + 5);

    sstrm << std::fixed << lat.L << " ";	//0
    sstrm << std::fixed << lat.runTemp << " ";	//1
    sstrm << std::fixed << lat.xmag << " ";	//2
    sstrm << std::fixed << lat.ymag << " ";    	//3
    sstrm << std::fixed << time << " ";         //4
    sstrm << std::fixed << n_cl << " ";         //5
    sstrm << std::fixed << jnum << " ";         //6
    sstrm << std::endl;				
    lat.oPer.addLine(sstrm.str());

}
void computeWolffCorrelation(Lattice3DXY &lat, long int n_clusters, int jack_num )
{
    long double total_time = 0.0L;
    for (int i =0; i < n_clusters; i++)
    {
        total_time += cluster3DXY(lat);
        print_line(lat, total_time, i, jack_num);
    }

}

