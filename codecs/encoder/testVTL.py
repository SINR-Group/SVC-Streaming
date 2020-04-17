import os
import numpy as np

itrs = [i for i in range(1, 11)]
hrch = [i for i in range(3)]

for h in hrch:
    for itr in itrs:
        if not os.path.exists('dhf1k_output/hrch_'+str(h)+'_itr'+str(itr)):
            os.makedirs('dhf1k_output/hrch_'+str(h)+'_itr'+str(itr))
        command = './train.sh '+str(h)+' h'+str(h)+'/model_iters_'+str(itr)+' '+str(itr)+' dhf1k_output/hrch_'+str(h)+'_itr'+str(itr)
        os.system('bash '+command+' > dhf1k_output/hrch_'+str(h)+'_itr'+str(itr)+'/results.txt')
