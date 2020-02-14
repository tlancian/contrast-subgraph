import networkx as nx
from greedy_oqc import greedyOQC, localSearchOQC
import sys
import time


def main():
    graphfile = sys.argv[1]
    outfname = sys.argv[2]
    subgraphfile = sys.argv[3]
    alpha = 1/3.

    print "Reading graph"
    G = nx.read_gml(graphfile)
    #G = nx.Graph()
    #with open(graphfile) as f:
    #    for i in xrange(4):
    #        f.readline()
    #    for line in f:
    #        tokens = line.strip().split('\t')
    #        G.add_edge(int(tokens[0]), int(tokens[1]))
    #G.remove_edges_from(G.selfloop_edges())
    #print len(G), G.number_of_edges()

    print "Running local search"
    start = time.time()
    if len(sys.argv) > 4:
        #H = nx.read_gml(sys.argv[4])
        #seed = nx.Graph()
        #for u, data in H.nodes_iter(data=True):
        #    data['label'] = int(data['label'])
        #for u, v, data in H.edges_iter(data=True):
        #    seed.add_edge(H.node[u]['label'], H.node[v]['label'])
        #S, obj = localSearchOQC(G, alpha, t_max=50, seed=seed)
        S, obj = localSearchOQC(G, alpha, t_max=50, seed=nx.read_gml(sys.argv[4]))
    else:
        S, obj = localSearchOQC(G, alpha, t_max=50)
    end = time.time()
    print "took %s seconds" % (end - start)

    nx.write_gml(S, subgraphfile)
    n = len(S)
    e = S.number_of_edges()
    header = "|S|,|E|,|S|/|V|,density,diameter,triangle density,OQC,time\n"
    with open(outfname, 'w') as f:
        if n > 0:
            f.write(header)
            f.write(str(n) + ',')
            f.write(str(e) + ',')
            f.write(str(n / float(len(G))) + ',')
            f.write(str(2. * e / (n * (n - 1))) + ',')
            if nx.is_connected(S):
                f.write(str(nx.diameter(S)) + ',')
            else:
                f.write('inf,')
            f.write(str( 2. * sum(i for i in nx.triangles(S).itervalues()) / (n * (n - 1) * (n - 2))) + ',')
            f.write(str(e - alpha * ((n * (n - 1)) / 2)) + ',')
            f.write(str(end - start) + '\n')
        else:
            f.write("0,0,0,0,0,0,0,%s\n" % (end - start))

    print "Running greedy"
    start = time.time()
    S, obj = greedyOQC(G, alpha)
    end = time.time()
    print "Took %s seconds" % (end - start)

    n = len(S)
    e = S.number_of_edges()
    with open(outfname, 'a') as f:
        if n > 0:
            f.write(str(n) + ',')
            f.write(str(e) + ',')
            f.write(str(n / float(len(G))) + ',')
            f.write(str(2. * e / (n * (n - 1))) + ',')
            if nx.is_connected(S):
                f.write(str(nx.diameter(S)) + ',')
            else:
                f.write('inf,')
            f.write(str( 2. * sum(i for i in nx.triangles(S).itervalues()) / (n * (n - 1) * (n - 2))) + ',')
            f.write(str(e - alpha * ((n * (n - 1)) / 2)) + ',')
            f.write(str(end - start) + '\n')
        else:
            f.write("0,0,0,0,0,0,0,%s\n" % (end - start))


if __name__ == "__main__":
    main()
