import numpy as np
import sys
import giveloops
import os

N = int(sys.argv[1])
M = int(sys.argv[2])
f_str = sys.argv[3]
dirname = sys.argv[4]
mesh = (10,10)

giveloops.write_to_file(N,M,f_str,mesh=mesh)
for i in range(mesh[0]):
	for j in range(mesh[1]):
		with open('temp.dat','w') as ff:
			with open(f_str,'r') as f:
				check = False
				for k,line in enumerate(f):
					if check:
						if line.split()[0] != 'group':
							ff.write(line)
						else:
							check = False
							break
					if line == 'group '+str(i+1)+' set '+str(j+1)+'\n':
						check = True
		index = i*10+j+1
		os.system('python RCGM_datafile.py -n '+str(N)+' -l 1.0 -f s -v -c '+str(M)+' -o '+ dirname+'/'+'RCGM_n'+str(N)+'_c'+str(M)+'_'+str(index)+'.dat '+'-i temp.dat')

