import numpy as np
import os
import time

import torch
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as LS
from torch.autograd import Variable

from dataset import get_loader
from evaluate import run_eval
from train_options import parser
from util import get_models, init_lstm, set_train, set_eval
from util import prepare_inputs, forward_ctx

import network

args = parser.parse_args()
print(args)

def get_eval_loaders():
  # We can extend this dict to evaluate on multiple datasets.
  eval_loaders = {
    'TVL': get_loader(
        is_train=False,
        root=args.eval, mv_dir=args.eval_mv,
        args=args),
  }
  return eval_loaders



############### Model ###############
encoder, binarizer, decoder, unet = get_models(
  args=args, v_compress=args.v_compress, 
  bits=args.bits,
  encoder_fuse_level=args.encoder_fuse_level,
  decoder_fuse_level=args.decoder_fuse_level)

d2 = network.DecoderCell2(v_compress=args.v_compress, shrink=args.shrink,bits=args.bits,fuse_level=args.decoder_fuse_level, itrs=args.iterations).cuda()

nets = [encoder, binarizer, decoder, d2]
if unet is not None:
  nets.append(unet)

print(nets)

gpus = [int(gpu) for gpu in args.gpus.split(',')]
if len(gpus) > 1:
  print("Using GPUs {}.".format(gpus))
  for net in nets:
    net = nn.DataParallel(net, device_ids=gpus)

params = [{'params': net.parameters()} for net in nets]

solver = optim.Adam(
    params,
    lr=args.lr)

milestones = [int(s) for s in args.schedule.split(',')]
scheduler = LS.MultiStepLR(solver, milestones=milestones, gamma=args.gamma)

if not os.path.exists(args.model_dir):
  print("Creating directory %s." % args.model_dir)
  os.makedirs(args.model_dir)

############### Checkpoints ###############
def resume(model_name, index):
  names = ['encoder', 'binarizer', 'decoder', 'unet', 'd2']

  for net_idx, net in enumerate(nets):
    if net is not None:
      name = names[net_idx]
      checkpoint_path = '{}/{}_{}_{:08d}.pth'.format(
          args.model_dir, model_name, 
          name, index)

      print('Loading %s from %s...' % (name, checkpoint_path))
      net.load_state_dict(torch.load(checkpoint_path))


train_iter = 0
just_resumed = False
if args.load_model_name:
    print('Loading %s@iter %d' % (args.load_model_name,
                                  args.load_iter))

    resume(args.load_model_name, args.load_iter)
    train_iter = args.load_iter
    scheduler.last_epoch = train_iter - 1
    just_resumed = True


set_eval(nets)

eval_loaders = get_eval_loaders()
for eval_name, eval_loader in eval_loaders.items():
    eval_begin = time.time()
    eval_loss, mssim, psnr = run_eval(nets, eval_loader, args,
        output_suffix='iter%d' % train_iter)

    print('Evaluation @iter %d done in %d secs' % (
        train_iter, time.time() - eval_begin))
    print('%s Loss   : ' % eval_name
          + '\t'.join(['%.5f' % el for el in eval_loss.tolist()]))
    print('%s MS-SSIM: ' % eval_name
          + '\t'.join(['%.5f' % el for el in mssim.tolist()]))
    print('%s PSNR   : ' % eval_name
          + '\t'.join(['%.5f' % el for el in psnr.tolist()]))

set_train(nets)
