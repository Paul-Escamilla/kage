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