import pickle
import collections

def saveData(data, fName="graph"):
    with open("./averages/{filename}.pickle".format(filename=fName), "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
def loadData(fName="graph"):
    with open("./averages/{filename}.pickle".format(filename=fName), "rb") as f:
        data = pickle.load(f);
    return data;

