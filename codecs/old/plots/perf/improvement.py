import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 50})
matplotlib.rcParams['figure.figsize'] = 16, 10

fig, ax = plt.subplots()
fig.tight_layout()
fig.subplots_adjust(left=0.15, top=0.96, right=0.98)

lines = open('improvement.txt', 'r')

bpp1 = []
itr = []
onetime = []

for line in lines:
    line = line.strip().split(',')
    bpp1.append(float(line[0]))
    itr.append(float(line[1]))
    onetime.append(float(line[2]))


lines = open('h264.txt', 'r')
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


ind = np.arange(len(onetime))  # the x locations for the groups
width = 0.2       # the width of the bars
rects1 = ax.bar(ind, onetime, width, edgecolor='k', color='skyblue', linewidth=4, label='Onetime')
rects2 = ax.bar(ind+width, itr, width, edgecolor='k', color='magenta', linewidth=4, label='Iterative')

plt.ylim([0.84, 1])

ax.set_ylabel('MS-SSIM')
ax.set_xlabel('Number of Enhancement Codes')
ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')
plt.xticks(ind+width, [1, 2, 3, 4, 5, 6])
ax.set_yticklabels([0.84, 0.88, 0.92, 0.94, 0.98])

plt.legend(ncol=2)

plt.savefig('quality.pdf')

plt.show()
