import os
import time
import sys
import downloader
import argparse
import pprint as pp
import urllib.request
import nw_filenames
import json
import argparse
import meta

parser = argparse.ArgumentParser(description = 'Search some files')

parser.add_argument("--url", dest="url", action="store", 
						default= meta.base_url + meta.manifest_path, help="url of manifest file of video")
parser.add_argument("--abr", dest="abr", action="store", 
						default="tputRule", help="ABR rule to download video" )
parser.add_argument("-b", dest="bufferSize", action="store",
						default=60, help="Buffer size for video playback")
parser.add_argument("--gp", dest="gp", action='store', default=5,
					  help = '(gamma p) product in seconds')


args = parser.parse_args()
args.lastSeg = meta.lastSeg

final_perf = {}
for rule in meta.rules:
	args.abr = rule
	perf_with_nw = {}

	for nw_f in meta.nw_files:
		args.nw = nw_f
		with urllib.request.urlopen(meta.nw_trace_start_url + nw_f) as f:
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

		# vd.perf_param.pop('bitrate_change')
		vd.perf_param.pop('prev_rate')
		perf_with_nw[nw_f] = vd.perf_param
		# pp.pprint(vd.perf_param)

		with urllib.request.urlopen(meta.nw_trace_stop_url) as f:
			print(f.read())

	final_perf[rule] = perf_with_nw


for rule in meta.rules:
	with open(meta.resultFileName + rule + '.json', 'w') as out:
		json.dump(final_perf[rule], out, indent=4)



