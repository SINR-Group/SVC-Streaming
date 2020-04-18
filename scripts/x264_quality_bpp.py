import os
import numpy as np

idir = 'yuvs/'
odir = 'compressed/'

def encodeRawVideos(fs):
    for f in fs:
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 400k -an '+odir+f[:-4]+'_compressed_1.mp4')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 1000k -minrate 1000k -maxrate 1000k -bufsize 200k -an '+odir+f[:-4]+'_compressed_2.mp4')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 500k -minrate 500k -maxrate 500k -bufsize 100k -an '+odir+f[:-4]+'_compressed_3.mp4')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 200k -minrate 200k -maxrate 200k -bufsize 50k -an '+odir+f[:-4]+'_compressed_4.mp4')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 100k -minrate 100k -maxrate 100k -bufsize 20k -an '+odir+f[:-4]+'_compressed_5.mp4')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -b:v 50k -minrate 50k -maxrate 50k -bufsize 10k -an '+odir+f[:-4]+'_compressed_6.mp4')

def vqa(fs):
    for f in fs:
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_1.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_1.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_1.log\" -f null -')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_2.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_2.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_2.log\" -f null -')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_3.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_3.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_3.log\" -f null -')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_4.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_4.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_4.log\" -f null -')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_5.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_5.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_5.log\" -f null -')
        os.system('ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 352x288 -r 30 -i '+idir+f+' -i '+odir+f[:-4]+'_compressed_6.mp4 -lavfi \"ssim=log/ssim_'+f[:-4]+'_6.log;[0:v][1:v]psnr=log/psnr_'+f[:-4]+'_6.log\" -f null -')

def computeAverage(fs, b, k):
    psnr = []
    ssim = []
    for f in fs:
        lines = open('log/psnr_'+f[:-4]+'_'+str(b)+'.log', 'r')
        for line in lines:
            q = line.strip().split(' ')[5].split(':')[1]
            psnr.append(float(q))
        lines = open('log/ssim_'+f[:-4]+'_'+str(b)+'.log', 'r')
        for line in lines:
            q = line.strip().split(' ')[4].split(':')[1]
            ssim.append(float(q))
    print 'bpp: '+str(k*1000/352/288.0), 'PSNR: '+str(np.mean(psnr)), 'MSSSIM: '+str(np.mean(ssim))

fs = os.listdir(idir)

#encodeRawVideos(fs)
#vqa(fs)
computeAverage(fs, 1, 2000)
computeAverage(fs, 2, 1000)
computeAverage(fs, 3, 500)
computeAverage(fs, 4, 200)
computeAverage(fs, 5, 100)
computeAverage(fs, 6, 50)
