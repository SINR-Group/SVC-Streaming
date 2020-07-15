import os
import time
import sys
import downloader
import argparse
import pprint as pp
import urllib.request
import nw_filenames
import json

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


# rules = ['tputRule', 'BBA0', 'BBA2', 'Bola']
rules = ['BBA2']
nw_files = nw_filenames.logs3g


# uncomment following line if streaming with out any network trace
# nw_files=['normal_nw']

final_perf = {}
for rule in rules:
	args.abr = rule

	for nw_f in nw_files:
		args.nw = nw_f
		perf_with_nw = {}

		with urllib.request.urlopen(nw_trace_start_url + nw_f) as f:
			print(f.read())


		print("----------------------------------------------------------------")
		print(args)
		print("----------------------------------------------------------------")

		vd = downloader.client(args)

		startTime = time.time()
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

		vd.perf_param.pop('bitrate_change')
		vd.perf_param.pop('prev_rate')
		perf_with_nw[nw_f] = vd.perf_param
		# pp.pprint(vd.perf_param)

	final_perf[rule] = perf_with_nw

	with urllib.request.urlopen(nw_trace_stop_url) as f:
		print(f.read())

# change _3g or _4g accordingly for correct file name.
for rule in rules:
	with open('results_' + rule + '_3g.json', 'w') as out:
		json.dump(final_perf[rule], out, indent=4)



