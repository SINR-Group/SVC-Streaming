import os
import numpy as np

iters = [i for i in range(1, 10)]

recframes = os.listdir('output_1/images')

bt = []
ps = []
ss = []

for itr in iters:
    b = {}
    psnr = {}
    ssim = {}

    a = []
    br = []
    c = []

    for rframe in recframes:
        bits = np.loadtxt('rd/bits_'+rframe[6:-13]+'_itr'+str(itr)+'.txt')
        quality = np.loadtxt('rd/quality_'+rframe[6:-13]+'_itr'+str(itr)+'.txt', delimiter=' ', usecols=(0, 1))
        b[rframe[6:-13]] = np.mean(bits)
        a.append(np.mean(bits))
        psnr[rframe[6:-13]] = np.mean(quality[:, 0][:-8])
        br.append(np.mean(quality[:, 0][:-8]))
        ssim[rframe[6:-13]] = np.mean(quality[:, 1][:-8])
        c.append(np.mean(quality[:, 1][:-8]))

    bt.append(np.mean(a))
    ps.append(np.mean(br))
    ss.append(np.mean(c))

    #for k in b:
    #    print (k, b[k], psnr[k], ssim[k])
    #print('\n\n')

for i, j, k in zip(bt, ps, ss):
    print (i, j, k)
