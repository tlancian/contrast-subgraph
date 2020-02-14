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


DIR = 'tmp/tommo'
CVXPATH = 'cvx'
alpha = 1
 

def make_matlab_script(prefix, N):
    with open("%s/solveSDP%s.m" % (CVXPATH, prefix.replace('-', '')), 'w') as f:
        f.write("cvx_setup\n")
        f.write("load('%s/%s.mat')\n" % (DIR, prefix))
        f.write("cvx_solver sedumi\n")
        f.write("cvx_begin sdp\n")
        f.write("    variable X(%s, %s) symmetric\n" % (N, N))
        f.write("    maximize trace(P*X)\n")
        f.write("    subject to\n")
        f.write("        X >= 0;\n")
        f.write("        diag(X) == ones(%s, 1);\n" % N)
        f.write("cvx_end\n")
        f.write("save('%s/%s.txt', 'X', '-ASCII');\n" % (DIR, prefix))
        f.write("exit;\n")


def write_output(sdp_results, densest_results, outfname, subgraphfile, densesubgraphfile):
    S, obj, obj_rounded = sdp_results
    D, density = densest_results

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
            #f.write(str(n / float(len(G))) + ',')
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
    print "Returning subgraph with density", density
    n = len(D)
    if 'weight' in S.edges_iter(data=True).next()[2]:
        e = sum(data['weight'] for u, v, data in S.edges_iter(data=True))
    else:
        e = D.number_of_edges()
    with open(outfname, 'a') as f:
        if n > 0:
            f.write(str(n) + ',')
            f.write(str(D.number_of_edges()) + ',')
            #f.write(str(n / float(len(G))) + ',')
            if n > 1:
                f.write(str(2. * e / (n * (n - 1))) + ',')
            else:
                f.write(str(0) + ',')
            if nx.is_connected(D):
                f.write(str(nx.diameter(D)) + ',')
            else:
                f.write('inf,')
            if n > 2:
                f.write(str(2. * sum(i for i in nx.triangles(D).itervalues()) / (n * (n - 1) * (n - 2))) + ',')
            else:
                f.write(str(0) + ',')
            f.write(str(obj_rounded) + ',')
            f.write(str(obj) + '\n')
        else:
            f.write("0,0,0,0,0,0,0,")
            f.write("%s\n" % obj)
    nx.write_weighted_edgelist(D, densesubgraphfile)


def main():
    egodir = sys.argv[1]
    outfname = sys.argv[2]
    subgraphfile = sys.argv[3]
    densesubgraphfile = sys.argv[4]
    best_S, best_obj, best_obj_rounded = nx.Graph(), 0, 0
    upper_bound = 0
    best_D, best_density = nx.Graph(), 0
    dirname = os.path.split(egodir.strip('/'))[-1]
    size_threshold = 5
    sdp_threshold = 2000 # nodes

    times = []

    if not os.path.exists(DIR):
        os.makedirs(DIR)
    # keep statistics on how many subgraphs we are able to prune with S.O.E (sum of edges)
    count = 0
    count_pruned = 0
    for graphfile in os.listdir(egodir):
        sum_edges = 0
        count += 1
        # load graph
        G = nx.Graph()
        with open(os.path.join(egodir, graphfile)) as f:
            for line in f:
                tokens = line.strip().split()
                u = int(tokens[0])
                v = int(tokens[1])
                w = float(tokens[2])
                G.add_edge(u, v, weight=w)
                sum_edges += w
        # S.O.E. Pruning. Check the number of edges before loading the graph
        if sum_edges < upper_bound:
            count_pruned += 1
            continue
        start = time.time()
        print "Processing node %s" % count
        print "%s nodes were pruned" % count_pruned
        # SDP solver is slow for graphs with more than a few thousand nodes
        # This part of the algorithm should be parallelized
        # For now, we just skip large ego networks
        if len(G) > sdp_threshold:
            continue
        print "Size of the ego network:", len(G)
        A = nx.to_numpy_matrix(G)
        w, d = oqc_sdp._make_coefficient_matrices(A)
        P = np.matrix(w - alpha * d)
        filename = os.path.split(graphfile)[1]
        # make matlab input
        prefix = dirname + "_" + os.path.splitext(filename)[0]
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
        # update best seen
        update = False
        if (obj_rounded > best_obj_rounded or
            (obj_rounded == best_obj_rounded and obj > best_obj)):
            # recover best subgraph
            best_S, best_obj, best_obj_rounded = S, obj, obj_rounded
            # update pruning bound
            upper_bound = obj
            update = True
        n_choose_2 = len(nodeset) * (len(nodeset) - 1) / 2
        density = (obj_rounded + (alpha * n_choose_2)) / n_choose_2
        # Even if the OQC score doesn't improve, we may still find a subgraph of highest density,
        # and we also want to update in this case
        if len(nodeset) > size_threshold and (density > best_density or
                (density == best_density and len(nodeset) > len(best_D))):
            best_density = density
            nodes = G.nodes()
            S = G.subgraph([nodes[i - 1] for i in nodeset])
            best_D, best_density = S, density
            update = True
        if update:
            write_output((best_S, best_obj, best_obj_rounded),
                         (best_D, best_density), outfname, subgraphfile, densesubgraphfile)
        end = time.time()
        times.append(end - start)
    print "%s nodes were pruned" % count_pruned
    print "Average time:", np.mean(times)

if __name__ == '__main__':
    main()
