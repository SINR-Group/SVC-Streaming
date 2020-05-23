import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 48})
matplotlib.rcParams['figure.figsize'] = 18, 10

tf = open('results.txt', 'r')
lines = tf.readlines()[1:]

encoding = []
iterative = []
onetime = []

for line in lines:
    line = line.strip().split('\t')
    encoding.append(float(line[1]))
    iterative.append(float(line[2]))
    onetime.append(float(line[3]))

ind = np.arange(len(encoding))  # the x locations for the groups
width = 0.25       # the width of the bars
fig, ax = plt.subplots()
fig.tight_layout()
fig.subplots_adjust(left=0.12, right=0.95)

rects1 = ax.bar(ind, encoding, width, edgecolor='k', color='orange', linewidth=4, label='Encoding')
rects2 = ax.bar(ind+width+0.03, iterative, width, edgecolor='k', color='skyblue', linewidth=4, label='Iterative')
rects2 = ax.bar(ind+2*width+0.06, onetime, width, edgecolor='k', color='magenta', linewidth=4, label='Onetime')

ax.set_ylabel('Latency (ms)')
ax.set_xlabel('Number of enhancement codes')
ax.set_xticks(ind+(width+0.04)/2)
plt.legend(ncol=1, loc='upper left')

plt.ylim([0, 500])

ax.set_xticklabels([1, 2, 3, 4, 5, 6])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.savefig('latency.pdf')
plt.show()
