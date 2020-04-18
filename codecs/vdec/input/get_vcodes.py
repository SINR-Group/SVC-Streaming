import os

for itr in range(1, 11):
    if not os.path.exists('vcodes/'+str(itr)):
        os.makedirs('vcodes/'+str(itr))
    for h in range(3):
        os.system('cp ../../venc/vtl_output/hrch_'+str(h)+'_itr'+str(itr)+'/iter20001/codes/* vcodes/'+str(itr)+'/')
