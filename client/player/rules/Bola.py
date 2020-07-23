from abr import abr
import math

# calculated from zip files, for each bitrate, from 1 to 5. in kBs
file_sizes = [112.22, 256.50, 577.10, 801.49, 1234.25]

MINIMUM_SAFE_BUFFER = 10
MAXIMUM_TARGET_BUFFER = 30

# NOTE: here should utilities be calculated once instead of every time for new segment?

class Bola(abr):
    def __init__(self, video_properties, args):
        super(Bola, self).__init__(video_properties, args)

        bitrates = self.getBitrateList()
        self.bitrates = sorted(bitrates)
        
        # buffer size in s
        self.buffer_size = args.bufferSize

        self.segment_duration = self.getSegmentDuration()

        # default value for gamma variable is set to 5(as said in paper). and V is calculated as 
        # specified by paper.
        # self.gp = args.gp

        # Vp calculated freshly for each new segment
        # self.Vp = (self.buffer_size - self.segment_size) / (self.utilities[-1] + self.gp)
        
        # print('Bola utilities ', self.utilities)
        # print("Bola vp ", self.Vp)
        # print('Bola gp ', self.gp)
    

    def calculateParameters(self, minmum_buffer, target_buffer, seg_idx):

        seg_sizes = self.video_properties['segment_size_bytes'][seg_idx]
        sM = seg_sizes[0] # NOTE: it assumes that size in json are stored in ascending order

        self.utilities = [math.log(s/sM) for s in seg_sizes]

        self.gp = 1 - self.utilities[0] + (self.utilities[-1] - self.utilities[0]) / (target_buffer / minmum_buffer - 1)
        self.Vp = minmum_buffer / (self.utilities[0] + self.gp - 1)

        # self.Vp = (self.buffer_size - self.segment_size) / (self.utilities[-1] + self.gp)

    def getNextBitrate(self, playerStats):

        self.calculateParameters(MINIMUM_SAFE_BUFFER, MAXIMUM_TARGET_BUFFER, playerStats['segment_Idx'])
        
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

