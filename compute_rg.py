import numpy as np
import sys

filename = sys.argv[1]
Rg = []
check = False

with open(filename,'r') as f:
	for i, line in enumerate(f):
		if not line.strip():
			continue
		else:
			if line.split()[0] == "Loop" and line.split()[1] == "time":
				break
			if check:
				Rg[k].append(float(line.split()[3]))
				#Rd[k].append(float(line.split()[4]))
			else:
				if line.split()[0] == "Step" and line.split()[1] == "CPULeft":
					check = True

Rg = np.array(Rg)
Rg_mean = np.mean(Rg)
print Rg_mean
