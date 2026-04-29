import networkx as nx

def base_of_cage(k, g):
    G = nx.Graph()
    if g%2 == 0:
        nodos = 2
        friends_down = [0, 1]
        next_friend = 2
        G.add_edge(0, 1)
        for i in range(1, int(g / 2)):
            nodos_nuevos = nodos + 2*(k - 1)**i
            for j in friends_down:
                for l in range(k-1):
                    G.add_edge(j, next_friend)
                    next_friend += 1
            friends_down = [amigos for amigos in range(nodos, nodos_nuevos)]
            nodos = nodos_nuevos   
        G.add_nodes_from(range(nodos))
    else:
        nodos = 1
        friends_down = [0]
        next_friend = 1
        
        for i in range(int((g - 1) / 2)):
            nodos_nuevos = nodos + k*(k - 1)**i
            for j in friends_down:
                for l in range(k-1):
                    G.add_edge(j, next_friend)
                    next_friend += 1
                if i == 0:
                    G.add_edge(j, next_friend)
                    next_friend +=1
            friends_down = [amigos for amigos in range(nodos, nodos_nuevos)]
            nodos = nodos_nuevos
        G.add_nodes_from(range(nodos))
    return G


def kage_construction_backing_track(k, g, G = None):
    if G == None:
        G = base_of_cage(k, g)
    if nx.is_regular(G):
        yield  G.copy()
        return
    else:
        key_nodes = [node for node in G.nodes if k != G.degree(node)]
        u = key_nodes[0]
        candidatos = [v for v in key_nodes if not G.has_edge(u, v)]
        for v in candidatos:
            if nx.shortest_path_length(G, u, v) >= g - 1:
                G.add_edge(u, v)
                yield from kage_construction_backing_track(k, g, G)
                G.remove_edge(u, v)