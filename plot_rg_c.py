import numpy as np
import sys
import matplotlib.pyplot as plt

finname = sys.argv[1:-1]
foutname = sys.argv[-1]
datalst = []
rg = []

for fname in finname:
	check = False
	with open(fname,'r') as f:
		for i, line in enumerate(f):
			if not line.strip():
				continue
			else:
				if line.split()[0] == "Loop" and line.split()[1] == "time":
					break
				if check:
					data = np.float_(line.split())
					data = data[np.array([0,3])]
					datalst.append(data)
				else:
					if line.split()[0] == "Step" and line.split()[1] == "CPULeft":
						check = True

	rg.append(np.mean(datalst[30000:]))

with open(foutname,'a') as f:
	f.write(str(rg[-1]).ljust(10)+"\n")
#fig,ax = plt.subplots()
#ax.plot(np.arange(1,201),rg)
#ax.set_xlabel('number of constrains')
#ax.set_ylabel('Rg')
#plt.savefig(foutname)