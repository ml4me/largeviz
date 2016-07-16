from rpforest import RPForest
import numpy as np
from heapq import heappush, heappop, heappushpop, nsmallest


np.random.seed(42)
def lvnn(fp, nt=3, k=5, iter= 2, leaves=50):
    
    nn=np.zeros((fp.shape[0],k), dtype='int')-1
    nn_d=np.zeros((fp.shape[0],k))-1
    
    print(' start Tree build')
    model = RPForest(leaf_size=leaves, no_trees=nt)
    model.fit(fp)
    for i in range(0,fp.shape[0]):
        nn[i,:] =model.query(fp [i,],k)
    
    t=0
    print('startnn')
    ii=[i]*(k*k)
    while t<iter:
        t +=1
        old_nn=nn
        for i in range(0,fp.shape[0]):
            ji = old_nn[i,:]
            li = old_nn[ji,:]
            jli = li.flatten()
            d=np.linalg.norm(fp [ii,:]-fp [jli,:], axis=1)
            mind=np.argpartition(d,k)
            nn [i,:]=jli[mind[:k]]
            nn_d [i,:]=d[mind[:k]]
            
    
    csr=np.zeros((fp.shape[0]*k, 3))
    print('start split')
    l=0
    for i in range(fp.shape[0]):
        for j in range(k):
            csr [l,0]=i
            csr [l,1]=nn[i,j]
            csr [l,2]=nn_d[i,j]
            l=l+ 1
    return csr

def testit():
    fp = np.random.randn(1000,1000)
    k=10
    from sklearn.neighbors import NearestNeighbors
    from sklearn.neighbors import kneighbors_graph
    import time
    print(' start skLearn')
    ms = time.time()*1000.0
    (kneighbors_graph(fp, k))
    print(' time',(time.time()*1000.0)-ms)
    print(' start rp nn')
    ms = time.time()*1000.0
    
    lvnn(fp, k=k)
    print(' time',(time.time()*1000.0)-ms)
    
import cProfile
st=cProfile.run('testit()', filename='stat.txt', sort='cumtime')
