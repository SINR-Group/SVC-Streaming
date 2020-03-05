import os
import numpy as np
from zipfile import ZipFile

# Packager packs the the series of frames to segments i.e., chunks and converts them in DASH format.
class Packager:

    def __init__(self, path):
        self.tracks = 5
        self.videos = 1
        self.segments = 5
        self.path = path
        self.gop = 7

    # Pack a group of frames as one segment
    def packFrames(self):
        for v in range(1, self.videos+1):
            npath = self.path+'video'+str(v)
            fs = os.listdir(npath)
            fs = sorted(fs)
            for i in range(0, len(fs), self.gop):
                zipper = ZipFile(npath+'/code_track5_'+str(i)+'.zip', 'w')
                if i+self.gop > len(fs):
                    break
                for j in range(self.gop):
                    zipper.write(npath+'/codes/'+fs[i+j])
                zipper.close()

    # Arrange the segments in the dash format
    def formatSegments(self):
        for track in range(self.tracks):
            os.system('ls')

path = '/home/mallesh/coding/svc/encoder/videos/'
packager = Packager(path)
packager.packFrames()
packager.formatSegments()
