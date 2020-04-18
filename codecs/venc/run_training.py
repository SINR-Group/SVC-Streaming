import os

iters = [i for i in range(8, 11)]
for itr in iters:
    modeldir = 'h1/model_iters_'+str(itr)
    os.system('bash ./train.sh 1 '+modeldir+' '+str(itr))

iters = [i for i in range(1, 11)]
for itr in iters:
    modeldir = 'h0/model_iters_'+str(itr)
    os.system('bash ./train.sh 0 '+modeldir+' '+str(itr))
