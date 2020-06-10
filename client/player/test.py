import os
import time
import sys
import downloader
import argparse
import pprint as pp

# url = "http://130.245.144.152:5000/video/output.mpd"
url = "http://130.245.144.152:5000/video1/dash_tiled.mpd"
# url = "http://130.245.144.102:5000/video1/dash_tiled.mpd"

currDir = os.getcwd()

parser = argparse.ArgumentParser(description ='Search some files')

parser.add_argument("--url", dest="url", action="store", 
                        default=url, help="url of manifest file of video")
parser.add_argument("--abr", dest="abr", action="store", 
                        default="tputRule", help="ABR rule to download video" )
parser.add_argument("-b", dest="bufferSize", action="store",
                        default=60, help="Buffer size for video playback")
parser.add_argument("--gp", dest="gp", action='store', default=5,
                      help = '(gamma p) product in seconds')
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


# print("Total Play time:{}".format(endTime-startTime))

# QOE calculations
# MPC lambda and mu for balanced
lamb = 1
mu = 3000
vd.perf_param['startup_delay'] = vd.perf_param['startup_delay'] - startTime
vd.perf_param['total_play_time'] = endTime-startTime
vd.perf_param['MPC_QOE'] = vd.perf_param['avg_bitrate'] - (lamb * vd.perf_param['avg_bitrate_change']) \
                            - (mu * vd.perf_param['rebuffer_time']) - (mu * vd.perf_param['startup_delay'])

pp.pprint(vd.perf_param)

