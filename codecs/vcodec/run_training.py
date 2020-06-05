import os

for itr in [9]:
    modeldir = 'h0/model_iters_'+str(itr)
    os.system('bash ./train.sh 0 '+modeldir+' '+str(itr)+' output')
