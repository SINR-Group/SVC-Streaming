import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 50})
matplotlib.rcParams['figure.figsize'] = 20, 10

fig, ax = plt.subplots()
fig.tight_layout()
fig.subplots_adjust(left=0.15, top=0.96, right=0.96)

lines = open('ssim.txt', 'r')

bpp1 = []
itr = []
onetime = []

for line in lines:
    line = line.strip().split(',')
    print (line)
    bpp1.append(float(line[0]))
    itr.append(float(line[1]))
    onetime.append(float(line[2]))


lines = open('vp9.txt', 'r')
bpp2 = []
h264 = []
for line in lines:
    line = line.strip().split(' ')
    bpp2.append(float(line[0]))
    h264.append(float(line[1]))

lines = open('h265.txt', 'r')
bpp3 = []
h265 = []
for line in lines:
    line = line.strip().split(' ')
    bpp3.append(float(line[0]))
    h265.append(float(line[1]))

plt.plot(bpp1, onetime, marker='D', color='magenta', markersize=24, markeredgecolor='black', linewidth=6, label='Residual-Onetime')
plt.plot(bpp1, itr, marker='s', color='skyblue', markersize=20, markeredgecolor='black', linewidth=6, label='Residual-Iterative')
plt.plot(bpp2, h264, marker='^', color='orange', markersize=32, markeredgecolor='black', linewidth=12, label='H.265')
plt.plot(bpp3, h265, marker='o', color='maroon', markersize=28, markeredgecolor='black', linewidth=12, label='VP9')

#plt.ylim([0.85, 1])
plt.xlim([0.5, 1])
#ax.set_yticklabels(np.arange(7), [0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96])

ax.set_ylabel('MS-SSIM')
ax.set_xlabel('BPP')
ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')
ax.xaxis.grid(linestyle='dotted')

plt.legend(loc='lower right')

plt.savefig('comparison.pdf')

plt.show()
