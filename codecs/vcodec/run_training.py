import os

iters = [10, 4, 6, 7, 8, 9]
for itr in iters:
    if itr != 10:
        modeldir = 'h0/model_iters_'+str(itr)
        os.system('bash ./train.sh 0 '+modeldir+' '+str(itr)+' output')

        modeldir = 'h1/model_iters_'+str(itr)
        os.system('bash ./train.sh 1 '+modeldir+' '+str(itr)+' output')

    modeldir = 'h2/model_iters_'+str(itr)
    os.system('bash ./train.sh 2 '+modeldir+' '+str(itr)+' output')
