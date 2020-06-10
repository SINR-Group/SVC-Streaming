
import urllib.request
import mpdparser
import os
import math
import time
import sys
import threading
from BBA0 import BBA0
from Bola import Bola
from abr import abr 
from queue import Queue

def downloadFile(url):
	data = None
	try:
		with urllib.request.urlopen(url) as f:
			data = f.read()
	
	except urllib.error.URLError as err:
		print("Error {} for {}".format(err,url))
	return data

def saveFile(dest, fileName, data):
	if data is None:
		print("Data is none..!! for {}".format(fileName))
	# print("dest:[{}], filename:[{}]".format(dest,fileName))
	with open(os.path.join(dest, fileName), 'wb') as f:
		f.write(data)

def extractCodes(segment):
	# extract codes and flows from zip file.
	# TODO: add extraction code
	print("extracting codes from zip file:[{}]".format(segment))

	return segment


class client:
	def __init__(self, args):
		self.args = args
		baseUrl, filename = os.path.split(args.url)
		
		print(baseUrl)

		self.baseUrl = baseUrl
		self.filename = filename.split(".")[0]

		# TODO: saving downloaded files is not required. Remove it.
		self.destination = os.path.join(args.downloadLoc + "/" + self.filename)
		try:
			os.mkdir(self.destination)
		except OSError as err:
			print(err)


		mpdContent = downloadFile(args.url)
		# saveFile(self.destination, os.path.split(args.url)[1], mpdContent)

		self.currentSegment = 0
		self.manifestData = mpdparser.ManifestParser(mpdContent)
		self.lastDownloadSize = self.lastDownloadTime = -1

		self.totalSegments = self.getTotalSegments()
		
		self.lock = threading.Lock() # this lock is primarily for current buffer level.

		self.totalBuffer = args.bufferSize #buffer time in seconds
		self.currBuffer = 0

		self.segmentQueue = Queue(maxsize=0)
		self.frameQueue = Queue(maxsize=0)

		if args.abr == "BBA0":
			self.abr = BBA0(self.manifestData)
		elif args.abr == 'Bola':
			self.abr = Bola(self.manifestData, args)
		else:
			self.abr = abr(self.manifestData)

		self.perf_param = {}
		self.perf_param['bitrate_change'] = []
		self.perf_param['prev_rate'] = 0
		self.perf_param['change_count'] = 0
		self.perf_param['rebuffer_time'] = 0.0
		self.perf_param['avg_bitrate'] = 0.0
		self.perf_param['avg_bitrate_change'] = 0.0



	def getDuration(self):
		# return total duration from manifest file

		dur = self.manifestData.mpd.periods[0].duration
		print("media duration:{}".format(dur))
		return dur
	
	def getTotalSegments(self):
		# calculates total number of video segments from manifest file

		ret = 0.0
		rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]

		ret = math.ceil((1.0 * self.getDuration() * rep.timescale) / rep.duration)
		print("totalSegments:[{}], rep ID [{}], rep timeScale [{}] rep duration [{}]".format(ret, rep.id, 
				rep.timescale, rep.duration))

		return ret


	
	def fetchNextSegment(self, bitrate = 0):
		# downloads next required segment from server with repId representation ID 
		# and return true if successfully downloaded

		if not bitrate:
			return
		adp_set = self.manifestData.mpd.periods[0].adaptation_sets[0]

		fName = None
		segmentDuration = 0

		for rep in adp_set.representations:
			# print("rep id {} {}, received parameter {} {}".format(rep.bandwidth,type(rep.bandwidth), bitrate, type(bitrate)))
			if rep.bandwidth == bitrate:
				fName = rep.media.replace("$Number$",str(self.currentSegment + 1))
				print("fName:{}".format(fName))
				segmentDuration = rep.duration / rep.timescale
				break
				

		startTime = time.time()
		data = downloadFile(self.baseUrl + "/" + fName)
		endTime = time.time()

		if data is not None:
			self.lastDownloadTime = endTime - startTime
			self.lastDownloadSize = sys.getsizeof(data)
			
			self.segmentQueue.put(fName)
			print("Downloaded segment:[{}]".format(fName))

			# saveFile(self.destination, fName, data)
			
			# QOE parameters update 
			self.perf_param['bitrate_change'].append((self.currentSegment + 1,  bitrate))
			self.perf_param['avg_bitrate'] += bitrate
			self.perf_param['avg_bitrate_change'] += abs(bitrate - self.perf_param['prev_rate'])

			if not self.perf_param['prev_rate'] or self.perf_param['prev_rate'] != bitrate:
				self.perf_param['prev_rate'] = bitrate
				self.perf_param['change_count'] += 1
			
			self.currentSegment += 1

			with self.lock:
					self.currBuffer += segmentDuration
			
			ret = True
		else:
			print("Error: downloaded segment is none!! Playback will stop shortly")
			ret = False
		
		return ret
		
	
	def lastSegmentThroughput(self):
		# returns throughput value of last segment downloaded in bits/seconds

		if self.currentSegment == 0:
			return 0

		return (self.lastDownloadSize * 8.0 ) / self.lastDownloadTime

	def getCorrespondingRepId(self, bitrate):
		adpSet = self.manifestData.mpd.periods[0].adaptation_sets[0]
		
		for rep in adpSet.representations:
			if int(rep.bandwidth) == bitrate:
				return rep.id
		
		return -1 #states no representation with given bitrate found

	def segmentDownloadThread(self):
		# thread to continuously downloads next segment based on selected abr rule.

		while self.currentSegment < self.totalSegments:
			with self.lock:
				currBuff = self.currBuffer
			
			rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]
			segmentDuration = rep.duration / rep.timescale

			playerStats = {}
			playerStats["lastTput"] = self.lastSegmentThroughput()
			playerStats["currBuffer"] = currBuff
			# playerStats['empty_buffer_size'] = self.args.bufferSize - currBuff

			if self.totalBuffer - currBuff >= segmentDuration:
				rateNext = self.abr.getNextBitrate(playerStats)
				# print("fetching segment number [{}] from representation [{}]".format(self.currentSegment+1, rateNext))
				if not self.fetchNextSegment(rateNext):
					break
			else:
				time.sleep(0.5)
		
		self.segmentQueue.put("done")


	def playThread(self):
		# thread to play decoded frames received from decoder
		
		# this flag is to mark start of play back.
		playback_started = False
		while True:

			rebuff_start = time.time()
			frame = self.frameQueue.get()
			rebuff_end = time.time()

			if frame == "done":
				print("played all frames")
				break
			
			if not playback_started:
				playback_started = True
				self.perf_param['startup_delay'] = time.time()
			else:
				self.perf_param['rebuffer_time'] += (rebuff_end - rebuff_start)

			time.sleep(2)
			with self.lock:
				self.currBuffer -= 2
			
			print("Played segment:[{}]".format(frame))


	def decodeThread(self):
		# thread to call decoder on segments waiting in queue

		while True:
			segment = self.segmentQueue.get()
			if segment == "done":
				print("All segments downloaded")
				self.frameQueue.put(segment)
				break

			frames = decode(extractCodes(segment))
			print("Decoded segment:{}".format(frames))
			self.frameQueue.put(frames)

	def play(self):
		# function to start 3 threads, downloading, decoding and playing

		downt = threading.Thread(target=self.segmentDownloadThread )
		downt.start()
		dect = threading.Thread(target=self.decodeThread)
		dect.start()

		pt = threading.Thread(target=self.playThread)
		pt.start()

		downt.join()
		dect.join()
		pt.join()

		self.perf_param['avg_bitrate'] /= self.totalSegments
		self.perf_param['avg_bitrate_change'] /= (self.totalSegments - 1)



def decode(a):
	# dummy function
	time.sleep(0.5)
	return a