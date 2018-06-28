import numpy as np
import settings

tag = "jun_26"
pth = settings.datatables_path + "June_26_2018/"
filelist = [
    np.load(pth + "datatable_4.0jun_153DXY.npy"),
    np.load(pth + "datatable_8.0jun_153DXY.npy"),
    np.load(pth + "datatable_16.0jun_153DXY.npy"),
    np.load(pth + "datatable_32.0jun_263DXY.npy"),
    np.load(pth + "datatable_64.0jun_263DXY.npy"),
    np.load(pth + "datatable_128.0jun_263DXY.npy"),
]

combined = np.empty((len(filelist), *filelist[0].shape))
print(combined.shape)

for i, fil in enumerate(filelist):
    combined[i, :, :] = fil[ :, :]
np.save(pth + "datatable_combined", combined)
