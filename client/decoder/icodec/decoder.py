import os, sys
import argparse

import numpy as np
from scipy.misc import imread, imresize, imsave

import torch
from torch.autograd import Variable

# small workaround to overcome python's new import structure
root = os.path.dirname(os.path.realpath(__file__))
data_root = '/'.join(root.split('/')[:-1])
sys.path.append(root)
import inetwork
sys.path.remove(root)

MODEL_PATH = os.path.join(root,'models/decoder.pth')
OUTPUT_DIR = os.path.join(data_root, 'vtl_data/images/decoded')

def decoder_init(model=MODEL_PATH):
    decoder = inetwork.DecoderCell()
    decoder.eval()

    decoder.load_state_dict(torch.load(model))
    return decoder

def get_codes_from_file(code_folder):
    assert  os.path.exists(code_folder)
    codeslist = []
    for code_file in os.listdir(code_folder):

        content = np.load(os.path.join(code_folder, code_file))
        codes = np.unpackbits(content['codes'])
        codes = np.reshape(codes, content['shape']).astype(np.float32) * 2 - 1
        codes = torch.from_numpy(codes)
        

        codes = Variable(codes, volatile=True)
        codes = (codes)
        codeslist.append(codes)
    return codeslist

def image_decode(codes, decoder, iterations=16, cuda=True):

    # assert  os.path.exists(input_codes)
    # content = np.load(input_codes)
    # codes = np.unpackbits(content['codes'])
    # codes = np.reshape(codes, content['shape']).astype(np.float32) * 2 - 1

    # codes = torch.from_numpy(codes)
    # iters, batch_size, channels, height, width = codes.size()
    # height = height * 16
    # width = width * 16

    # codes = Variable(codes, volatile=True)

    # decoder = inetwork.DecoderCell()
    # decoder.eval()

    # decoder.load_state_dict(torch.load(model))

    iters, batch_size, channels, height, width = codes.size()
    height = height * 16
    width = width * 16
    decoder_h_1 = (Variable(
        torch.zeros(batch_size, 512, height // 16, width // 16), volatile=True),
                Variable(
                    torch.zeros(batch_size, 512, height // 16, width // 16),
                    volatile=True))
    decoder_h_2 = (Variable(
        torch.zeros(batch_size, 512, height // 8, width // 8), volatile=True),
                Variable(
                    torch.zeros(batch_size, 512, height // 8, width // 8),
                    volatile=True))
    decoder_h_3 = (Variable(
        torch.zeros(batch_size, 256, height // 4, width // 4), volatile=True),
                Variable(
                    torch.zeros(batch_size, 256, height // 4, width // 4),
                    volatile=True))
    decoder_h_4 = (Variable(
        torch.zeros(batch_size, 128, height // 2, width // 2), volatile=True),
                Variable(
                    torch.zeros(batch_size, 128, height // 2, width // 2),
                    volatile=True))

    if cuda:
        decoder = decoder.cuda()

        codes = codes.cuda()

        decoder_h_1 = (decoder_h_1[0].cuda(), decoder_h_1[1].cuda())
        decoder_h_2 = (decoder_h_2[0].cuda(), decoder_h_2[1].cuda())
        decoder_h_3 = (decoder_h_3[0].cuda(), decoder_h_3[1].cuda())
        decoder_h_4 = (decoder_h_4[0].cuda(), decoder_h_4[1].cuda())

    image = torch.zeros(1, 3, height, width) + 0.5
    for iters in range(min(iterations, codes.size(0))):

        output, decoder_h_1, decoder_h_2, decoder_h_3, decoder_h_4 = decoder(
            codes[iters], decoder_h_1, decoder_h_2, decoder_h_3, decoder_h_4)
        image = image + output.data.cpu()

    # print(codes[1])
    # print(output_folder)
    # assert(os.path.exists(output_folder))

    
    out = np.squeeze(image.numpy().clip(0, 1) * 255.0).astype(np.uint8).transpose(1, 2, 0)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default=MODEL_PATH, type=str, help='path to model')
    parser.add_argument('--input', '-i', required=True, type=str, help='input codes')
    parser.add_argument('--output', '-o', default='.', type=str, help='output folder')
    parser.add_argument('--cuda',  action='store_true', help='enables cuda')
    parser.add_argument(
        '--iterations', type=int, default=16, help='unroll iterations')
    args = parser.parse_args()

    model = args.model
    input_codes = args.input
    output_file = args.output
    cuda = args.cuda
    iterations = args.iterations


    codes = get_codes_from_file(input_codes)
    decoder = decoder_init(model)
    for code in codes:
        image_decode(code, decoder, iterations=iterations, cuda=cuda)