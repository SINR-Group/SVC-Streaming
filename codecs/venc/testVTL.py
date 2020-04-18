import os
import numpy as np

itrs = [i for i in range(1, 11)]
hrch = [i for i in range(3)]

for h in hrch:
    for itr in itrs:
        if not os.path.exists('vtl_output/hrch_'+str(h)+'_itr'+str(itr)):
            os.makedirs('vtl_output/hrch_'+str(h)+'_itr'+str(itr))
        command = './train.sh '+str(h)+' ../vcodec/h'+str(h)+'/model_iters_'+str(itr)+' '+str(itr)+' vtl_output/hrch_'+str(h)+'_itr'+str(itr)
        os.system('bash '+command+' > vtl_output/hrch_'+str(h)+'_itr'+str(itr)+'/results.txt')
