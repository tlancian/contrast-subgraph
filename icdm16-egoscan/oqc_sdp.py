import networkx as nx
import numpy as np
   
    
def _make_coefficient_matrices(A, weight='weight'):
    N = len(A)
    # w is the matrix of coefficients for 
    # the objective function
    w = np.zeros((N + 1, N + 1))
    # the (0, j)th entry of w is the sum of column j
    w_0j = np.zeros(N + 1)
    w_0j[1:] = A.sum(axis=0)
    w[0, :] = w_0j
    # the (i, 0)th entry of w is the sum of row i
    w_i0 = np.zeros(N + 1)
    w_i0[1:] = A.sum(axis=1).T
    w[:, 0] = w_i0
    # the rest of w (i.e., entries (i, j), such that i != 0 and j != 0)
    # are just the adjacency matrix of G
    w[1:, 1:] = A
    # diagonal elements should be all zero (no self-loops)
    np.fill_diagonal(w, 0.)
    
    # d is the matrix of coefficients for constraint (1)
    # For constraint (1), we want each edge in the final solution to
    # contribute a weight of 1
    # We can think of d as being the corresponding matrix w
    # for a complete graph (i.e., each edge has weight 1)
    d = np.ones((N + 1, N + 1))
    # the (0, j)th entry of d is the sum of column j (i.e., N - 1)
    d_0j = np.ones(N + 1) * (N - 1)
    d[0, :] = d_0j
    # same for the (i, 0)th entries
    d_i0 = np.ones(N + 1) * (N - 1)
    d[:, 0] = d_i0
    np.fill_diagonal(d, 0.)

    return w, d


def random_projection(L, A, W, D, alpha, t=100, return_x_rounded=False):
    '''
        Input:
        L: Solution matrix from SDP
        A: Adjacency matrix
        alpha: parameter of OQC problem
        
        Returns:
        S: Set of nodes obtained from rounding
    '''
    # random projection algorithm
    # Repeat t times
    count = 0
    x_rounded = -1 * np.ones(len(L))
    x_rounded[0] = 1
    obj = 0
    K = alpha * np.ones((len(L) - 1, len(L) - 1))
    np.fill_diagonal(K, 0.)
    K = np.matrix(K)
    sum_weights = (A - K).sum()
    #sum_weights = A.sum()
    obj_orig = ((sum_weights + np.trace((W - (alpha * D)) * (L * L.T))) / 8.)

    while (count < t):
        r = np.matrix(np.random.normal(size=len(L)))
        L_0_sign = np.array(np.sign(L[0] * r.T))[0][0]
        x = np.sign(L * r.T) == L_0_sign
        x = x * 1
        x[x == 0] = -1
        #o = (x[1:, :].T * (A - K) * x[1:, :]).tolist()[0][0]
        o = ((sum_weights + x.T * (W - (alpha * D)) * x) / 8.).tolist()[0][0]
        #o = ((sum_weights + x.T * W * x) / 8.).tolist()[0][0]
        if o > obj:
            x_rounded = x
            obj = o
        count += 1
    # solution is the set of nodes with the same orientation
    # as x_0
    S = [n for n in xrange(1, len(L)) if x_rounded[n] == x_rounded[0]]
    if return_x_rounded:
        x_rounded = np.matrix(x_rounded)
        if x_rounded.shape[0] != len(L):
            x_rounded = x_rounded.T
        return x_rounded
    return S, obj_orig, obj


def semidefinite_cholesky(X):
    # the Cholesky decomposition is defined for 
    # positive definite matrices. We have to add
    # a small constant to X to make it PD
    V = np.array(X.value) if type(X) not in [np.array, np.ndarray] else X

    eps = 1e-10
    while True:
        try:
            L = np.linalg.cholesky(V + (eps * np.identity(len(V))))
            L = np.matrix(L)
            break
        except np.linalg.LinAlgError:
            eps *= 10
    # print a warning if epsilon starts getting too big
    if (eps >= 1e-3):
        print "WARNING in Cholesky Decomposition:"
        print "Input matrix had to be perturbed by", eps
    return L


