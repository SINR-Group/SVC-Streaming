# this file creates folders for each video and 
# put required Iframes Codes, Pframe Codes, and flows in 
# respective folders

import os
import _pickle as pickle
import numpy as np
from PIL import Image 
import glob

import logger
import argparse
logger = logger.logger("Packager")

################################ video packager config start ################################
iCodePath = 'rawVideoData/icodes'
# as present in above path
iCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'

pCodePath = 'rawVideoData/pcodes/output_$trackNum$/codes'
# as present in above path
pCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'

pFlowsPath = 'rawVideoData/pflows'

# as present in above path
pFlowsFileNameFormat = ['video_$videoName$_cif_$frameNum$_after_flow_x_0001.jpg', 
						'video_$videoName$_cif_$frameNum$_after_flow_y_0001.jpg',
						'video_$videoName$_cif_$frameNum$_before_flow_x_0001.jpg',
						'video_$videoName$_cif_$frameNum$_before_flow_y_0001.jpg']

# videoNames = ['all']
videoNames = ['all', 'aris']

saveToPath = './static' 

videoFramePcodeNameFormat = 'video_t_$trackNum$_f_$frameNum$.p'
videoFrameIcodeNameFormat = 'video_f_$frameNum$.p'
videoFrameFlowsNameFormat = 'video_f_$frameNum$.p'

replicateFactor = 5

totalFrames = 97
iCodeFrequency = 12
iCodeCount = 9
pCodeCount = 88

totalTracks = 10
################################ video packager config end ##################################

################################# Assumptions ################################## 
# Frames start from number 1.
# 
# After pickling file extension should be .p and before .p 4 characters will be segment number.
# otherwise replicate function will break.
# 
################################# Assumptions ################################## 


