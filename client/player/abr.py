
# Base class for abr rules. Implements common functions and 
# basic throughput rule.

class abr:
	def __init__(self, manifestData):
		self.manifestData = manifestData
	
	# estimates representation id for next segment to be downloaded on the basis
	# throughPut(tput) of last downloaded segment
	def repIdForNextSegment(self, playerStats):

		tput = playerStats["lastTput"]

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
	
	def getBitrateList(self):
		adpSet = self.manifestData.mpd.periods[0].adaptation_sets[0]
		bitrateList = []
		for rep in adpSet.representations:
			bitrateList.append(int(rep.bandwidth))
		
		return bitrateList
	
	def getCorrespondingRepId(self, bitrate):
		adpSet = self.manifestData.mpd.periods[0].adaptation_sets[0]
		
		for rep in adpSet.representations:
			if int(rep.bandwidth) == bitrate:
				return rep.id
		
		return -1 #states no representation with given bitrate found
