import os, sys
import importlib.util

import numpy as np
import torch
from torch.autograd import Variable
# TODO: read from arguments instead of memory (discuss how tf this is possible)

# import specific files as modules
# change to relative paths later
# fix directory structure later as well after it is working
root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root)
# vcodec_path = '/home/nfv/aniket/SVC-Streaming/codecs/vcodec'
# icodec_path = '/home/nfv/aniket/SVC-Streaming/codecs/icodec'

# idecoder_path = os.path.join(icodec_path, 'decoder.py')

# util_path = os.path.join(root, 'util.py')
# dataset_path = os.path.join(root, 'dataset.py')
# network_path = os.path.join(root, 'network.py')
# unet_path = os.path.join(root, 'unet.py')

# vcii imports
import sys
import util
import dataset
import network
import unet
sys.path.remove(root)
# def path_import(absolute_path):
#    '''implementation taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly'''
#    spec = importlib.util.spec_from_file_location(absolute_path, absolute_path)
#    module = importlib.util.module_from_spec(spec)
#    spec.loader.exec_module(module)
#    return module

# # idecoder = path_import(idecoder_path)

# util = path_import(util_path)
# dataset = path_import(dataset_path)
# network = path_import(network_path)
# unet = path_import(unet_path)

# read context frame npz's from file

# decode npz's using image decoder
# save images to dict

# iterate through heirarchies

# read video npz
# decode npz with flows
# store decoded image to dict

# use existing function just pad the batch with one of the frames
currentfolder = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = "/home/nfv/aniket/SVC-Streaming/vtl_data"
OUTPUT_PATH = ROOT_PATH + "/images/decoded"
CODES_PATH = ROOT_PATH + "/codes/codes"
MV_PATH = ROOT_PATH + "/images/flows"
MODEL_PATH = currentfolder + "/model"
IN_DIR = ROOT_PATH +"/images/"


decode_order = [[7], [4,10],[2,3,5,6,8,9,11,12]]
# decode_order = [[7], [4,10]]
# decode_order = [[7]]

################################   init     #####################################

def decoder_init(model_path=MODEL_PATH, output_path=OUTPUT_PATH):
    """
    initializes models and frames

    args:
    from_file(bool) - flag decides whether code is read from argument or from file

    returns:
    models in heirarchical order

    """
    models = []
    argslist = []

    for heirarchy, _ in enumerate(decode_order):
        argslist.append(Args(heirarchy, output_path))
        models.append(read_models_from_file(model_path, heirarchy, argslist[heirarchy]))

    return models, argslist


def read_models_from_file(model_path, heirarchy, args):
    """
    initializes models and reads them from file
    """
    encoder, binarizer, decoder, unet = util.get_models(
        args=args, v_compress=args.v_compress, 
        bits=args.bits,
        encoder_fuse_level=args.encoder_fuse_level,
        decoder_fuse_level=args.decoder_fuse_level)

    d2 = network.DecoderCell2(v_compress=args.v_compress, shrink=args.shrink,bits=args.bits,fuse_level=args.decoder_fuse_level, itrs=args.iterations).cuda()
    print(d2)
    nets = [d2]
    if unet is not None:
        nets.append(unet)

    names = ['unet', 'd2']

    for net_idx, net in enumerate(nets):
        if net is not None:
            name = names[net_idx]
            checkpoint_path = '{}/{}_{}_{:08d}.pth'.format(
                model_path + "/h"+ str(heirarchy), 'demo', 
                name, 100000)

            print('Loading %s from %s...' % (name, checkpoint_path))
            net.load_state_dict(torch.load(checkpoint_path))

    return nets

class Args:
    """
    returns model parameters based on heirarchy
    this only exists as a workaround so we can import existing code
    """
    def __init__(self, heirarchy, output_path):    

        self.v_compress = True
        self.stack = True
        self.warp = True
        self.fuse_encoder = True
        self.shrink = 2
        self.iterations = 5
        self.batch_size = 1
        self.patch = 64
        self.num_crops = 2
        self.eval_batch_size = 1
        self.batch_size = 1

        self.in_dir = IN_DIR

        self.output_path = output_path
        self.heirarchy = heirarchy

        if heirarchy == 0:
            self.encoder_fuse_level = 1
            self.decoder_fuse_level = 1
            self.bits = 16
            self.distance1 = 6
            self.distance2 = 6

        if heirarchy == 1:
            self.encoder_fuse_level = 2
            self.decoder_fuse_level = 3
            self.bits = 16
            self.distance1 = 3
            self.distance2 = 3
        if heirarchy == 2:
            self.encoder_fuse_level = 1
            self.decoder_fuse_level = 1
            self.bits = 8
            self.distance1 = 1
            self.distance2 = 2



#####################   run decode algorithm    ################################

def decode_frames(model, codes, ctx_frames, flows):
    """
    takes codes and produces images for a particular heirarchy

    args:
    imodel(pytorch model) - vcii image decoder model
    vmodel(pytorch model) - vcii image decoder model
    codes(pytorch tensor) - hidden codes to be passed to the image decoder
    """
def read_data_from_file(argslist):

    codes_list = []
    flows_list = []
    for heirarchy, layer in enumerate(decode_order):

        args = argslist[heirarchy]

        # load batches 
        create_placeholders(heirarchy, args)
        # loader = get_batches_from_file(args)
        codes_list.append(read_codes_from_file(args))
        # print(codes_list[0])
        
        flows_list.append(get_flows_from_file(args))
        # print(type(flows_list[0]))
    
    return reverse_rearrange_list(flows_list), reverse_rearrange_list(codes_list)

