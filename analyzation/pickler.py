import pickle
import collections

def saveData(data, filename="graph"):
    with open(f"./averages/{filename}.pickle", "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
def loadData(filename="graph"):
    with open(f"./averages/{filename}.pickle", "rb") as f:
        data = pickle.load(f);
    return data;

