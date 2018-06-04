import oneLana
import settings
import subprocess



filelist =[
        "flat.npy"
        ,"reg.npy"]
for f in filelist:
    subprocess.call(["python3",settings.scripts_path+"oneLana.py",settings.pickles_path+f,settings.model]);
