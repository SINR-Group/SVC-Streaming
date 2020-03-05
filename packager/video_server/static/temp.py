import os
import glob

fs = glob.glob('24_tiles/*.m4s')

for f in fs:
    os.system('cp '+f+' codes/'+f[9:-3]+'npz')
