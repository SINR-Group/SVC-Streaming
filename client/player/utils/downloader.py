
import urllib.request
import mpdparser
import os
import math
import time
import sys
import threading
from queue import Queue

def downloadFile(url):
	data = None
	try:
		with urllib.request.urlopen(url) as f:
			# print(f.read(50))
			data = f.read()
		# print("downloaded:{}".format(url))
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
	print("extracting codes from zip file:[{}]".format(segment))

	return segment



class client:
	def __init__(self, url, dest):
		baseUrl, filename = os.path.split(url)
		print(baseUrl)
		self.baseUrl = baseUrl
		self.filename = filename.split(".")[0]
		# print(self.filename)
		self.destination = os.path.join(dest + "/" + self.filename)
		try:
			os.mkdir(self.destination)
		except OSError as err:
			print(err)


		mpdContent = downloadFile(url)
		saveFile(self.destination, os.path.split(url)[1], mpdContent)

		self.currentSegment = 0
		self.manifestData = mpdparser.ManifestParser(mpdContent)
		self.lastDownloadSize = self.lastDownloadTime = -1

		self.totalSegments = self.getTotalSegments()
		
		self.lock = threading.Lock()

		self.buffer = 60 #buffer time in seconds
		self.segmentQueue = Queue(maxsize=0)
		self.frameQueue = Queue(maxsize=0)

		self.abr = Abr(self.manifestData)



	def getDuration(self):
		dur = self.manifestData.mpd.periods[0].duration
		print("media duration:{}".format(dur))
		return dur
	
	def getTotalSegments(self):
		ret = 0.0
		rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]

		ret = math.ceil((1.0 * self.getDuration() * rep.timescale) / rep.duration)
		print("totalSegments:[{}], rep ID [{}], rep timeScale [{}] rep duration [{}]".format(ret, rep.id, 
				rep.timescale, rep.duration))

		return ret


	# downloads next required segment from server with repId representation ID 
	def fetchNextSegment(self, repId = 0):

		if not repId:
			return
		adp_set = self.manifestData.mpd.periods[0].adaptation_sets[0]

		fName = None
		segmentDuration = 0

		for rep in adp_set.representations:
			# print("rep id {} {}, received parameter {} {}".format(rep.id,type(rep.id), repId, type(repId)))
			if rep.id == repId:
				fName = rep.media.replace("$Number$",str(self.currentSegment + 1))
				# print("fname:{}".format(fName))
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

			saveFile(self.destination, fName, data)

			self.currentSegment += 1

			with self.lock:
					self.buffer -= segmentDuration
		


	# returns throuhput value of last segement downloaded in bits/seconds
	def lastSegmentThroughput(self):
		if self.currentSegment == 0:
			return 0

		return (self.lastDownloadSize * 8.0 ) / self.lastDownloadTime


	def segmentDownloadThread(self):

		while self.currentSegment < self.totalSegments:
			with self.lock:
				currBuff = self.buffer
			
			rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]
			segmentDuration = rep.duration / rep.timescale

			if currBuff >= segmentDuration:
				repId = self.abr.repIdForNextSegment(self.lastSegmentThroughput())
				print("fetching segment number [{}] from representation [{}]".format(self.currentSegment+1, repId))
				self.fetchNextSegment(repId)
			else:
				time.sleep(0.5)
		
		self.segmentQueue.put("done")


	def playThread(self):
		

		while True:
			frame = self.frameQueue.get()
			if frame == "done":
				print("played all frames")
				break
			time.sleep(2)
			with self.lock:
				self.buffer += 2
			
			print("Played segment:[{}]".format(frame))

		# currentFrame = 0
		# rep = self.manifestData.mpd.periods[0].adaptation_sets[0].representations[0]
		# segmentDuration = rep.duration / rep.timescale

		# while currentFrame < self.totalSegments:

		# 	if currentFrame <= self.currentSegment:
		# 		print("playing {} frame,".format(currentFrame+1))
		# 		time.sleep(segmentDuration)
		# 		with self.lock:
		# 			self.buffer += segmentDuration
		# 		currentFrame += 1
		# 	else:
		# 		time.sleep(1)


	def decodeThread(self):

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

		downt = threading.Thread(target=self.segmentDownloadThread )
		downt.start()
		dect = threading.Thread(target=self.decodeThread)
		dect.start()

		pt = threading.Thread(target=self.playThread)
		pt.start()

		downt.join()
		dect.join()
		pt.join()

		
class Abr:
	def __init__(self, manifestData):
		self.manifestData = manifestData
	
	# estimates representation id for next segment to be downloaded on the basis
	# throughPut(tput) of last downloaded segment
	def repIdForNextSegment(self, tput = 0):

		if not tput:
			return 1
		
		adpSet = self.manifestData.mpd.periods[0].adaptation_sets[0]

		repId = 1
		for rep in adpSet.representations:
			if rep.bandwidth > tput:
				repId = rep.id - 1
				break
			repId = rep.id
		
		if repId >= 1:
			return repId
		else:
			return 1
		


def decode(a):
	time.sleep(0.5)
	return a