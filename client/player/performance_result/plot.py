import json
import matplotlib.pyplot as plt 

filePath = 'results_Bola_3g.json'
bitrates = [214.915, 562.660, 990.946, 1520.727, 2963.872]

with open(filePath, 'r') as f:
    data = json.load(f)

    for k in data.keys():
        total_segments = 60
        tput = [0] * total_segments
        bitVals = [0] * total_segments
        x1 = []
        for idx in range(total_segments):
            x1.append(2*idx)
            # print(data[k]['bitrate_change'])
            bitVals[idx] = data[k]['bitrate_change'][idx][1] * 0.001
            tput[idx] = data[k]['tput_observed'][idx][1]
        
        plt.plot(x1, tput, label = "tput")
        plt.plot(x1, bitVals, label = 'bitrate')
        plt.xlabel('time(sec)')
        plt.ylabel('bandwidth')
        plt.legend()
        plt.title(k)
        plt.show()




        print(k)

