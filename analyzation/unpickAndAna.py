import pickle
import sys
import numpy as np

import pickler

data = pickler.loadData(sys.argv[1]);

print(data[0])
