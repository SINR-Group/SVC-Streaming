from .abr import abr
		
class BBA0(abr):

	def __init__(self, video_properties, args):
		super(BBA0, self).__init__(video_properties, args)
		self.reservoir = 8
		self.cushion = 46

		self.ratePrev = 0
		# self.buffer = 0
	

	def getNextBitrate(self, playerStats):
		# implements BBA0 algorithm from paper

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
				if bitrates[i] <= funCurrBuffer:
					rateNext = bitrates[i]
					break
		elif funCurrBuffer <= rateMinus:
			for i in range(len(bitrates)):
				if bitrates[i] >= funCurrBuffer:
					rateNext = bitrates[i]
					break
		else:
			rateNext = self.ratePrev
		
		self.ratePrev = rateNext

		return rateNext


	def fCurrBuffer(self, currBuffer, step, rateMap):
		if currBuffer <= self.cushion + self.reservoir and currBuffer >= self.reservoir:
			return rateMap[round((currBuffer-self.reservoir)/step)*step + self.reservoir]

		elif currBuffer > self.cushion + self.reservoir :
			return rateMap[self.cushion + self.reservoir]

		else:
			return rateMap[self.reservoir]

