import os

#iters = [i for i in range(1, 11)]
iters = [1]
for itr in iters:
    modeldir = 'h0/model_iters_'+str(itr)
    os.system('bash ./train.sh 0 '+modeldir+' '+str(itr)+' output')

    modeldir = 'h1/model_iters_'+str(itr)
    os.system('bash ./train.sh 1 '+modeldir+' '+str(itr)+' output')

    modeldir = 'h2/model_iters_'+str(itr)
    os.system('bash ./train.sh 2 '+modeldir+' '+str(itr)+' output')
