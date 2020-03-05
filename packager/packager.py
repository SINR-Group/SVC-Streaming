import os
import glob
import numpy as np
from zipfile import ZipFile

# Packager packs the the series of frames to segments i.e., chunks and converts them in DASH format.
class Packager:

    def __init__(self, path):
        self.tracks = 5
        self.videos = 1
        self.segments = 300
        self.path = path
        self.gop = 8

    def replicateSegments(self):
        for v in range(1, self.videos+1):
            npath = self.path+'video'+str(v)
            fs = glob.glob(npath+'/*.zip')
            for f in fs:
                for i in range(self.segments):
                    os.system('cp '+f+' '+f[:-5]+str(i)+'.zip')

    # Pack a group of frames as one segment
    def packFrames(self):
        for v in range(1, self.videos+1):
            npath = self.path+'video'+str(v)
            fs = os.listdir(npath+'/codes')
            fs = sorted(fs)
            for i in range(0, len(fs), self.gop):
                if (i+self.gop) > len(fs):
                    break
                zipper = ZipFile(npath+'/code_track4_'+str(i)+'.zip', 'w')
                for j in range(self.gop):
                    zipper.write(npath+'/codes/'+fs[i+j])
                    zipper.write(npath+'/codes/'+fs[i+j])
                zipper.close()

    # Arrange the segments in the dash format
    def formatSegments(self):
        for v in range(1, self.videos+1):
            npath = self.path+'video'+str(v)
            spath = './video_server/static/'
            for track in range(1, self.tracks+1):
                for seg in range(self.segments):
                    dash_path = 'video_'+str(track)+'_dash'+str(seg)+'.zip'
                    code = npath+'/code_track'+str(track)+'_'+str(seg)+'.zip'
                    os.system('cp '+code+' '+spath+'video'+str(v)+'/'+dash_path)

path = '/home/mallesh/coding/svc/encoder/videos/'
packager = Packager(path)
#packager.packFrames()
#packager.replicateSegments()
packager.formatSegments()
