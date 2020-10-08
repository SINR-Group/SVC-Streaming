import os

for itr in [9]:
    modeldir = 'hh0/model_iters_'+str(itr)
    modeldir = 'hh1/model_iters_'+str(itr)
    modeldir = 'hh2/model_iters_'+str(itr)
    os.system('bash ./train.sh 0 '+modeldir+' '+str(itr)+' output')
    os.system('bash ./train.sh 1 '+modeldir+' '+str(itr)+' output')
    os.system('bash ./train.sh 2 '+modeldir+' '+str(itr)+' output')
