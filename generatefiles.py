import os
import numpy as np

clist = np.delete(np.arange(30)+11,[9,19,29])

for c in clist:
	try:
		os.makedirs('n300_c'+str(c))
	except:
		pass
	os.system('python RCGM_writedatafile.py 300 '+str(c)+' loopfile.dat '+'n300_c'+str(c))
	for i in range(100):
		os.system('python RCGM_inputfile.py -i RCGM_n300_c'+str(c)+'_'+str(i+1)+'.dat -o RCGM_n300_c'+ str(c)+'_'+str(i+1)+' -n 300 -t 1.0 -d 50000000 -l 1.0 -k 1.5 -f s n300_c'+str(c)+'/RCGM_n300_c'+str(c)+'_'+str(i+1)+'.in')
	os.system('python write_batch_RCGM.py '+str(c)+' n300_c'+str(c))