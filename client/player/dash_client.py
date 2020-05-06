import os
import time
import sys

currDir = os.getcwd()
url = "http://130.245.144.102:5000/video1/dash_tiled.mpd"

startTime = time.time()
vd = downloader.client(url, currDir)
vd.play()
endTime = time.time()

print("Total Play time:{}".format(endTime-startTime))
