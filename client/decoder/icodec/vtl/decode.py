import os
import glob
import numpy as np

fs = os.listdir('codes/')

for f in fs:
    os.system('python ../decoder.py --model ../checkpoint/decoder_epoch_00000080.pth --input codes/'+f+' --cuda --output images/'+f[:-10]+' --iterations 5')
