import networkx as nx


def find_seed(G):
    triangles = nx.triangles(G)
    degree = nx.degree(G)
    best_ratio = -1
    best_node = None
    for node in G:
        if degree[node] > 0:
            ratio = triangles[node] / float(degree[node])
            if ratio > best_ratio:
                best_ratio = ratio
                best_node = node
    best_ego = nx.ego_graph(G, best_node)
    return best_ego

    
def localSearchOQC(G, alpha, t_max=1000, seed=None):
    if seed is None:
        S = find_seed(G)
    else:
        S = seed
    weight = S.number_of_edges()
    N = float(len(S))
    oqc_score = weight - alpha * (N * (N - 1) / 2)
    b1 = True
    t = 1
    while b1 and t <= t_max:
        found1 = False
        b2 = True
        while b2:
            found2 = False
            for node in G:
                if node not in S:
                    new_weight = weight + sum(1 for neighbor in G.neighbors_iter(node) if neighbor in S)
                    new_oqc_score = new_weight - alpha * (N * (N + 1) / 2)
                    if new_oqc_score > oqc_score:
                        weight = new_weight
                        oqc_score = new_oqc_score
                        N += 1
                        S.add_node(node)
                        for neighbor in G.neighbors_iter(node):
                            if neighbor in S:
                                S.add_edge(node, neighbor)
                        found2 = True
                        #break
            b2 = found2
        if len(S) == 1:
            break
        for node in S.nodes():
            new_weight = weight - S.degree(node)
            new_oqc_score = new_weight - alpha * ((N - 1) * (N - 2) / 2)
            if new_oqc_score > oqc_score:
                weight = new_weight
                oqc_score = new_oqc_score
                N -= 1
                S.remove_node(node)
                found1 = True
                #break
        b1 = found1
        t += 1
    S_bar = G.subgraph([node for node in G if node not in S])
    oqc_score_bar = S_bar.number_of_edges() - alpha * (len(S_bar) * (len(S_bar) - 1) / 2)
    if oqc_score_bar > oqc_score:
        return S_bar, oqc_score_bar
    return S, oqc_score


def localSearchOQCConstrained(G, alpha, seed, t_max=1000):
    S = seed
    weight = S.number_of_edges()
    N = float(len(S))
    oqc_score = weight - alpha * (N * (N - 1) / 2)
    b1 = True
    t = 1
    while b1 and t <= t_max:
        found1 = False
        b2 = True
        while b2:
            found2 = False
            for node in G:
                if node not in S:
                    new_weight = weight + sum(1 for neighbor in G.neighbors_iter(node) if neighbor in S)
                    new_oqc_score = new_weight - alpha * (N * (N + 1) / 2)
                    if new_oqc_score > oqc_score:
                        weight = new_weight
                        oqc_score = new_oqc_score
                        N += 1
                        S.add_node(node)
                        for neighbor in G.neighbors_iter(node):
                            if neighbor in S:
                                S.add_edge(node, neighbor)
                        found2 = True
                        #break
            b2 = found2
        if len(S) == 1:
            break
        for node in S.nodes():
            if node in seed:
                continue
            new_weight = weight - S.degree(node)
            new_oqc_score = new_weight - alpha * ((N - 1) * (N - 2) / 2)
            if new_oqc_score > oqc_score:
                weight = new_weight
                oqc_score = new_oqc_score
                N -= 1
                S.remove_node(node)
                found1 = True
                #break
        b1 = found1
        t += 1
    S_bar = G.subgraph([node for node in G if node not in S])
    oqc_score_bar = S_bar.number_of_edges() - alpha * (len(S_bar) * (len(S_bar) - 1) / 2)
    if oqc_score_bar > oqc_score:
        return S_bar, oqc_score_bar
    return S, oqc_score


def localSearchOQCAlpha(G, alpha, t_max=1000, seed=None):
    if seed is None:
        S = find_seed(G)
    else:
        S = seed
    weight = S.number_of_edges()
    N = float(len(S))
    penalty = 0
    for u in S:
        for v in S:
            if u < v:
                penalty += alpha[(u, v)]
    oqc_score = weight - penalty
    b1 = True
    t = 1
    while b1 and t <= t_max:
        found1 = False
        b2 = True
        while b2:
            found2 = False
            for node in G:
                if node not in S:
                    new_weight = weight + sum(1 for neighbor in G.neighbors_iter(node) if neighbor in S)
                    new_penalty = penalty
                    for u in S:
                        if u < node:
                            new_penalty += alpha[(u, node)]
                        else:
                            new_penalty += alpha[(node, u)]
                    new_oqc_score = new_weight - new_penalty
                    if new_oqc_score > oqc_score:
                        weight = new_weight
                        oqc_score = new_oqc_score
                        N += 1
                        S.add_node(node)
                        for neighbor in G.neighbors_iter(node):
                            if neighbor in S:
                                S.add_edge(node, neighbor)
                        found2 = True
                        #break
            b2 = found2
        if len(S) == 1:
            break
        for node in S.nodes():
            new_weight = weight - S.degree(node)
            new_penalty = penalty
            for u in S:
                if u < node:
                    penalty -= alpha[(u, node)]
                elif u > node:
                    penalty -= alpha[(node, u)]
            new_oqc_score = new_weight - new_penalty
            if new_oqc_score > oqc_score:
                weight = new_weight
                oqc_score = new_oqc_score
                N -= 1
                S.remove_node(node)
                found1 = True
                #break
        b1 = found1
        t += 1
    S_bar = G.subgraph([node for node in G if node not in S])
    S_bar_penalty = 0
    for u in S_bar:
        for v in S_bar:
            if u < v:
                S_bar_penalty += alpha[(u, v)]
    oqc_score_bar = S_bar.number_of_edges() - S_bar_penalty
    if oqc_score_bar > oqc_score:
        return S_bar, oqc_score_bar
    return S, oqc_score


