import os
import glob
import numpy as np

fs = glob.glob('/home/mallesh/deepvideo/data/vtl/iframes/*.png')

for f in fs:
    os.system('python ../encoder.py --model ../checkpoint/encoder_epoch_00000080.pth --input '+f+' --cuda --output codes/'+f[41:]+'.codes --iterations 5')