class packager:

	def __init__(self,args):
		self.args = args
		logger.info('')
		logger.info('packaging video:{}'.format(self.args.vidName))

	def replicateIcodes(self, factor):

		iframeFnames = glob.glob(os.path.join(saveToPath, self.args.vidName, 'icodes/*.p'))
		framePresentInFolder = len(iframeFnames)

		if framePresentInFolder % iCodeCount != 0:
			logger.error(f'Icodes in folder not in multiple of {pCodeCount}')
			return False
		logger.info('Total number of frames already in [{}] video folder:{}'.format(self.args.vidName, framePresentInFolder))
		
		if framePresentInFolder >= 90:
			logger.info('Way too many frames already present. Use them only. Returning')
			return False

		incrementCounter = (framePresentInFolder//iCodeCount) * totalFrames
		
		for sfn in iframeFnames:
			currFrameNum = int(sfn[-6:-2]) + incrementCounter
			
			for i in range(1, factor):
				os.system('cp ' + sfn + ' ' + sfn[:-6] + str(currFrameNum).zfill(4)+'.p')
				currFrameNum += incrementCounter

		return True

	def replicatePcodes(self, factor):
		pframesFname = glob.glob(os.path.join(saveToPath, self.args.vidName, 'pcodes/*.p'))
		
		framePresentInFolder = len(pframesFname)
		if framePresentInFolder % (pCodeCount * totalTracks) != 0:
			logger.error(f'pcodes in folder not in multiple of {pCodeCount}')
			return False

		incrementCounter = (framePresentInFolder//(pCodeCount * totalTracks)) * totalFrames
		for sfn in pframesFname:
			currFrameNum = int(sfn[-6:-2]) + incrementCounter
			for i in range(1, factor):
				os.system('cp ' + sfn + ' ' + sfn[:-6] + str(currFrameNum).zfill(4)+'.p')
				currFrameNum += incrementCounter
		
		return True
		
	def replicateFlows(self, factor):
		flowsFname = glob.glob(os.path.join(saveToPath, self.args.vidName, 'flows/*.p'))
		
		framePresentInFolder = len(flowsFname)
		if framePresentInFolder % pCodeCount != 0:
			logger.error(f'flows in folder not in multiple of {pCodeCount}')
			return False
	
		incrementCounter = (framePresentInFolder//pCodeCount ) * totalFrames
		for sfn in flowsFname:
			currFrameNum = int(sfn[-6:-2]) + incrementCounter
			for i in range(1, factor):
				os.system('cp ' + sfn + ' ' + sfn[:-6] + str(currFrameNum).zfill(4)+'.p')
				currFrameNum += incrementCounter
		
		return True

	def replicate(self, factor = 2):
		if factor <= 1:
			return
		if not self.replicateIcodes(factor):
			return
		if not self.replicatePcodes(factor):
			return	
		if not self.replicateFlows(factor):
			return

		
	def isIcodeFrame(self, frameNum):
			# print(frameNum)
		if (frameNum - 1) % iCodeFrequency == 0:
			return True
		return False

	def packPcodesForTrack(self, trackNum):

		for currFrameNumber in range(1, totalFrames+1):
			if self.isIcodeFrame(currFrameNumber):
				continue
			pCodesObj = []
			# pCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'
			pcFile = pCodeFileNameFormat \
					.replace('$videoName$',self.args.vidName) \
					.replace('$frameNum$', str(currFrameNumber).zfill(4))
			
			# logger.info('Pcode file name:{}'.format(pcFile))

			pcTrackPath = pCodePath.replace('$trackNum$', str(trackNum))
			with open(os.path.join(pcTrackPath, pcFile), 'rb') as f:
				pCodesObj.append(f.read())
		
			pCodePckFile = os.path.join(saveToPath,self.args.vidName, 'pcodes', videoFramePcodeNameFormat)
			pCodePckFile = pCodePckFile \
							.replace('$frameNum$', str(currFrameNumber).zfill(4)) \
							.replace('$trackNum$',str(trackNum).zfill(4))

			# logger.info('pCodePckFile Name:{}'.format(pCodePckFile))	
			with open(pCodePckFile, 'wb') as f:
				pickle.dump(pCodesObj, f)


	def packPcodes(self):		
		for t in range(1, totalTracks+1):
			self.packPcodesForTrack(t)

	def packFlows(self):

		for currFrameNumber in range(1, totalFrames+1):
			if self.isIcodeFrame(currFrameNumber):
				continue
			pflowsObj = []

			# pFlowsFileNameFormat = ['video_$videoName$_cif_$frameNum$_after_flow_x_0001.jpg', 
			for flowFileNameFormat in pFlowsFileNameFormat:
				flFile = flowFileNameFormat \
							.replace('$videoName$', self.args.vidName) \
							.replace('$frameNum$', str(currFrameNumber).zfill(4))
				
				# logger.info('Flow file Name:{}'.format(flFile))
				with open(os.path.join(pFlowsPath, flFile), 'rb') as f:
					pflowsObj.append(f.read())
					
			# videoFrameFlowsNameFormat = 'video_f_$frameNum$'
			pCodePckFile = os.path.join(saveToPath,self.args.vidName, 'flows', videoFrameFlowsNameFormat)
			pCodePckFile = pCodePckFile \
							.replace('$frameNum$', str(currFrameNumber).zfill(4))
			# logger.info('pFlowsPckFile Name:{}'.format(pCodePckFile))	
			with open(pCodePckFile, 'wb') as f:
				pickle.dump(pflowsObj, f)
		
	def packIcodes(self):

		currIframe = 1
		for currIframe in range(1, totalFrames+1, iCodeFrequency):

			iCodesObj = []

			# iCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'
			icFile = iCodeFileNameFormat \
				.replace('$videoName$',self.args.vidName) \
				.replace('$frameNum$',str(currIframe).zfill(4))

			# logger.info('Icode file name:{}'.format(icFile))

			with open(iCodePath+ '/' +icFile, 'rb') as f:
				iCodesObj.append(f.read())

			# videoFrameIcodeNameFormat = 'video_f_$frameNum$.p'
			iCodePckFile = os.path.join(saveToPath, self.args.vidName , 'icodes', videoFrameIcodeNameFormat)
			iCodePckFile = iCodePckFile.replace('$frameNum$', str(currIframe).zfill(4))
			# logger.info('iCodePckFile Name:{}'.format(iCodePckFile))

			with open(iCodePckFile, 'wb') as f:
				pickle.dump(iCodesObj, f)

			# videoSegmentIcodeNameFormat = 'video_$segmentNum$.pickle$'

	def createFolders(self):
		videoName = self.args.vidName

		p = os.path.join(saveToPath, videoName, 'pcodes')
		i = os.path.join(saveToPath, videoName, 'icodes')
		f = os.path.join(saveToPath, videoName, 'flows')

		if not os.path.isdir(p):
			logger.info(f'creating dir {p}')
			os.makedirs(p)
		if not os.path.isdir(i):
			logger.info(f'creating dir {i}')
			os.makedirs(i)
		if not os.path.isdir(f):
			logger.info(f'creating dir {f}')
			os.makedirs(f)
	
parser = argparse.ArgumentParser(description="Packager")
args = parser.parse_args()

for vN in videoNames:
	args.vidName = vN
	pc = packager(args)
	pc.createFolders()
	pc.packIcodes()
	pc.packPcodes()
	pc.packFlows()
	pc.replicate(replicateFactor)







