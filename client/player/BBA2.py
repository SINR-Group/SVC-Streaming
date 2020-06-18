from abr import abr

# calculated from zip files, for each bitrate, from 1 to 5. in kBs
file_sizes = [112.22, 256.50, 577.10, 801.49, 1234.25]


class BBA2(abr):

	def __init__(self, manifestData):
		super(BBA2, self).__init__(video_properties, args)
		self.reservoir = 8
		self.cushion = 46
		self.ratePrev = 0
		self.chunksizeMin = min(file_sizes)
		self.chunksizeMax = max(file_sizes)
		self.k = 0

		# self.buffer = 0
	

	def getNextBitrate(self, playerStats):
		# implements BBA2 algorithm from paper

		currBuffer = playerStats["currBuffer"]

		bitrates = self.getBitrateList()
		bitrates = sorted(bitrates)
		rateMap = {}

		step = self.cushion / (len(bitrates) - 1)

		for i in range(len(bitrates)):
			rateMap[self.reservoir + i * step] = bitrates[i]
		
		rMax = bitrates[-1]
		rMin = bitrates[0]

		ratePlus = None
		rateMinus = None

		if self.ratePrev < rMin:
			self.ratePrev = rMin
		
		if self.ratePrev == rMax:
			ratePlus = rMax
		else:
			for i in range(len(bitrates)):
				if bitrates[i] > self.ratePrev:
					ratePlus = bitrates[i]
					break
		
		if self.ratePrev == rMin:
			rateMinus = rMin
		else:
			for i in range(len(bitrates) - 1, -1, -1):
				if bitrates[i] < self.ratePrev:
					rateMinus = bitrates[i]
					break
		
		funCurrBuffer = self.fCurrBuffer(currBuffer, step, rateMap)

		rateNext = None

		if currBuffer <= self.reservoir:
			rateNext = rMin
		elif currBuffer >= self.reservoir + self.cushion:
			rateNext = rMax
		elif funCurrBuffer >= ratePlus:
			for i in range(len(bitrates) - 1 , -1 , -1):
				if bitrates[i] < funCurrBuffer:
					rateNext = bitrates[i]
					break
		elif funCurrBuffer <= rateMinus:
			for i in range(len(bitrates)):
				if bitrates[i] > funCurrBuffer:
					rateNext = bitrates[i]
					break
		else:
			rateNext = self.ratePrev
		
		self.ratePrev = rateNext

		return rateNext
		# return self.getCorrespondingRepId(rateNext)


	def fCurrBuffer(self,currBuffer):

		if currBuffer < self.reservoir:
			return self.chunksizeMin
		elif(currBuffer > self.reservoir + self.cushion):
			return self.chunksizeMax
		else:
			return (currBuffer - self.reservoir) * k + self.chunksizeMin

	