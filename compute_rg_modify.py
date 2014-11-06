import numpy as np
import sys
import matplotlib.pyplot as plt

Rg = []
check = False

k=0
G_list = [0,2.4,4.8,7.2,9.6,12,14.4]
for G in [0,2.4,4.8,7.2,9.6,12,14.4]:
	Rg.append([])
	for j in range(1,51,1):
		check = False
		with open("log.wlc_lj_n300_G"+str(G)+"_"+str(j)+".txt",'r') as f:
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
	k += 1

Rg = np.array(Rg)

for i in range(len(Rg)):
	hist, bins = np.histogram(Rg[i],50,density=True)
	plt.plot(bins[:-1],hist,'o')
	plt.xlabel(r'$\langle R_{g} \rangle$')
	plt.ylabel('Probability')
	plt.title("G="+str(G_list[i]))

	plt.savefig("G="+str(G_list[i])+".png")
	plt.clf()

