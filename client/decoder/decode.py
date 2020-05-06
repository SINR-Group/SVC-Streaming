import os
import importlib.util
import sys

import numpy as np
import torch 
from torch.autograd import Variable
from scipy.misc import imread, imresize, imsave

sys.stdout = open(os.devnull, 'w')

root = os.path.dirname(os.path.realpath(__file__))

data_root = '/'.join(root.split('/'))
vdecoder_path = os.path.join(root, 'vcodec/decode.py')
idecoder_path = os.path.join(root, 'icodec/decoder.py')

def path_import(absolute_path):
   '''implementation taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly'''
   spec = importlib.util.spec_from_file_location(absolute_path, absolute_path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)
   return module

idecoder = path_import(idecoder_path)
vdecoder = path_import(vdecoder_path)


CODES_PATH = os.path.join(data_root, 'vtl_data/codes/codes')
OUTPUT_DIR = os.path.join(data_root, 'vtl_data/images/decoded')
MV_PATH = os.path.join(data_root, 'vtl_data/images/flows')

def get_codes_from_file(code_dir=CODES_PATH):
    codes = []

    for i in range(1,14):
        for filename in os.listdir(code_dir):
            # print(code_dir)
            # print(filename)
            idx = int(filename[:-14].split('_')[-1])

            if i == idx:

                npfile = np.load(os.path.join(code_dir, filename))

                code = np.unpackbits(npfile['codes'])
                code = np.reshape(code, npfile['shape']).astype(np.float32) * 2 - 1
                code = torch.from_numpy(code)
                code = Variable(code, volatile=True)
                code = code.cuda()

                codes.append(code)
    
    return codes, filename


def decoder_init(output_path):
    idecodermodel = idecoder.decoder_init()
    vdecodermodels, argslist = vdecoder.decoder_init(output_path=output_path)
    
    return idecodermodel, vdecodermodels, argslist

def video_decode(idecodermodel, vdecodermodels, codes, flows, argslist):

    filename = os.listdir(CODES_PATH)[0]

    icodes = [codes[0], codes[12]]
    images = []
    images.append(idecoder.image_decode(codes[0], idecodermodel, iterations=16, cuda=True))
    imgfile = filename[:-18] + '0001' + filename[-14:-10] 
    imsave(os.path.join(OUTPUT_DIR, imgfile), images[0])
    images.append(idecoder.image_decode(codes[12], idecodermodel, iterations=16, cuda=True))
    imgfile = filename[:-18] + '0013' + filename[-14:-10]
    imsave(os.path.join(OUTPUT_DIR, imgfile), images[1])

    # vcodes = codes[1:12]
    vdecoder.video_decode(vdecodermodels, flows, codes, argslist)
    

    return images

def decoder_deinit(model):
    """
    destructors
    """
    del model

if __name__ == "__main__":

    codes, filename= get_codes_from_file()

    idecodermodel, vdecodermodels, argslist = decoder_init(OUTPUT_DIR)
    flows, vcodes = vdecoder.read_data_from_file(argslist)

    images = video_decode(idecodermodel, vdecodermodels, codes, flows, argslist)
    decoder_deinit(idecodermodel)
    decoder_deinit(vdecodermodels)
