import networkx as nx

def base_of_cage(k, g):             # Se crea un funcion que estructura un arbol para distintos valores de k y g    
    G = nx.Graph()
    if g%2 == 0:            # if g%2 == 0 (Si g par)
        nodos = 2               # Condiciones iniciales
        friends_down = [0, 1]     # (friends_down son los ultimos nodos creados)
        next_friend = 2            # Next_friend ayuda a etiquetar los nuevos nodos (2,3,4,...)
        G.add_edge(0, 1)           # Representa la arista con la que empezamos (de 0 a 1)
        for i in range(1, int(g / 2)):        # Se usa hasta g/2 para no crear cuello mas pequeño (es bipartita)
            nodos_acumulados = nodos + 2*(k - 1)**i   # Los k - 1 se estan anidando a los nos ya existentes    
            for j in friends_down:
                for _ in range(k-1):
                    G.add_edge(j, next_friend)    # Para cada nodo existente se le añade una arista entre el y el nuevo amigo generado
                    next_friend += 1       # Etiqueta los nuevos nodos                 
            friends_down = [amigos for amigos in range(nodos, nodos_acumulados)] # Enlista los nodos actuales (las hojas del arbol)
            nodos = nodos_acumulados   
        G.add_nodes_from(range(nodos))  # Añade los respectivos nodos para cada nivel del arbol
    else:
        nodos = k + 1                              # Si k es impar, empezamos con un arbol de un nodo con k amigos
        friends_down = [i for i in range(1, k+1)]  # nodos actuales
        next_friend = k + 1                        # Desde ahi se empieza a etiquetar los nuevos nodos

        for i in range(1, k + 1):            # Corregir
            G.add_edge(0, i)

        for i in range(int((g - 1) / 2)):
            nodos_acumulados = nodos + k*(k - 1)**i        # Parecido a cuando g es par pero k en vez de 2
            for j in friends_down:
                for l in range(k-1):
                    G.add_edge(j, next_friend)
                    next_friend += 1
            friends_down = [amigos for amigos in range(nodos, nodos_acumulados)]
            nodos = nodos_acumulados
        G.add_nodes_from(range(nodos))     # Añade los respectivos nodos para cada nivel del arbol
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

def add_node(k, g, G): 
    nuevo_nodo = G.number_of_nodes()
    G.add_edge(nuevo_nodo - 1, nuevo_nodo)
    return G

def jaula(k, g):
    isomorfas = kage_construction_backing_track(k, g)
    try:
        return next(isomorfas).edges()
    except StopIteration:
        G = base_of_cage(k, g)
        return add_node(k, g, G)