def greedyOQC(G, alpha):
    
    E = G.number_of_edges()
    N = G.number_of_nodes()
    best_score = 0.0
    best_iter = 0

    # trivial case, empty graph
    if E == 0:
        return G

    nodes_by_degree = {i: dict() for i in xrange(len(G))}
    degree_by_node = {}
    order = []
    neighbors = {}

    for node in G:
        deg = G.degree(node)
        nodes_by_degree[deg][node] = 1
        degree_by_node[node] = deg
        neighbors[node] = {neighbor: 1 for neighbor in G.neighbors_iter(node)}

    min_deg = 0
    while not nodes_by_degree[min_deg]:
        min_deg += 1

    for it in xrange(N - 1):
        # update best subgraph
        score = E - (alpha * (N * (N - 1) / 2.))
        if best_score <= score:
            best_score = score
            best_iter = it
        # pick a node with minimum degree for deletion
        min_deg_node = nodes_by_degree[min_deg].iterkeys().next()
        order.append(min_deg_node)
        del nodes_by_degree[min_deg][min_deg_node]
        E -= min_deg
        N -= 1
        # update neighbors
        # decrease the degree of all neighbors of min_deg_node
        # by one
        for neighbor in neighbors[min_deg_node]:
            del nodes_by_degree[degree_by_node[neighbor]][neighbor]
            degree_by_node[neighbor] -= 1
            nodes_by_degree[degree_by_node[neighbor]][neighbor] = 1
            del neighbors[neighbor][min_deg_node]

        if min_deg > 0 and nodes_by_degree[min_deg - 1]:
            min_deg -= 1
        else:
            while not nodes_by_degree[min_deg]:
                min_deg += 1

    S = nx.Graph()
    to_ignore = set(order[:best_iter])
    for u, v in G.edges_iter():
        if u not in to_ignore and v not in to_ignore:
            S.add_edge(u, v)
    return S, best_score


def find_seed_negative(G):
    best_ego = nx.ego_graph(G, G.node.iterkeys().next())
    best_density = sum(data['weight'] for u, v, data in best_ego.edges_iter(data=True)) / float(len(best_ego))
    for node in G:
        ego = nx.ego_graph(G, node)
        density = sum(data['weight'] for u, v, data in ego.edges_iter(data=True)) / float(len(ego))
        if density > best_density:
            best_density = density
            best_ego = ego
    return best_ego


def localSearchNegativeOQC(G, alpha, t_max=1000, seed=None):
    all_negative = True
    for u, v, data in G.edges_iter(data=True):
        if data['weight'] > 0:
            all_negative = False
            break
    if all_negative:
        S = G.subgraph(G.node.iterkeys().next())
        return S, 0.
    
    if seed is None:
        S = find_seed_negative(G)
    else:
        S = seed
    weight = sum(data['weight'] for u, v, data in S.edges_iter(data=True))
    N = float(len(S))
    oqc_score = weight - alpha * (N * (N - 1) / 2)
    b1 = True
    t = 1
    while b1 and t <= t_max:
        found1 = False
        b2 = True
        while b2:
            found2 = False
            for node in G:
                if node not in S:
                    new_weight = weight + sum(G[node][neighbor]['weight'] 
                                              for neighbor in G.neighbors_iter(node) if neighbor in S)
                    new_oqc_score = new_weight - alpha * (N * (N + 1) / 2)
                    if new_oqc_score > oqc_score:
                        weight = new_weight
                        oqc_score = new_oqc_score
                        N += 1
                        S.add_node(node)
                        for neighbor in G.neighbors_iter(node):
                            if neighbor in S:
                                S.add_edge(node, neighbor, weight=G[node][neighbor]['weight'])
                        found2 = True
                        #break
            b2 = found2
        if len(S) == 1:
            break
        for node in S.nodes():
            new_weight = weight - sum(S[node][neighbor]['weight'] for neighbor in S.neighbors_iter(node))
            new_oqc_score = new_weight - alpha * ((N - 1) * (N - 2) / 2)
            if new_oqc_score > oqc_score:
                weight = new_weight
                oqc_score = new_oqc_score
                N -= 1
                S.remove_node(node)
                found1 = True
                #break
        b1 = found1
        t += 1
    S_bar = G.subgraph([node for node in G if node not in S])
    oqc_score_bar = (sum(data['weight'] for u, v, data in S_bar.edges_iter(data=True)) - 
                     alpha * (len(S_bar) * (len(S_bar) - 1) / 2))
    if oqc_score_bar > oqc_score:
        return S_bar, oqc_score_bar
    return S, oqc_score
