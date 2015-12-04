import sys
M = int(sys.argv[1])
dirname = sys.argv[2]
c=M
for i in range(100):
	with open(dirname+'/run_n300_c'+str(c)+'_'+str(i+1)+'.sh','w') as f:
		f.write('#!/bin/tcsh\n')
		f.write('#SBATCH -n 12\n')
		f.write('#SBATCH -t 00:60:00\n')
		f.write('\n')
		f.write('cd /lustre/gshi1/RCGM/n300')
		f.write('\n')
		f.write('module load intel\n')
		f.write('module load openmpi/intel/1.6.5\n')
		f.write('\n')
		f.write('mpirun -bind-to-core /lustre/gshi1/lmp < /lustre/gshi1/RCGM/n300/RCGM_n300_c'+str(c)+'_'+str(i+1)+'.in\n')