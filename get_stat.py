import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import *

Rg = []
Rd = []
k=0

for n in [10,13,16,20,26,32,40,51,64,80,100,118,140,170,200,225,270,300,370,400,430,500,600,700,800,900,1000]:
	Rg.append([])
	Rd.append([])
	for j in range(1,6,1):
		check = False
		with open("log.wlc_n"+str(n)+"_"+str(j)+".txt",'r') as f:
			for i, line in enumerate(f):
				if not line.strip():
					continue
				else:
					if line.split()[0] == "Loop" and line.split()[1] == "time":
						break
					if check:
						Rg[k].append(float(line.split()[3]))
						Rd[k].append(float(line.split()[4]))
					else:
						if line.split()[0] == "Step" and line.split()[1] == "CPULeft":
							check = True
	k += 1

nn = np.array([10,13,16,20,26,32,40,51,64,80,100,118,140,170,200,225,270,300,370,400,430,500,600,700,800,900,1000])
Rg = np.square(np.array(Rg))
Rd = np.array(Rd)
Rd_scale = np.mean(Rd,axis=1)/(2*1.13*nn)

def wlc_fit(x,lp):
	return lp*(1-(lp/(1.13*x))*(1-np.exp(1-x*1.13/lp)))

popt, pcov = curve_fit(wlc_fit,nn[:11],Rd_scale[:11])

wlc_fit = np.vectorize(wlc_fit)

fitnn = np.linspace(10,100,1)
fitRd_scale = wlc_fit(fitnn,popt[0])

Rg_dist = []
Rd_dist = []

Rg_stat = np.dstack((nn,np.mean(Rg,axis=1),np.std(Rg,axis=1)/sqrt(len(Rg[0]))))
Rd_stat = np.dstack((nn,np.mean(Rd,axis=1),np.std(Rd,axis=1)/sqrt(len(Rd[0]))))

for i in range(10):
	Rg_dist.append(np.histogram(Rg[i],bins=30,density=True))
	Rd_dist.append(np.histogram(Rd[i],bins=30,density=True))

#n, bins, patches = plt.hist(Rg,30,normed=1)
###########################
# plot Rg 
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$R_g$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
ax.errorbar(nn,Rg_stat[0][:,1],Rg_stat[0][:,2],fmt='o',label='simulation')
legend = ax.legend(loc='upper right')

fig.savefig("Rg.png")
fig.clf()

###########################
# plot Rd
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$R_d$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
ax.errorbar(nn,Rd_stat[0][:,1],Rd_stat[0][:,2],fmt='o',label='simulation')
legend = ax.legend(loc='upper right')

fig.savefig("Rd.png")
fig.clf()

##########################
# plot scale-graph
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\langle R_e^2 \rangle/(2l_{0}N)$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
plt.plot(nn,Rd_scale,'o')
plt.plot(fitnn,fitRd_scale)

fig.savefig("Rd_scale.png")
fig.clf()

