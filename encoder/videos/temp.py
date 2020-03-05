import os
import glob

fs = glob.glob('video1/*.zip')

for f in fs:
    for i in range(300):
        os.system('cp '+f+' '+f[:-5]+str(i)+'.zip')
