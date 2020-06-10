from abr import abr
import math

# calculated from zip files, for each bitrate, from 1 to 5. in kBs
file_sizes = [112.22, 256.50, 577.10, 801.49, 1234.25]


class Bola(abr):
    def __init__(self, manifestData, args):
        super(Bola, self).__init__(manifestData)

        bitrates = self.getBitrateList()
        self.bitrates = sorted(bitrates)
        
        sM = file_sizes[0] # minimum file size.
        self.utilities = [math.log(s/sM) for s in file_sizes]
        
        # buffer size in ms
        self.buffer_size = args.bufferSize

        rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]
        self.segment_size = (rep.duration / rep.timescale)

        # default value for gamma variable is set to 5(as said in paper). and V is calculated as 
        # specified by paper.
        self.gp = args.gp
        self.Vp = (self.buffer_size - self.segment_size) / (self.utilities[-1] + self.gp)
        
        # print('Bola utilities ', self.utilities)
        # print("Bola vp ", self.Vp)
        # print('Bola gp ', self.gp)
    
    def getNextBitrate(self, playerStats):

        level = playerStats['currBuffer']
        quality = 0
        score = None
        for q in range(len(self.bitrates)):
            s = ((self.Vp * (self.utilities[q] + self.gp) - level) / file_sizes[q])
            # print('level:{}, quality:{}, score:{}'.format(level, q, s))
            if score == None or s >= score:
                quality = q
                score = s
        
        # print('bola quality:{}'.format(quality))
        return self.bitrates[quality]

