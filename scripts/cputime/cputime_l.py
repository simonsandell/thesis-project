import sys

def time(L):
    A = 0.000432888
    B = 2.96398
    print(A*(pow(L,B)))

time(4);
time(8);
time(16);
time(32);
time(64);
time(128);
