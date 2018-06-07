import pickle
import numpy as np


def saveData(data, fName):
    n_bytes = data.size * data.dtype.itemsize
    max_bytes = 2 ** 31 - 1
    bytes_out = pickle.dumps(data)
    with open("./pickles/{filename}.pickle".format(filename=fName), "wb") as f:
        for idx in range(0, n_bytes, max_bytes):
            f.write(bytes_out[idx : idx + max_bytes])


def loadData(fName="graph"):
    filepath = "./pickles/{filename}.pickle".format(filename=fName)
    bytes_in = bytearray(0)
    input_size = os.path.getsize(filepath)
    max_bytes = 2 ** 32 - 1
    with open(filepath, "rb") as f:
        for _ in range(0, input_size, max_bytes):
            bytes_in += f.read(max_bytes)

    data = pickle.loads(bytes_in)
    return data
