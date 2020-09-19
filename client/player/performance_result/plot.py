import json
import matplotlib.pyplot as plt 

filePath = 'results_lol_60Bola.json'
bitrates = [214.915, 562.660, 990.946, 1520.727, 2963.872] #kbits per sec

def plotTputAndBitrate(perf_results, ax):

    total_segments = 60
    tput = [0] * total_segments
    bitVals = [0] * total_segments
    x1 = []
    for idx in range(total_segments):
        x1.append(idx)
        # print(data[k]['bitrate_change'])
        bitVals[idx] = perf_results['bitrate_change'][idx][1] * 0.001
        tput[idx] = perf_results['tput_observed'][idx][1]
    
    ax.plot(x1, tput, label = "tput")
    ax.plot(x1, bitVals, label = 'bitrate')
    # ax.set_xlabel('Segment No.')
    ax.set_ylabel('bandwidth (kbitps)')
    ax.legend()
    ax.set_title(k)
    # plt.show()
    print(k)

def plotBuffer(perf_results, ax):

    total_segments = 60
    bufferLevel = [0] * total_segments
    bitVals = [0] * total_segments
    x1 = []
    for idx in range(total_segments):
        x1.append(idx)
        # print(data[k]['bitrate_change'])      
        bufferLevel[idx] = perf_results['buffer_level'][idx][1]
    
    ax.plot(x1, bufferLevel, label = "buffer Level")

    # plt.plot(x1, bitVals, label = 'bitrate')
    ax.set_xlabel('Segment No.')
    ax.set_ylabel('buffer (sec)')
    ax.legend()
    # ax.set_title(k)
    # plt.show()
    print(k)


with open(filePath, 'r') as f:
    data = json.load(f)

    for k in data.keys():
        fig, (ax1, ax2) = plt.subplots(2,1)
        # plt.title(k)

        plotTputAndBitrate(data[k], ax1)
        plotBuffer(data[k], ax2)
        plt.tight_layout()

        
        plt.savefig('_'.join(k.split('/'))+'.png')

