import os
import time
import sys
import downloader
import argparse
import pprint as pp
import urllib.request

# url = "http://130.245.144.152:5000/video/output.mpd"
# url = "http://130.245.144.152:5000/video1/dash_tiled.mpd"
url = 'http://130.245.144.152:5000/video1/video_properties.json'
nw_trace_start_url = 'http://130.245.144.152:5000/networkTrace?file='
nw_trace_stop_url ='http://130.245.144.152:5000/stopNWtrace'
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
parser.add_argument('--nw', dest='nw', action='store',
						default='report.2010-09-13_1003CEST.json', help='nw trace file to test algorithm')
# TODO: this argument will be removed

args = parser.parse_args()


rules = ['tputRule', 'BBA0', 'BBA2', 'Bola']
nw_files = ['report.2010-09-13_1003CEST.json', 'report_bus_0001.json']

final_perf = {}
for nw_f in nw_files:
	args.nw = nw_f
	perf_with_nw = {}

	with urllib.request.urlopen(nw_trace_start_url + nw_f) as f:
		print(f.read())

	# time.sleep(120)
	
	# with urllib.request.urlopen(nw_trace_stop_url) as f:
	# 	print(f.read())
	# continue

	for rule in rules:
		args.abr = rule

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

		perf_with_nw[rule] = vd.perf_param
		# pp.pprint(vd.perf_param)


	final_perf[nw_f] = perf_with_nw

	with urllib.request.urlopen(nw_trace_stop_url) as f:
		print(f.read())

print(final_perf)

