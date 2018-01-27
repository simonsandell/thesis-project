#include <iostream>
#include <string>

using namespace std;




int main(int argc, char* argv[]){

	if (argc != 3 ){

		cout << "Usage: ./a.out <L> <T>" << endl;
		return -1;
	}
	int L = atoi(argv[1]);
	double T = stod(argv[2]);
	cout << L << T << endl;
}
