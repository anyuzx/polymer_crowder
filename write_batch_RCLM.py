import sys

filename = sys.argv[1]
inputfilename = sys.argv[2]

with open(filename,'w') as f:
	f.write('#!/bin/tcsh\n')
	f.write('#SBATCH -n 20\n')
	f.write('#SBATCH -t 00:800:00\n')
	f.write('\n')
	f.write('cd /lustre/gshi1/TAD_model/RSM')
	f.write('\n')
	f.write('module load intel\n')
	f.write('module load openmpi/intel/1.6.5\n')
	f.write('\n')
	f.write('mpirun -bind-to-core /lustre/gshi1/lmp < /lustre/gshi1/TAD_model/RSM/'+inputfilename+'\n')