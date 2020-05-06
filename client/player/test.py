
import os
import downloader
import time

currDir = os.getcwd()
url = "http://130.245.144.102:5000/video1/dash_tiled.mpd"

startTime = time.time()
vd = downloader.client(url, currDir)
vd.play()
endTime = time.time()

print("Total Play time:{}".format(endTime-startTime))



# import urllib.request

# mpdAdr="http://130.245.144.102:5000/video1/dash_tiled.mpd"
# try:
#     with urllib.request.urlopen(mpdAdr) as f:
#         print(f.read(50))
#     # print("length of file: {} file content {}".format(len(data),data[:50]))
# except urllib.error.URLError as err:
#     print("Error {} for {}".format(err,mpdAdr))

