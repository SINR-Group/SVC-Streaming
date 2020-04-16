import os
import numpy as np

itrs = [i for i in range(1, 11)]
hrch = [i for i in range(3)]

for h in hrch:
    for itr in itrs:
        path = '../vcodec/vtl_output/hrch_'+str(h)+'_itr'+str(itr)+'/results.txt'
        f = open(path, 'r')
        lines = f.readlines()[173:-1]
        enc = []
        dec1 = []
        dec2 = []
        for line in lines:
            line = line.strip().split(':')[1:]
            #print line[1]#, line[2], line[3]
            enc.append(int(line[1].split('\t')[0][1:-3]))
        print h, itr, np.mean(enc)
