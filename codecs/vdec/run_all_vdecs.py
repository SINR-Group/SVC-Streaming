import os

iters = [i for i in range(1, 10)]
iters = [1, 2, 5]
hrch = [i for i in range(3)]

for itr in iters:
    if not os.path.exists('vtl/output_'+str(itr)):
        os.makedirs('vtl/output_'+str(itr))
        os.makedirs('vtl/output_'+str(itr)+'/codes')
        os.makedirs('vtl/output_'+str(itr)+'/images')
    for h in hrch:
        os.system('bash train.sh '+str(h)+' ../vcodec/h'+str(h)+'/model_iters_'+str(itr)+' '+str(itr)+' input output >> vtl/output_'+str(itr)+'/results.txt')
    os.system('cp -r input/cframes/* vtl/output_'+str(itr)+'/images/')
    os.system('cp -r input/vcodes/'+str(itr)+'/* vtl/output_'+str(itr)+'/codes/')
