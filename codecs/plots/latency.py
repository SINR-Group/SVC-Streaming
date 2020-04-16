import os
import numpy as np

itrs = [i for i in range(1, 11)]
hrch = [i for i in range(3)]

total_enc_time = {}
total_dec1_time = {}
total_dec2_time = {}
for itr in itrs:
    total_enc_time[itr] = 0
    total_dec1_time[itr] = 0
    total_dec2_time[itr] = 0
    for h in hrch:
        path = '../vcodec/vtl_output/hrch_'+str(h)+'_itr'+str(itr)+'/results.txt'
        f = open(path, 'r')
        lines = f.readlines()[173:-1]
        enc = []
        dec1 = []
        dec2 = []
        for line in lines:
            line = line.strip().split(':')[1:]
            enc.append(int(line[1].split('\t')[0][1:-3]))
            dec1.append(int(line[2].split('\t')[0][1:-3]))
            dec2.append(int(line[3][1:-2]))
        #print (h, itr, np.mean(enc), np.mean(dec1), np.mean(dec2))
        total_enc_time[itr] += np.mean(enc)/1000.0
        total_dec1_time[itr] += np.mean(dec1)/1000.0
        total_dec2_time[itr] += np.mean(dec2)/1000.0
print (total_enc_time)
print (total_dec1_time)
print (total_dec2_time)

tf = open('results.txt', 'w')

for itr in itrs:
    tf.write('{}\t{}\t{}\n'.format(total_enc_time[itr], total_dec1_time[itr], total_dec2_time[itr]))
tf.close()
