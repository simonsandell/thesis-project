import sys
import numpy as np
import math

#
#read raw data from file in ./output
##########################################################
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
arguments = sys.argv
fName = arguments[1]
L = int(arguments[2])
print(L)
dataIn = open("./output/" + fName,"r")
dataOut = open("./output/"+fName+str(arguments[2]),"w");
#load data and form array
for ln in dataIn:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [int(float(x)) for x in strlist] 
    if (fllist[0] == L):
        dataOut.write(ln);
