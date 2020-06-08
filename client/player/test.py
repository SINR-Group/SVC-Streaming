import os
import time
import sys
import downloader
import argparse

#url = "http://130.245.144.152:5000/video/output.mpd"
url = "http://130.245.144.102:5000/video1/dash_tiled.mpd"
currDir = os.getcwd()

parser = argparse.ArgumentParser(description ='Search some files')

parser.add_argument("--url", dest="url", action="store", 
                        default=url, help="url of manifest file of video")
parser.add_argument("--abr", dest="abr", action="store", 
                        default="tputRule", help="ABR rule to download video" )
parser.add_argument("-b", dest="bufferSize", action="store",
                        default=60, help="Buffer size for video playback")

parser.add_argument("--loc", dest="downloadLoc", action="store", 
                        default=currDir, help="location to save downloaded files")
# TODO: this argument will be removed

args = parser.parse_args()
print("----------------------------------------------------------------")
print(args)
print("----------------------------------------------------------------")


startTime = time.time()
vd = downloader.client(args)
vd.play()
endTime = time.time()

print("Total Play time:{}".format(endTime-startTime))
