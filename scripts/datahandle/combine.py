import os 
import numpy as np

data = np.empty((0,22));
for filename in os.listdir("."):
    data = np.append(data,np.load("./"+filename),axis=0);
pwd = os.path.abspath(os.curdir).split("/")[-1];
np.save("../"+pwd+"combined",data);



