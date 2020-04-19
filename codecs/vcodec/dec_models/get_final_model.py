import os

for h in range(3):
    if not os.path.exists('./h'+str(h)):
        os.makedirs('./h'+str(h))
    for itr in range(1, 11):
        if not os.path.exists('./h'+str(h)+'/model_iters_'+str(itr)):
            os.makedirs('./h'+str(h)+'/model_iters_'+str(itr))
        os.system('cp ../h'+str(h)+'/model_iters_'+str(itr)+'/demo_decoder_00020000.pth ./h'+str(h)+'/model_iters_'+str(itr)+'/')
