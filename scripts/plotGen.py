from plotting import datatableToPlots
import settings


dirpath = settings.datatables_path + "July_20_2018/"
tag = settings.TAG
datatableToPlots.datatableToPlots(dirpath, tag)
