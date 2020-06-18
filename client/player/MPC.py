from abr import abr
import math
from collections import deque
import itertools
import time

MPC_STARTUP_STATE = "startup"
MPC_STEADY_STATE = "steady"

look_ahead_segments = 2
keep_past_segment = 5

# bitrate combinations for look_ahead_segments. will be used to calculate QOE.
bitrate_combination = list(itertools.product(range(5), repeat = look_ahead_segments))


LAMBDA = 1
MU = MUs = 3000

class MPC(abr):
    def __init__(self, manifestData, video_properties):
        super(MPC, self).__init__(manifestData, video_properties)
        print('USING MPC abr')
        self.prev_tput_pred = deque()
        self.prev_tput_observed = deque()
        self.state = MPC_STEADY_STATE
        self.prev_bitrate = 0

    
    def getNextBitrate(self, playerStats):
        if playerStats['lastTput_kbps']:
            self.prev_tput_observed.append(playerStats['lastTput_kbps'])

        if len(self.prev_tput_observed) > keep_past_segment:
            self.prev_tput_observed.popleft()
        
        tput_pred = self.throughput_pred()

        if self.state == MPC_STARTUP_STATE:
            next_bitrate , ts = self.f_MPC(self.prev_bitrate, playerStats['currBuffer'], tput_pred, playerStats['segment_Idx'])
            
        elif self.state == MPC_STEADY_STATE:
            next_bitrate = self.f_MPC(self.prev_bitrate, playerStats['currBuffer'], tput_pred, playerStats['segment_Idx'])
            
        
        return next_bitrate
    
    def f_MPC(self, prev_bitrate, buffer_level, tput_pred, segment_idx):

        sTime = time.time()
        max_qoe = -float('inf')
        best_bitrate = -1
        for combo in bitrate_combination:
            curr_qoe = 0
            curr_buffer = buffer_level
            seg_idx = segment_idx
            last_bitrate = prev_bitrate

            for i, b in enumerate(combo):
                curr_bitrate = self.video_properties['bitrates'][b]
                segment_size = self.video_properties['segment_size_bytes'][seg_idx][b]
                download_time = segment_size / (tput_pred * 125) # convert kilobits per sec to bytes per second 1000/8
                # print('size:{}, downloadtime:{}, tput:{}'.format(segment_size, download_time, tput_pred))
                rebuf_time =  download_time - curr_buffer
                
                curr_buffer += (self.getSegmentDuration() - download_time)

                curr_qoe += curr_bitrate
                curr_qoe -= (LAMBDA * abs(last_bitrate - curr_bitrate))
                curr_qoe -= (MU * rebuf_time)

                last_bitrate = curr_bitrate
            
            if curr_qoe > max_qoe:
                max_qoe = curr_qoe
                best_bitrate = self.video_properties['bitrates'][combo[0]]
        print('for seg:{}, at buffer:{}, tputpred:{},best rate:{}, with score:{}'.format(segment_idx,buffer_level,tput_pred, best_bitrate, max_qoe))
        # print('time for looping:{}'.format(time.time() - sTime))
        return best_bitrate

    def throughput_pred(self):
        
        # basic MPC - throughput prediction from paper by harmonic mean
        
        rev_sum = 0.0
        for a in self.prev_tput_observed:
            if a != 0:
                rev_sum += (1/a)
        print('observed:{}'.format(self.prev_tput_observed))
        print('pred:{}'.format(self.prev_tput_pred))

        try:        
            harmonic_mean = len(self.prev_tput_observed) / rev_sum
            max_error = -1.0
            
            for i in range(len(self.prev_tput_observed)):
                max_error = max(abs(self.prev_tput_observed[i] - self.prev_tput_pred[i]), max_error)
            
            # robust MPC- lower bound for tput from harmonic mean
            next_tput = harmonic_mean / (1 + max_error)

        except ZeroDivisionError:
            next_tput = 214.0

        self.prev_tput_pred.append(next_tput)

        if len(self.prev_tput_pred) > keep_past_segment:
            self.prev_tput_pred.popleft()

        return next_tput

