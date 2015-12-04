import numpy as np
#import myPackage.tools.lattice_SAW as lattice_SAW
import lattice_SAW
# --------------------------
# description:
# self.looplst : loop length list
# self.pair : loop pair list

# define class for loop model
class LoopModel:
    
    #-------------------------------------------------------------
    def __init__(self,N,M):
        self.looplst = 0
        self.pair = 0
        self.N = N
        self.M = M
        self.chain = []

    # ------------------------------------------------------------
    # define function to generate loop pair for Cross Loop Model
    # No arguments needed for Cross Loop Model
    # Randomly assign M pairs of anchors. Choose each anchor in one pair randomly
    def CLM(self):
        self.pair = np.random.choice(np.arange(1,self.N+1),2*self.M,replace=True).reshape(self.M,2)
        self.pair.sort(axis=1)
        
        self.pair = self.pair[self.pair[:,0].argsort()]
        self.looplst = self.pair[:,1] - self.pair[:,0]
    
    #-------------------------------------------------------------
    # define function to generate loop pair for Linear Loop Model
    def LLM(self,avgl,loopdist='gaussian'):
        x = np.arange(1,self.N)
        pickpdist = pdist()
        if loopdist == 'gaussian':
            cdf = np.cumsum(pickpdist.gaussian(avgl)(x))
        
        while True:
            self.looplst = x[np.searchsorted(cdf,np.random.random(self.M))]
            if np.sum(self.looplst) < self.N-1:
                break
        
        rest = self.N-1-np.sum(self.looplst)
        temp1 = np.sort(np.random.choice(rest,self.M,replace=False))+np.cumsum(self.looplst)
        temp2 = temp1 - self.looplst
        self.pair = np.array(zip(temp2,temp1))
        
        return self.looplst,self.pair
    
    #-------------------------------------------------------------
    # define function to generate loop pair for Rossete string Model
    def RSM(self,avgl,rossete = 4,loopdist='gaussian'):
        x = np.arange(1,self.N)
        pickpdist = pdist()
        if loopdist == 'gaussian':
            cdf = np.cumsum(pickpdist.gaussian(avgl)(x))
            
        while True:
            self.looplst = x[np.searchsorted(cdf,np.random.random(self.M))]
            if np.sum(self.looplst) < self.N - 1:
                break
        
        rest = self.N-1-np.sum(self.looplst)
        temp = np.array_split(np.arange(rest),3*rossete)
        anchor = []
        for i in range(rossete):
            temp3 = []
            temp3.append(np.random.choice(temp[i*3+1],1)[0])
            for j in np.arange([len(np.array_split(np.arange(self.M),rossete)[k]) for k in range(rossete)][i]-1):
                temp3.append(temp3[-1]+np.random.randint(1,5))
            anchor.append(temp3)
        
        anchor = np.array(anchor)
        anchor = anchor.flatten()
        temp1 = anchor + np.cumsum(self.looplst)
        temp2 = temp1 - self.looplst
        self.pair = np.array(zip(temp2,temp1))
        
        return self.looplst,self.pair
    
            
        
    #------------------------------------------------------------
    def givechain(self,SAW=False):
        if SAW:
            self.chain = lattice_SAW.lattice_SAW(self.N,l0=1.0)
        else:
            self.chain = np.zeros((self.N,3))
            self.chain[:,0] = np.arange(self.N)+1
            
            for item in self.pair:
                temp1 = np.copy(self.chain[item[0]-1])
                temp2 = np.copy(self.chain[item[1]-1])
                l = item[1] - item[0]
                j = 1
                for i in np.arange(1,l/2+1):
                    self.chain[item[0]-1+i,:2] = np.array([temp1[0],temp1[1]+j])
                    j += 1
                j -= 1
                for i in np.arange(l/2+1,l+1):
                    self.chain[item[0]-1+i,:2] = np.array([temp1[0]+1,temp1[1]+j])
                    j -= 1
                self.chain[item[1]:] += self.chain[item[1]-1] - temp2

            self.chain = self.chain - np.int_(np.mean(self.chain,axis=0))
        
        return self.chain, self.pair
        

class pdist:
    # define p(l)=A*l^2*exp(-B*l^2)
    def gaussian(self,avg):
        B = 4/(np.pi*(avg**2))
        A = 4*B**(1.5)/np.sqrt(np.pi)
        return lambda l:A*(l**2)*np.exp(-B*(l**2))
    
    # define p(l)=A*(1/l)
    def powerlaw(self,avg,lmin,lmax):
        A = avg/(lmax-lmin+1)
        return lambda l:A*(1.0/l)