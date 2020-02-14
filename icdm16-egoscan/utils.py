import networkx as nx
import os
import random
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
import sys


def write_ego_graphs_to_dir(G, radius=1, max_size=1000000, outdir='./', fmt="gml"):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for node in G:
        S = nx.ego_graph(G, node, radius=radius)
        S.graph = {}
        if len(S) <= max_size:
            if fmt == "gml":
                nx.write_gml(S, os.path.join(outdir, "%s.gml" % node))
            elif fmt == "uel":
                with open(os.path.join(outdir, "%s.txt" % node), 'w') as f:
                    for u, v, data in S.edges_iter(data=True):
                        w = data['weight'] if 'weight' in data else 1
                        f.write("%s %s %s\n" % (u, v, w))
            else:
                raise Exception, "Unrecognized format '%s'" % fmt


def processNode(args):
    node, G, radius, max_size, outdir, fmt = args
    S = nx.ego_graph(G, node, radius=radius)
    S.graph = {}
    if len(S) <= max_size:
        if fmt == "gml":
            nx.write_gml(S, os.path.join(outdir, "%s.gml" % node))
        elif fmt == "uel":
            with open(os.path.join(outdir, "%s.txt" % node), 'w') as f:
                for u, v, data in S.edges_iter(data=True):
                    w = data['weight'] if 'weight' in data else 1
                    f.write("%s %s %s\n" % (u, v, w))
        else:
            raise Exception, "Unrecognized format '%s'" % fmt
    #print "Done with node", node


def write_ego_graphs_to_dir_parallel(G, radius=1, max_size=1000000, outdir='./', fmt="gml"):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)
    chunksize = (len(G) / (num_cores * 10)) + 1  # has to be integer
    pool.map(processNode, [(node, G, radius, max_size, outdir, fmt) for node in G],
             chunksize=chunksize)
    pool.close()
    pool.join()


def write_r1_ego_graphs_to_dir(G, max_size=1000000, outdir='./'):
    egos = {}
    i = 0
    for node in G:
        i += 1
        #if i % 1000 == 0:
        #    print "Processed %s nodes" % i
        if len(G[node]) < 3:
            continue
        S = {node}
        for n1 in G.neighbors_iter(node):
            S.add(n1)
        seen = False
        if len(S) > max_size:
            continue
        for v in S:
            if v in egos:
                S_other = egos[v]
                if S.issubset(S_other):
                    seen = True
                elif S_other.issubset(S):
                    del egos[v]
        if not seen:
            egos[node] = S
    print "Writing files"
    for node, S in egos.iteritems():
        with open(os.path.join(outdir, "%s.txt" % node), 'w') as f:
            for u in S:
                f.write("%s\n" % u)


def write_r1_ego_graphs_to_dir(G, alphas, outdir='./'):
    egos = {}
    i = 0
    for node in G:
        i += 1
        if len(G[node]) < 3:
            continue
        S = {node}
        for n1 in G.neighbors_iter(node):
            S.add(n1)
        seen = False
        if len(S) > max_size:
            continue
        for v in S:
            if v in egos:
                S_other = egos[v]
                if S.issubset(S_other):
                    seen = True
                elif S_other.issubset(S):
                    del egos[v]
        if not seen:
            egos[node] = S
    print "Writing files"
    for node, S in egos.iteritems():
        with open(os.path.join(outdir, "%s.txt" % node), 'w') as f:
            for u in S:
                f.write("%s\n" % u)


def write_r2_ego_graphs_to_dir(G, max_size=1000000, outdir='./'):
    egos = {}
    i = 0
    for node in G:
        i += 1
        #if i % 1000 == 0:
        #    print "Processed %s nodes" % i
        if len(G[node]) < 3:
            continue
        S = {node}
        for n1 in G.neighbors_iter(node):
            S.add(n1)
            for n2 in G.neighbors_iter(n1):
                S.add(n2)
        seen = False
        if len(S) > max_size:
            continue
        for v in S:
            if v in egos:
                S_other = egos[v]
                if S.issubset(S_other):
                    seen = True
                elif S_other.issubset(S):
                    del egos[v]
        if not seen:
            egos[node] = S
    print "Writing files"
    for node, S in egos.iteritems():
        with open(os.path.join(outdir, "%s.txt" % node), 'w') as f:
            for u in S:
                f.write("%s\n" % u)


def weighted_oqc(G, alpha=1/3.):
    W = sum(data['weight'] for u, v, data in G.edges_iter(data=True))
    return W - alpha * ((len(G) * (len(G) - 1)) / 2.)


def oqc(G, alpha=1/3.):
    return G.number_of_edges() - alpha * ((len(G) * (len(G) - 1)) / 2.)


def density(G):
    W = sum(data['weight'] for u, v, data in G.edges_iter(data=True))
    return 2. * W / (len(G) * (len(G) - 1))


def triangle_density(G):
    assert(len(G.selfloop_edges()) == 0)
    W = 0
    for u in G:
        for v in G[u]:
            for w in G[v]:
                if w in G[u]:
                    W += G[u][w]['weight'] + G[u][v]['weight'] + G[v][w]['weight']
    W /= 3. # weight pf a triangle is average weight of edges
    return (2. * W) / (len(G) * (len(G) - 1) * (len(G) - 2))


def random_const_set(G, size, fname):
    nodes = G.nodes()
    Q = np.random.choice(nodes, size=size, replace=False)
    with open(fname, 'w') as f:
        for i in Q:
            f.write("%s\n" % i)
