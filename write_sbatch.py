for n in [100,125,159,200,252,317,400,501,600,631,700,795,900,1000]:
	for j in range(1,11):
		with open("run_"+str(n)+"_"+str(j)+".sh",'w') as f:
			f.write("#!/bin/tcsh\n")
			f.write("#SBATCH -n 12\n")
			if n <= 500:
				f.write("#SBATCH -t 00:60:00\n")
			elif n > 500:
				f.write("#SBATCH -t 00:90:00\n")
			#f.write("#SBATCH --gres=gpu\n")
			f.write("\n")
			f.write("cd crowder2\n")
			f.write("\n")
			f.write("module load intel\n")
			f.write("module load openmpi/intel/1.6.5\n")
			#f.write("module load cuda\n")
			f.write("\n")
			f.write("mpirun -bind-to-core lmp < "+"wlc_n"+str(n)+"_input_"+str(j)+".txt\n")