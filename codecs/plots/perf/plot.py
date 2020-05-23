import os
import matplotlib.pyplot as plt

lines = open('ssim.txt', 'r')

bpp = []
itr = []
onetime = []

for line in lines:
    line = line.strip().split('\t')
    bpp.append(float(line[0]))
    itr.append(float(line[1]))
    onetime.append(float(line[2]))

plt.plot(bpp, itr)
plt.plot(bpp, onetime)

plt.show()
