import os
import numpy as np

iters = [i for i in range(1, 11)]

opath = '/home/mallesh/deepvideo/data/vtl/test/'

def get_flows_size(rframe):
    flow_fs = []

for itr in iters:
    recframes = os.listdir('output_'+str(itr)+'/images')
    for rframe in recframes:
        oframe = opath+rframe
        size = get_flows_size(rframe) + get_code_size(rframe, 1)
        bpp = size/(get_number_of_pixels(rframe))

    irecframes = os.listdir('../../icodec/vtl/images/')
    for irframe in irecframes:
        oframe = opath+irframe
        size = get_code_size(irframe, 0)
        bpp = size/(get_number_of_pixels(rframe))
