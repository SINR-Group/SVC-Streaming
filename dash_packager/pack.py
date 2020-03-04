import os
import numpy as np

class Packager:

    def __init__(self):
        self.rates = 3
        self.videos = 1
        self.segments = 5
        self.path = '/home/mallesh/coding/svc/encoder/videos/'

    # pack a group of frames as one segment
    def packFrames(self):
        for i in range(self.segments):
            print (i)

    # arrange the segments in the dash format
    def formatSegments(self):
        for r in range(self.rates):
            os.system('ls')

packager = Packager()
packager.packFrames()
packager.formatSegments()
