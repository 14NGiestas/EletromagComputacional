import numpy as np

def direct_sum(A,B):
    C = np.zeros(np.add(A.shape,B.shape))
    C[:A.shape[0],:A.shape[1]]=A
    C[A.shape[0]:,A.shape[1]:]=B
    return C

