import os
import numpy as np

itrs = [i for i in range(1, 11)]
hrch = [i for i in range(3)]

for h in hrch:
    for itr in itrs:
        command = 'bash vcodec/train.sh '+str(h)+' vcodec/h'+str(h)+'/model_iters_'+str(itr)+' '+str(itr)+' vtl_output/hrch_'+str(h)+'_itr'+str(itr)
        print (command)
