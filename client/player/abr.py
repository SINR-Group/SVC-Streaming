
# Base class for abr rules. Implements common functions and 
# basic throughput rule.

class abr:
	def __init__(self, video_properties, args):
		self.video_properties = video_properties
		self.args = args
	
	# estimates representation id for next segment to be downloaded on the basis
	# throughPut(tput) of last downloaded segment
	def getNextBitrate(self, playerStats):

		tput = playerStats["lastTput_kbps"] * 1000
		bitrateList = self.getBitrateList()
		bitrateList = sorted(bitrateList)
		rateNext = bitrateList[0]
		
		# tput will be 0 for very first segment

		if not tput:
			return rateNext

		for bt in bitrateList:
			if bt <= tput:
				rateNext = bt
			else:
				break
			
		return rateNext
	
	def getBitrateList(self):
		bitrateList = self.video_properties['bitrates']
		return bitrateList
	
	def getCorrespondingRepId(self, bitrate):

		for i,b in enumerate(self.video_properties['bitrates']):
			if b == bitrate:
				return i + 1
		
		return -1 #states no representation with given bitrate found

	def getSegmentDuration(self):
		return self.video_properties['duration'] / self.video_properties['timescale']