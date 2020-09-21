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
iCodePath = './icodes'
# as present in above path
iCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'

pCodePath = './pcodes/output_$trackNum$/codes'
# as present in above path
pCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'

pFlowsPath = './pflows'
# as present in above path
pFlowsFileNameFormat = ['video_$videoName$_cif_$frameNum$_after_flow_x_0001.jpg', 
						'video_$videoName$_cif_$frameNum$_after_flow_y_0001.jpg',
						'video_$videoName$_cif_$frameNum$_before_flow_x_0001.jpg',
						'video_$videoName$_cif_$frameNum$_before_flow_y_0001.jpg']

# videoNames = ['all']
videoNames = ['all', 'aris']

saveToPath = './static' 

videoSegmentPcodeNameFormat = 'video_t_$trackNum$_s_$segmentNum$.p'
videoSegmentIcodeNameFormat = 'video_s_$segmentNum$.p'

replicateFactor = 5

totalFrames = 97

framesPerSegment = 97

iCodeFrequency = 12

iCodePerSegment = 1 + (framesPerSegment - 1) // iCodeFrequency
totalSegments = totalFrames // framesPerSegment

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


	def replicate(self, factor = 2):
		if factor <= 1:
			return
		
		segmentFname = glob.glob(os.path.join(saveToPath, self.args.vidName, 'icodes/*.p'))
		segmentPresentInFolder = len(segmentFname)
		logger.info('Total number of segment already in {} video folder:{}'.format(self.args.vidName, segmentPresentInFolder))
		
		if segmentPresentInFolder >= 100:
			logger.info('Way too many segments already present. Use them only. Returning')
			return
		for sfn in segmentFname:
			currSegNum = int(sfn[-6:-2]) + segmentPresentInFolder
			for i in range(1, factor):
				os.system('cp ' + sfn + ' ' + sfn[:-6] + str(currSegNum).zfill(4)+'.p')
				currSegNum += segmentPresentInFolder

		segmentFname = glob.glob(os.path.join(saveToPath, self.args.vidName, 'pcodes/*.p'))
		
		for sfn in segmentFname:
			currSegNum = int(sfn[-6:-2]) + segmentPresentInFolder
			for i in range(1, factor):
				os.system('cp ' + sfn + ' ' + sfn[:-6] + str(currSegNum).zfill(4)+'.p')
				currSegNum += segmentPresentInFolder


	def packPcodesFlowsForTrack(self, trackNum):

		def isIcodeFrame(frameNum):
			# print(frameNum)
			if (frameNum - 1) % iCodeFrequency == 0:
				return True
			return False


		currSegmentNum = 1
		currFrame = 1

		for i in range(1, totalSegments+1):
			pCodesObj = []

			for j in range(1, framesPerSegment+1):

				pCodeFlowFrm = []
				if isIcodeFrame(currFrame):
					currFrame += 1
					continue
				
				# pCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'
				pcFile = pCodeFileNameFormat \
						.replace('$videoName$',self.args.vidName) \
						.replace('$frameNum$', str(currFrame).zfill(4))
				
				# logger.info('Pcode file name:{}'.format(pcFile))

				pcTrackPath = pCodePath.replace('$trackNum$', str(trackNum))

				with open(os.path.join(pcTrackPath, pcFile), 'rb') as f:
					pCodeFlowFrm.append(f.read())

				# pFlowsFileNameFormat = ['video_$videoName$_cif_$frameNum$_after_flow_x_0001.jpg', 
				for flowFileNameFormat in pFlowsFileNameFormat:
					flFile = flowFileNameFormat \
								.replace('$videoName$', self.args.vidName) \
								.replace('$frameNum$', str(j).zfill(4))
					
					# logger.info('Flow file Name:{}'.format(flFile))
					with open(os.path.join(pFlowsPath, flFile), 'rb') as f:
						pCodeFlowFrm.append(f.read())
				
				pCodesObj.append(pCodeFlowFrm)
				currFrame += 1
			
			pCodePckFile = os.path.join(saveToPath,self.args.vidName, 'pcodes', videoSegmentPcodeNameFormat)
			pCodePckFile = pCodePckFile \
							.replace('$segmentNum$', str(currSegmentNum).zfill(4)) \
							.replace('$trackNum$',str(trackNum).zfill(4))

			logger.info('pCodePckFile Name:{}'.format(pCodePckFile))
				
			with open(pCodePckFile, 'wb') as f:
				pickle.dump(pCodesObj, f)


	def packPcodesFlows(self):		

		for t in range(1, totalTracks+1):
			self.packPcodesFlowsForTrack(t)

	def packIcodes(self):

		currIframe = 1
		for currSegmentNum in range(1, totalSegments+1):

			iCodesObj = []

			for j in range(iCodePerSegment):
				# iCodeFileNameFormat = 'video_$videoName$_cif_$frameNum$.png.codes.npz'
				icFile = iCodeFileNameFormat \
					.replace('$videoName$',self.args.vidName) \
					.replace('$frameNum$',str(currIframe).zfill(4))

				# logger.info('Icode file name:{}'.format(icFile))

				with open(iCodePath+ '/' +icFile, 'rb') as f:
					iCodesObj.append(f.read())
				
				currIframe += iCodeFrequency

			iCodePckFile = os.path.join(saveToPath, self.args.vidName , 'icodes',videoSegmentIcodeNameFormat)
			iCodePckFile = iCodePckFile.replace('$segmentNum$', str(currSegmentNum).zfill(4))
			logger.info('iCodePckFile Name:{}'.format(iCodePckFile))

			with open(iCodePckFile, 'wb') as f:
				pickle.dump(iCodesObj, f)

			# videoSegmentIcodeNameFormat = 'video_$segmentNum$.pickle$'

	def createFolders(self):
		videoName = self.args.vidName
		p = saveToPath + '/' + videoName + '/pcodes'
		i = saveToPath + '/' + videoName + '/icodes'
		if not os.path.isdir(p):
			os.makedirs(p)
		if not os.path.isdir(i):
			os.makedirs(i)
	
parser = argparse.ArgumentParser(description="Packager")
args = parser.parse_args()

for vN in videoNames:
	args.vidName = vN
	pc = packager(args)
	pc.createFolders()
	pc.packIcodes()
	pc.packPcodesFlows()
	pc.replicate(replicateFactor)







