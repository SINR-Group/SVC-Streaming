import os
import time

for level in range(2, 5):
    os.system('bash train.sh 2 '+str(level))
