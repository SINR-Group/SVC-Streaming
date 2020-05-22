import os

for level in range(5):
    os.system('bash train.sh 2 '+str(level))
