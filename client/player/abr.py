
# Base class for abr rules. Implements common functions and 
# basic throughput rule.

class abr:
	def __init__(self, manifestData):
		self.manifestData = manifestData
	
	# estimates representation id for next segment to be downloaded on the basis
	# throughPut(tput) of last downloaded segment
	def getNextBitrate(self, playerStats):

		tput = playerStats["lastTput"]
		
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

		# adpSet = self.manifestData.mpd.periods[0].adaptation_sets[0]

		# repId = 1
		
		# for rep in adpSet.representations:
		# 	if rep.bandwidth > tput:
		# 		repId = rep.id - 1
		# 		rateNext
		# 		break
		# 	repId = rep.id
		
		# if repId >= 1:
		# 	return repId
		# else:
		# 	return 1
	
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
