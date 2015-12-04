for i in range(50):
	with open('run_n4000_'+str(i+1)+'.sh','w') as f:
		f.write('#!/bin/tcsh\n')
		f.write('#SBATCH -n 20\n')
		f.write('#SBATCH -t 00:1000:00\n')
		f.write('\n')
		f.write('\n')
		f.write('module load intel\n')
		f.write('module load openmpi/intel/1.6.5\n')
		f.write('\n')
		f.write('mpirun -bind-to-core /lustre/gshi1/lmp < /lustre/gshi1/lj_chain/n4000_G0/cooling/wlc_lj_n4000_G0_T2.0_input_'+str(i+1)+'.txt\n')