# coding: utf-8
import networkx as nx
import oqc_sdp
import sys
import os
import numpy as np
import scipy.io
import subprocess
import time
from greedy_oqc import localSearchNegativeOQC
import pickle


DIR = 'tmp'
CVXPATH = 'cvx'
alpha = float(sys.argv[2])
def make_matlab_script(prefix, N):
    with open("%s/solveSDP%s.m" % (CVXPATH, prefix.replace('-', '')), 'w') as f:
        f.write("cvx_setup\n")
        f.write("load('../%s/%s.mat')\n" % (DIR, prefix))
        f.write("cvx_solver sedumi\n")
        f.write("cvx_begin sdp\n")
        f.write("    variable X(%s, %s) symmetric\n" % (N, N))
        f.write("    maximize trace(P*X)\n")
        f.write("    subject to\n")
        f.write("        X >= 0;\n")
        f.write("        diag(X) == ones(%s, 1);\n" % N)
        f.write("cvx_end\n")
        f.write("save('../%s/%s.txt', 'X', '-ASCII');\n" % (DIR, prefix))
        f.write("exit;\n")


def write_output(sdp_results, outfname, subgraphfile):
    S, obj, obj_rounded = sdp_results

    print "Returning subgraph with OQC score", obj_rounded, "(%s)" % obj
    n = len(S)
    if 'weight' in S.edges_iter(data=True).next()[2]:
        e = sum(data['weight'] for u, v, data in S.edges_iter(data=True))
    else:
        e = S.number_of_edges()
    header = "|S|,|E|,density,diameter,triangle density,OQC,obj\n"
    with open(outfname, 'w') as f:
        f.write(header)
        if n > 0:
            f.write(str(n) + ',')
            f.write(str(S.number_of_edges()) + ',')
            if n > 1:
                f.write(str(2. * e / (n * (n - 1))) + ',')
            else:
                f.write(str(0) + ',')
            if nx.is_connected(S):
                f.write(str(nx.diameter(S)) + ',')
            else:
                f.write('inf,')
            if n > 2:
                f.write(str(2. * sum(i for i in nx.triangles(S).itervalues()) / (n * (n - 1) * (n - 2))) + ',')
            else:
                f.write(str(0) + ',')
            f.write(str(obj_rounded) + ',')
            f.write(str(obj) + '\n')
        else:
            f.write("0,0,0,0,0,0,0,")
            f.write("%s\n" % obj)
    nx.write_weighted_edgelist(S, subgraphfile)


def main():
    graphfile = sys.argv[1]
    #outfname = sys.argv[2]
    #subgraphfile = sys.argv[3]
    upper_bound = 0

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    # load graph
    G = nx.Graph()
    with open(graphfile) as f:
        for line in f:
            tokens = line.strip().split()
            u = int(tokens[0])
            v = int(tokens[1])
            w = float(tokens[2])
            G.add_edge(u, v, weight=w)
    print "Loaded graph with %s nodes and %s edges from %s" % (len(G), G.number_of_edges(), graphfile)
    A = nx.to_numpy_matrix(G)
    w, d = oqc_sdp._make_coefficient_matrices(A)
    P = np.matrix(w - alpha * d)
    filename = os.path.split(graphfile)[1]
    # make matlab input
    prefix = os.path.splitext(filename)[0]
    scipy.io.savemat('%s/%s.mat' % (DIR, prefix), mdict={'P': (1 / 4.) * P})
    make_matlab_script(prefix, len(P))
    # run matlab
    subprocess.call("run_matlab.sh solveSDP%s" % prefix.replace('-', '') , shell=True)
    # rounding step
    X = scipy.loadtxt('%s/%s.txt' % (DIR, prefix))
    L = oqc_sdp.semidefinite_cholesky(X)
    nodeset, obj, obj_rounded = oqc_sdp.random_projection_qp(L, P, A, alpha, t=1000)
    nodes = G.nodes()
    S_bar = G.subgraph([nodes[i - 1] for i in nodeset])
    # do local search to try to improve solution
    S, obj_rounded = localSearchNegativeOQC(G, alpha, t_max=50, seed=S_bar)
    #with open('%s/%s.pickle' % (DIR, prefix), 'w') as handle:
    #    pickle.dump([list(S.nodes), obj_rounded], handle, -1)

    
    with open('%s/%s.txt' % (DIR, prefix), 'w') as res:
        res.write(str(S.nodes()))
        res.close()
        
    
    #n_choose_2 = len(nodeset) * (len(nodeset) - 1) / 2
    #density = (obj_rounded + (alpha * n_choose_2)) / n_choose_2
    #write_output((S, obj, obj_rounded), outfname, subgraphfile)
    



if __name__ == '__main__':
    main()
