import utils
import sys
import networkx as nx


def main():
    graphfile = sys.argv[1]
    outdir = sys.argv[2]
    radius = 1
    max_size = 1000000
    G = nx.Graph()
    with open(graphfile) as f:
        for line in f:
            tokens = line.strip().split()
            u = int(tokens[0])
            v = int(tokens[1])
            w = float(tokens[2])
            G.add_edge(u, v, weight=w)
    utils.write_ego_graphs_to_dir(G, radius, max_size, outdir, 'uel')


if __name__ == "__main__":
    main()
