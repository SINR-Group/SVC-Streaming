from .abr import abr
import math

# this is in terms of segments
MINIMUM_SAFE_BUFFER = 10 #Qlow
MAXIMUM_TARGET_BUFFER = 60 #Qmax

# NOTE: here should utilities be calculated once instead of every time for new segment?

class Bola(abr):
    def __init__(self, video_properties, args):
        super(Bola, self).__init__(video_properties, args)

        bitrates = self.getBitrateList()
        self.bitrates = sorted(bitrates)
        
        # buffer size in s
        self.buffer_size = args.bufferSize

        global MINIMUM_SAFE_BUFFER, MAXIMUM_TARGET_BUFFER

        MAXIMUM_TARGET_BUFFER = self.buffer_size 

        # default value for gamma variable is set to 5(as said in paper). and V is calculated as 
        # specified by paper.
        # self.gp = args.gp

        # Vp calculated freshly for each new segment
        # self.Vp = (self.buffer_size - self.segment_size) / (self.utilities[-1] + self.gp)
        
        # print('Bola utilities ', self.utilities)
        # print("Bola vp ", self.Vp)
        # print('Bola gp ', self.gp)
        self.calculateParameters()
    

    def calculateParameters(self, seg_idx=1):

        seg_sizes = self.video_properties['segment_size_bytes'][seg_idx]
        sM = seg_sizes[0] # NOTE: it assumes that size in json are stored in ascending order

        self.utilities = [math.log(s/sM) for s in seg_sizes]
        
        bitMin = self.bitrates[0]
        self.utilities = [math.log(b/bitMin) for b in self.bitrates]

        alpha = (seg_sizes[0] * self.utilities[1] - seg_sizes[1] * self.utilities[0]) / (seg_sizes[1] - seg_sizes[0])

        self.V = (MAXIMUM_TARGET_BUFFER - MINIMUM_SAFE_BUFFER) / (self.utilities[-1] - alpha)

        self.gp = (self.utilities[-1] * MINIMUM_SAFE_BUFFER - alpha * MAXIMUM_TARGET_BUFFER) / (MAXIMUM_TARGET_BUFFER - MINIMUM_SAFE_BUFFER)

        self.V = 0.93
        self.gp = 5

        self.gp = 1 - self.utilities[0] + (self.utilities[-1] - self.utilities[0]) / (MAXIMUM_TARGET_BUFFER / MINIMUM_SAFE_BUFFER - 1)
        self.V = MINIMUM_SAFE_BUFFER / (self.utilities[0] + self.gp - 1)

        # print('Bola Utilities:{}'.format(self.utilities))
        # print('Bola alpha:{}'.format(alpha))
        # print('Bola V:{}'.format(self.V))
        # print('Bola gp:{}'.format(self.gp))
        # print('Minmum:{} Maxi:{}'.format(MINIMUM_SAFE_BUFFER, MAXIMUM_TARGET_BUFFER))
        # self.V = (self.buffer_size - self.segment_size) / (self.utilities[-1] + self.gp)

    def getBitrateFromBuffer(self, bufferLevel, seg_idx):

        seg_sizes = self.video_properties['segment_size_bytes'][seg_idx]
        quality = 0
        score = None
        for q in range(len(self.bitrates)):
            # s = ((self.V * (self.utilities[q] + self.gp) - level) / seg_sizes[q])
            s = ((self.V * (self.utilities[q] + self.gp) - bufferLevel) / self.bitrates[q])
            # print('level:{}, quality:{}, score:{}'.format(bufferLevel, q, s))
            if score == None or s >= score:
                quality = q
                score = s
        
        # print('bola quality:{}'.format(quality))
        return self.bitrates[quality]
        

    def getNextBitrate(self, playerStats):

        bufferLevel = playerStats['currBuffer']
        seg_Idx = playerStats['segment_Idx']

        self.calculateParameters(seg_Idx)
        quality = self.getBitrateFromBuffer(bufferLevel, seg_Idx)

        return quality

        

