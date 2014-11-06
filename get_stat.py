import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import *

Rg1 = []
Rg2 = []
Rd1 = []
Rd2 = []

k=0
for n in [10,13,16,20,26,32,40,51,64,80]:
	Rg1.append([])
	Rd1.append([])
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
						Rg1[k].append(float(line.split()[3]))
						Rd1[k].append(float(line.split()[4]))
					else:
						if line.split()[0] == "Step" and line.split()[1] == "CPULeft":
							check = True
	k += 1

k = 0
for n in [100,125,159,200,252,317,400,501,600,700,795,900,1000]:
	Rg2.append([])
	Rd2.append([])
	for j in range(1,11,1):
		check = False
		with open("test/log.restart.wlc_n"+str(n)+"_"+str(j)+".txt",'r') as f:
			for i, line in enumerate(f):
				if not line.strip():
					continue
				else:
					if line.split()[0] == "Loop" and line.split()[1] == "time":
						break
					if check:
						Rg2[k].append(float(line.split()[3]))
						Rd2[k].append(float(line.split()[4]))
					else:
						if line.split()[0] == "Step" and line.split()[1] == "CPULeft":
							check = True
	k += 1

nn = np.array([10,13,16,20,26,32,40,51,64,80,100,125,159,200,252,317,400,501,600,700,795,900,1000])
Rg1 = np.square(np.array(Rg1))
Rg2 = np.square(np.array(Rg2))
Rd1 = np.array(Rd1)
Rd2 = np.array(Rd2)

Rg_square_mean = np.concatenate((np.mean(Rg1,axis=1),np.mean(Rg2,axis=1)))
Rd_square_mean = np.concatenate((np.mean(Rd1,axis=1),np.mean(Rd2,axis=1)))
Rg_square_std = np.concatenate((np.std(Rg1,axis=1)/sqrt(len(Rg1[0])),np.std(Rg2,axis=1)/sqrt(len(Rg2[0]))))
Rd_square_std = np.concatenate((np.std(Rd1,axis=1)/sqrt(len(Rd1[0])),np.std(Rd2,axis=1)/sqrt(len(Rd2[0]))))

def wlc_fit(x,l0,lp):
	return 2*l0*(x-1)*lp*(1-(lp/(l0*(x-1)))*(1-np.exp(-(x-1)*l0/lp)))

def wlc_fit2(x,l0,lp):
	return lp*(1-(lp/(l0*(x-1)))*(1-np.exp(-(x-1)*l0/lp)))

def wlc_ve_fit(x,b):
	return 1.176*x + b

popt, pcov = curve_fit(wlc_fit,nn[:11],Rd_square_mean[:11])
popt2, pcov2 = curve_fit(wlc_ve_fit,np.log10(nn[13:]),np.log10(Rd_square_mean[13:]))
Rd_scale = Rd_square_mean/(2*popt[0]*(nn-1))
Rd1/(2*pop1[0]*(nn-1))

fitlabel_Rd_square_mean = r"$\langle R_{ee}^{2} \rangle \backsim N^{2\nu}$"
fitlabel_Rd_scale1 = r"$\frac{\langle R_{ee}^{2} \rangle}{2 l_{0}N} = 2 l_{p}{1-\frac{l_p}{N l0}[1-\mathrm{exp}(-Nl0/l_p)]}$"
fitlabel_Rd_scale2 = r"$\backsim N^{2\nu -1}$"

wlc_fit = np.vectorize(wlc_fit)
wlc_fit2 = np.vectorize(wlc_fit2)

fitnn = np.linspace(10,600,100)
fitRd_scale1 = wlc_fit2(fitnn,popt[0],popt[1])
fitnn2 = np.linspace(10,1000,100)
fitRd_scale2 = (10**popt2[0])*(fitnn2**1.176)/(2*popt[0]*fitnn2)
fitRd = (10**popt2[0])*(fitnn2**1.176)

#Rg_dist = []
#Rd_dist = []

#Rg_stat = np.dstack((nn,Rg_square_mean,np.std(Rg,axis=1)/sqrt(len(Rg[0]))))
#Rd_stat = np.dstack((nn,np.mean(Rd,axis=1),np.std(Rd,axis=1)/sqrt(len(Rd[0]))))

#for i in range(10):
#	Rg_dist.append(np.histogram(Rg[i],bins=30,density=True))
#	Rd_dist.append(np.histogram(Rd[i],bins=30,density=True))

#n, bins, patches = plt.hist(Rg,30,normed=1)
###########################
# plot Rg 
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\langle R_{g}^{2} \rangle$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
ax.plot(nn,Rg_square_mean,'o',label='simulation')
legend = ax.legend(loc='upper right')

fig.savefig("Rg.png")
fig.clf()

###########################
# plot Rd
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\langle R_{ee}^{2} \rangle$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
ax.errorbar(nn,Rd_square_mean,Rd_square_std,fmt='o',label = 'simulation')
ax.plot(fitnn2,fitRd,label=fitlabel_Rd_square_mean)
legend = ax.legend(loc='upper right')

fig.savefig("Ree.png")
fig.clf()

##########################
# plot scale-graph
fig,ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\langle R_{ee}^{2} \rangle/(2l_{0}N)$")
ax.set_xticks([10,100,1000])
ax.set_xticklabels(["10","100","1000"])
plt.plot(nn,Rd_scale,'o',fitnn,fitRd_scale1,fitnn2,fitRd_scale2)
#ax.plot(fitnn,fitRd_scale)

fig.savefig("Ree_scale.png")
fig.clf()