def random_projection_qp(L, P, A, alpha, t=100, seed=None, return_x_rounded=False):
    '''
        Input:
        L: Solution matrix from SDP
        P: ceofficient matrix of SDP
        A: Adjacency matrix
        alpha: parameter of OQC problem
        
        Returns:
        S: Set of nodes obtained from rounding
        obj_orig: The objective value before rounding
        obj: The objective value of the rounded matrix
    '''
    # random projection algorithm
    # Repeat t times
    eps = 1e-6
    count = 0
    sum_weights = A.sum() - alpha * (len(A) * (len(A) - 1))
    # initial solution: S = \emptyset (1, -1, ... , -1)
    x_rounded = -1 * np.ones(len(L))
    x_rounded[0] = 1
    obj = 0
    if seed is not None:
        x_rounded[seed] = 1
        obj = ((sum_weights + np.matrix(x_rounded) * P * np.matrix(x_rounded).T) / 8.)[0, 0]
    obj_orig = (sum_weights + np.trace(P * (L * L.T))) / 8.

    while (count < t):
        r = np.matrix(np.random.normal(size=len(L)))
        L_0_sign = np.sign(L[0] * r.T)[0, 0]
        x = np.sign(L * r.T) == L_0_sign
        x = x * 1
        x[x == 0] = -1
        o = ((sum_weights + x.T * P * x) / 8.)[0, 0]
        #print "number of nodes in set:",  x[x == 1].shape
        #S = G.subgraph([(n - 1) for n in xrange(1, len(L)) if x[n] == x[0]])
        #print o
        #print x.shape
        if o > obj + eps:
            x_rounded = x
            obj = o
            #print "found a better solution"
            #print obj
            #S = [(n - 1) for n in xrange(1, len(L)) if x_rounded[n] == x_rounded[0]]
            #print S
        count += 1
    # solution is the set of nodes with the same orientation
    # as x_0
    S = [n for n in xrange(1, len(L)) if x_rounded[n] == x_rounded[0]]
    if return_x_rounded:
        x_rounded = np.matrix(x_rounded)
        if x_rounded.shape[0] != len(L):
            x_rounded = x_rounded.T
        return x_rounded
    return S, obj_orig, obj


def charikar_projection(L, P, A, alpha, t=100, return_x_rounded=False):
    '''
        Input:
        L: Solution matrix from SDP
        P: ceofficient matrix of SDP
        A: Adjacency matrix
        alpha: parameter of OQC problem
        
        Returns:
        S: Set of nodes obtained from rounding
        obj_orig: The objective value before rounding
        obj: The objective value of the rounded matrix
    '''
    # random projection algorithm
    # Repeat t times
    eps = 1e-6
    count = 0
    # initial solution: S = \emptyset (1, -1, ... , -1)
    x_rounded = -1 * np.ones(len(L))
    x_rounded[0] = 1
    obj = 0
    n = len(L)
    sum_weights = A.sum() - alpha * (len(A) * (len(A) - 1))
    #obj_orig = (sum_weights + np.trace(P * (L * L.T))) / 8.
    obj_orig = (np.trace(P * (L * L.T))) / 8.
    T = 2 * np.sqrt(np.log2(n))
    #T = 1
    t = 100
    all_ones = np.ones((n, 1))

    while (count < t):
        r = np.matrix(np.random.normal(size=n))
        #z_0 = ((L[0] * r.T)[0, 0]) / T
        #y_0 = np.sign(z_0) * np.minimum(np.abs(z_0), 1.)
        #assert(np.abs(y_0) <= 1)
        #p_0 = ((1 - y_0) / 2.)
        #L_0_sign =  np.sign((np.random.uniform() - p_0) + eps)
        z = (L * r.T) / T
        print "|z_i| > 1:", z[np.abs(z) > 1].shape[1], np.abs(z).mean()
        true_nodes = [0, 2, 6, 7, 10, 14, 18, 55, 42, 58]
        y = np.multiply(np.sign(z), np.minimum(np.abs(z), all_ones))
        p = (1 - y) / 2
        print "z vector:", z[true_nodes]
        print "y vector:", y[true_nodes]
        print "p vector:", p[true_nodes]
        assert(np.all(p >= 0) and np.all(p <= 1))
        unif_numbers = np.matrix(np.random.uniform(size = n)).T
        #x = np.sign(unif_numbers - p) == L_0_sign
        x = np.sign((unif_numbers - p) + eps)
        print "x vector:", x[true_nodes]
        S = [(i - 1) for i in xrange(1, len(L)) if x[i] == x[0]]
        #if len(S) < 20:
        #    print S
        #x = x * 1
        #x[x == 0] = -1
        #o = ((sum_weights + x.T * P * x) / 8.)[0, 0]
        o = ((x.T * P * x) / 8.)[0, 0]
        print "number of nodes in set:",  x[x == x[0, 0]].shape
        print o
        if o > obj + eps:
            x_rounded = x
            obj = o
            print "found a better solution"
            #print obj
            #S = [(n - 1) for n in xrange(1, len(L)) if x_rounded[n] == x_rounded[0]]
            #print S
        count += 1
    # solution is the set of nodes with the same orientation
    # as x_0
    S = [i for i in xrange(1, n) if x_rounded[i] == x_rounded[0]]
    #x = -1 * np.ones(len(L))
    #x[true_nodes] = 1
    #x = np.matrix(x)
    #print "Optimal: ", ((x * P * x.T) / 8.)[0, 0] 
    if return_x_rounded:
        x_rounded = np.matrix(x_rounded)
        if x_rounded.shape[0] != len(L):
            x_rounded = x_rounded.T
        return x_rounded
    return S, obj_orig, obj
