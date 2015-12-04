import numpy as np

def p(lmin,lmax):
    a = 1/np.sum(1.0/np.arange(lmin,lmax+1))
    return a/np.arange(lmin,lmax+1)

def singl(lmin,lmax):
    temp = np.cumsum(p(lmin,lmax))
    rnd = np.random.random()
    index = np.searchsorted(temp,rnd)
    return index + lmin

def givel(N,M,lmin,lmax):
    temp = []
    for i in range(M):
        temp.append(singl(lmin,lmax-1-np.sum(temp)-lmin*(M-i-1)))
    temp = np.array(temp)
    sortl = np.sort(np.random.choice(N-np.sum(temp+1),len(temp),replace=False))
    y = np.cumsum(temp)+sortl
    x = y - temp
    pair = np.dstack((x,y))
    return temp, pair[0]

# define function to generate the proper initial loop configuration
def GLC(N,M):
    l,pair = givel(N,M,100,3000)
    
    chain = np.zeros((N,3))
    chain[:,0] = np.arange(N)+1
    
    for item in pair+1:
        temp1 = np.copy(chain[item[0]-1])
        temp2 = np.copy(chain[item[1]-1])
        l = item[1] - item[0]
        j = 1
        for i in np.arange(1,l/2+1):
            chain[item[0]-1+i,:2] = np.array([temp1[0],temp1[1]+j])
            j += 1
        j -= 1
        for i in np.arange(l/2+1,l+1):
            chain[item[0]-1+i,:2] = np.array([temp1[0]+1,temp1[1]+j])
            j -= 1
        chain[item[1]:] += chain[item[1]-1] - temp2

    chain = chain - np.int_(np.mean(chain,axis=0))
    return chain,pair+1