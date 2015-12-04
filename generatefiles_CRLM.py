import os
import numpy as np

N = 10000
M = 0

ensemble = 10

for i in range(ensemble):
	datafilename = 'RSM_fene_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+'.dat'
	inputfilename = 'RSM_fene_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+'.in'
	os.system('python RCGM_datafile.py -n '+str(N)+' -l 1.00 -f s --mode=rsm -c '+str(M)+' -o ' + datafilename)
	#os.system('python RCGM_inputfile.py -i ' + datafilename + ' -o ' + 'RSM_LJ_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+' -n '+str(N)+' -t 1.2 -d 50000000 -l 1.0 -k 100 -f s -v wca '+inputfilename)
	#os.system('python write_batch_RCLM.py '+'run_RSM_LJ_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+'.sh ' + inputfilename)
	#os.system('python RCGM_datafile.py -n '+str(N)+' -l 1.0 -f s -v -a -c '+str(M)+' -o ' + datafilename)
	#os.system('python RCGM_inputfile.py -i ' + datafilename + ' -o ' + 'RSM_LJ_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+' -n '+str(N)+' -t 1.2 -d 50000000 -l 1.0 -k 100 -f s -v wca -a 10 '+inputfilename)
	#os.system('python write_batch_RCLM.py '+'run_RSM_LJ_n'+str(N)+'_c'+str(M)+'_'+str(i+1)+'.sh ' + inputfilename)