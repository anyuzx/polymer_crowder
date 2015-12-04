import numpy as np
import sys

def weightfunc(N,gamma):
	#return 2*float((N-l))/((N-1)*(N-2))
	l = np.arange(N-2,dtype=float)+2
	return l**(gamma)

def giveloops(N,M,gamma):
	looplst = []
	# initial i dic
	idic = np.empty(N-2)
	factor = np.empty(N-2)
	for i in np.arange(N-2)+2:
		idic[i-2] = N-i
		factor[i-2] = N-i

	# define cummulative list generated function
	def cumlst(N):
		return (weightfunc(N,gamma)/factor)*idic

	# pick up the item M times
	for i in range(M):
		temp = cumlst(N)
		f = np.cumsum(temp)
		f = np.float_(f)/f[-1]
		rndn = np.random.random()
		index = np.searchsorted(f,rndn)
		idic[index] = idic[index]-1
		looplst.append(index+2)

	looplst = np.array(looplst)
	looplst = np.sort(looplst)
	#return np.prod((looplst+1)**(1.0/len(looplst)))-1
	return looplst, (np.prod((looplst+1)**(1.0/len(looplst)))-1)/N

#N=300
#M=100
#llst = giveloops(N,M,0)
#unique, counts = np.unique(llst,return_counts=True)
#pairlst=[]
#for item in zip(unique,counts):
#	temp1 = np.random.choice(np.arange(N-item[0])+1,item[1])
#	temp2 = temp1+item[0]
#	pairlst.append(zip(temp1,temp2))

#print np.array(pairlst)

def givepair(N,M,*args,**kwargs):
	mesh = kwargs.get('mesh',None)
	try:
		mesh[0]
	except:
		sys.exit('please specify the mesh')

	count = np.zeros(mesh[0]*5)
	pairset = [[] for i in range(mesh[0])]
	pairgroup = [[] for i in range(mesh[0])]
	ave_lset = []
	for gamma in [-1,-0.8,-0.5,-0.3,0,0.5,1,2,3,4,5,6,7,8,9,10]:
		for i in range(500):
			llst,ave_l = giveloops(N,M,gamma)
			index = int(np.floor(ave_l/(1.0/(mesh[0]*5))))
			if count[index] < mesh[1]:
				count[index] += 1
				pairset[index/5].append(llst)
				ave_lset.append(ave_l)
			else:
				continue


	for i in range(mesh[0]):
		if len(pairset[i]) < mesh[1]:
			print 'try again: no enough sample is accquired'
			sys.exit()
		else:
			temp = np.array(pairset[i])[np.random.choice(len(pairset[i]),mesh[1],replace=False)]
			for j in range(mesh[1]):
				unique,counts = np.unique(temp[j],return_counts=True)
				temp3 = []
				for item in zip(unique,counts):
					temp1 = np.random.choice(np.arange(N-item[0])+1,item[1],replace=False)
					temp2 = temp1+item[0]
					temp3.append(zip(temp1,temp2))
				pairgroup[i].append(temp3)

	return count,pairgroup,ave_lset

def write_to_file(N,M,f_str,*args,**kwargs):
	mesh = kwargs.get('mesh',None)
	try:
		mesh[0]
	except:
		sys.exit('please specify the mesh')

	count,pairgroup,ave_lset = givepair(N,M,mesh=mesh)
	with open(f_str,'w') as f:
		for i in range(mesh[0]):
			for j in range(mesh[1]):
				f.write('group '+str(i+1)+' set '+str(j+1)+'\n')
				for item in pairgroup[i][j]:
					for itemitem in item:
						f.write(str(itemitem[0]).ljust(10)+str(itemitem[1])+'\n')

#count,pairgroup,ave_lset = givepair(300,30,mesh=(10,10))
#print pairgroup[0]

#write_to_file(300,100,'loopfile.dat',mesh=(10,10))






#print np.array(pairset[0])[np.random.choice(len(pairset[0]),10,replace=False)]



#fig,ax=plt.subplots()
#n,bins,patches=ax.hist(ave_lset,bins=10,range=(0,1))
#plt.show()

#def giveplot(N,M,gamma):
#	hist = []
#	for i in range(1000):
#		hist.append(giveloops(N,M,gamma))
#	n,bins,patches = ax.hist(hist,50,normed=1,label=r'$w(l)=l^{'+str(gamma)+'}$')
#	ax.set_title(r'$\mathrm{Histogram\ of\ \langle \mathcal{L} \rangle:}\ M=$'+r'${}$'.format(M)+' '+r'$N={}$'.format(N))

#M=2
#N=300
#fig, ax = plt.subplots()
#for gamma in [-1,-0.8,-0.5,-0.3,0,0.5,1,1.5,2]:
#	giveplot(N,M,gamma)
#giveplot(300,10,-1)
#giveplot(300,10,0)
#giveplot(300,10,1)
#ax.set_xlabel(r'$\langle \mathcal{L} \rangle$')
#ax.set_ylabel(r'$Probability$')
#plt.legend(loc='upper right')
#ax.text(0.97,0.97,r'$w(l)=l^{'+str(gamma)+'}$',horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
#ax.set_title(r'$\mathrm{Histogram\ of\ \langle \mathcal{L} \rangle:}\ M=$'+r'${}$'.format(M)+' '+r'$N={}$'.format(N))
#plt.show()

