import os

iters = [9, 7]
for itr in iters:
    modeldir = 'h2/model_iters_'+str(itr)
    os.system('bash ./train.sh 2 '+modeldir+' '+str(itr)+' output')
