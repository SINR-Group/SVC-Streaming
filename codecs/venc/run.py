import os
import time 

levels = ['0', '1', '2']
bits = ['8', '16', '24', '32', '48', '56', '64']

for b in bits:
    for l in levels:
        os.system('bash train.sh '+l+' '+b)
