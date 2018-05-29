import oneLana
import settings
import subprocess



filelist =[
        "4combined_reduced.npy",
        "8combined_reduced.npy",
        "16combined_reduced.npy",
        "32combined_reduced.npy",
        "64combined_reduced.npy",
        "128combined_reduced.npy"];
for f in filelist:
    subprocess.call(["python3",settings.scripts_path+"oneLana.py",settings.pickles_path+f,settings.model]);