def video_decode(models, flows_list, codes_list, argslist):
    """
    sends context frames (frame 1 and 13), codes and flows to decoder iteratively
    according to heirarchical compression to reconstruct all frames

    NOTE: if not reading batch from file, batch MUST be padded to have 13 channels
    TODO: fix later 
    """
    # if not __name__=="__main__":
    flows_list = rearrange_list(flows_list)
    codes_list = rearrange_list(codes_list)

    frames = []

    for heirarchy, layer in enumerate(decode_order):

        args = argslist[heirarchy]

        # load batches 
        # create_placeholders(heirarchy, args)
        # # loader = get_batches_from_file(args)
        # codes = read_codes_from_file(args)
        
        # flows_list = get_flows_from_file(args)
        batches = get_batches(args, flows_list[heirarchy])
        codes = codes_list[heirarchy]


        for idx, (flows, ctx_frames, fn) in enumerate(batches):

            code = codes[idx]


            with torch.no_grad():
                
                out_img = util.forward_decoder(models[heirarchy], code, flows, ctx_frames, args.heirarchy)

            #util.save_numpy_array_as_image(os.path.join(args.output_path,fn), out_img)
            frames.append(out_img)
    return frames


# read batches from file

def get_batches_from_file(args):
    # TODO: torch stack batch, ctx frames for better performance
    dset = dataset.ImageFolder(
        is_train=False,
        root=args.output_path,
        mv_dir=MV_PATH,
        args=args
    )
    batches = []
    for idx in range(dset.__len__()):
        batch, ctx_frames, fn = dset.__getitem__(idx)

        batch = batch[None, :, :, :]    
        ctx_frames = ctx_frames[None, :, :, :]
        with torch.no_grad():
            batch = batch.cuda()
            cooked_batch = util.prepare_batch(batch, args.v_compress, args.warp)
            _,_,_,flows = cooked_batch
        batches.append((flows, ctx_frames, fn))
    
    return batches

def get_flows_from_file(args):
    # one layer of flows
    flowslist = []
    batches = get_batches_from_file(args)
    for flows, _, _ in batches:
        flowslist.append(flows)

    return flowslist

def get_batches(args, flows):
    args.warp = False
    dset = dataset.ImageFolder(
        is_train=False,
        root=args.output_path,
        mv_dir='',
        args=args
    )
    batches = []
    assert len(flows)==dset.__len__()
    for idx in range(dset.__len__()):
        _, ctx_frames, fn = dset.__getitem__(idx)

        ctx_frames = ctx_frames[None,:,:,:]
        # print("frames")
        # print(ctx_frames.size())
        batches.append((flows[idx], ctx_frames, fn))

    return batches



def create_placeholders(heirarchy, args):
    """
    creates placeholder images to trick the dataloader
    NOTE: assumes that directory contains only images 1 and 13.
    workaround since we're using a dataloader meant for images
    """
    templatefile = os.listdir(args.output_path)[0]
    filenamepre = templatefile[:-8]
    filenamepost = templatefile[-4:]
    heirarchy_order = [[7] ,[4,10], [2,3,5,6,8,9,11,12]]

    for index in heirarchy_order[heirarchy]:
        create_single_placeholder(args.output_path, templatefile, filenamepre, filenamepost, index)

def create_single_placeholder(output_path, templatefile, filenamepre, filenamepost, index):
    """
    creates temporary placeholder image by copying templatefile

    IMAGE IS TEMPORARY AND WILL BE OVERWRITTEN BY OUTPUT OF DECODER!!!
    """
    file1 = os.path.join(output_path, templatefile)
    file2 = os.path.join(output_path, filenamepre + str(index).zfill(4) + filenamepost)
    os.system("cp " + file1 + " " + file2)


# read codes from file

def read_codes_from_file(args):
    """
    reads npz's from file
    args:
    codefile(str) - location of .npz file

    returns: code (np array)
    """
    loader = get_batches_from_file(args)
    codes = []
    for _,_, filename in loader:
        codefile = filename.split('/')[-1] + ".codes.npz"
        npfile = np.load(CODES_PATH + "/" + codefile)
        code = np.unpackbits(npfile['codes'])

        code = np.reshape(code, npfile['shape']).astype(np.float32) * 2 - 1
        code = torch.from_numpy(code)
        code = Variable(code, volatile=True)
        code = code.cuda()
        # print("codes")
        # print(codefile)
        # print(code.shape)
        codes.append(code)

    return codes
def reverse_rearrange_list(input_list):
    output_list = []
    # reverse_order = [
    #     (1,0),
    #     (0,0),
    #     (1,1)
    # ]
    reverse_order = [
        (2,0),
        (2,1),
        (1,0),
        (2,2),
        (2,3),
        (0,0),
        (2,4),
        (2,5),
        (1,1),
        (2,6),
        (2,7)
    ]
    output_list.append('Filler')
    for idx1, idx2 in reverse_order:
        try:
            output_list.append(input_list[idx1][idx2])
        except:
            output_list.append('Filler')
    output_list.append('Filler')

    return output_list
            
def rearrange_list(input_list):
    out_list = []
    # print(len(input_list))
    for layer in decode_order:
        temp_list = []
        for idx in layer:
            temp_list.append(input_list[idx-1])
        out_list.append(temp_list)
    
    return out_list

######################## main loop (for testing)    ################################

if __name__ == "__main__":

    models, argslist = decoder_init()
    flows_list, codes_list = read_data_from_file(argslist)
    video_decode(models, flows_list, codes_list, argslist)


# init 
# image decode and move to output folder
# video decode using context frames
# deinit
