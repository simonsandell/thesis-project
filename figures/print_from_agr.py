import subprocess
import time
import os
from tempfile import NamedTemporaryFile


def mk_bat(title):
    t = NamedTemporaryFile("w", delete=False)
    t.write("#asdf\n")
    t.write(r'PRINT TO "../eps_files/jul_26/' + title + r'.eps"' + "\n")
    t.write('HARDCOPY DEVICE "EPS"\n')
    t.write('PAGE SIZE 2560, 2048\n')
    t.write('DEVICE "EPS" OP "level2"\n')
    t.write('DEVICE "EPS" OP "bbox:tight"\n')
    t.write('PRINT\n')
    return t

for files in os.listdir("."):
    if ".agr" in files:
        title = files.rstrip(".agr")
        f = mk_bat(title)
        f.flush();
        cmd  = ['gracebat',"./"+files, '-batch', f.name, '-nosafe','-noask' ]
        print(cmd)
        subprocess.call(cmd)
        time.sleep(0.4)

