import os
import sys
inf= open(sys.argv[1],"r");
for ln in inf:
    os.makedirs(ln,exist_ok=True);
