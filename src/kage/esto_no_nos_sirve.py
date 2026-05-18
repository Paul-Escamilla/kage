import networkx as nx
import matplotlib.pyplot as plt

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

        for i in range(1, int((g - 1) / 2)):
            nodos_acumulados = nodos + k*(k - 1)**i        # Parecido a cuando g es par pero k en vez de 2
            for j in friends_down:
                for l in range(k-1):
                    G.add_edge(j, next_friend)
                    next_friend += 1
            friends_down = [amigos for amigos in range(nodos, nodos_acumulados)]
            nodos = nodos_acumulados
        G.add_nodes_from(range(nodos))     # Añade los respectivos nodos para cada nivel del arbol
    key_nodes = friends_down
    return G, key_nodes


def kage_construction_backing_track(k, g, G = None, key_nodes = None):
    if G == None:
        G, key_nodes = base_of_cage(k, g)
    if nx.is_regular(G):
        yield  G.copy()
        return
     #deficit_total = sum(k - G.degree(node) for node in G.nodes)                     #Pruning    comprueba si es posible que el grafo se vuelva k regular
    #if deficit_total % 2 != 0:                                                       # Si los nodos con grado<k  requieren un numero impar de nodos mas
       # return   # imposible alcanzar regularidad                                      para k entonces es imposible llegar a completar y cortamos tal rama
    else: 
        u = key_nodes[-1]
        #u = min(key_nodes, key=lambda x: G.degree(x))   # el de menor grado
        candidatos = [v for v in key_nodes if not G.has_edge(u, v)]             #Añadi una podada (pruning)   (posibles cambios)
        #candidatos.sort(key=lambda v: G.degree(v))   # orden ascendente de grado
        for v in candidatos:
            if nx.shortest_path_length(G, u, v) >= g - 1:
                G.add_edge(u, v)
                if k == G.degree(u):
                    key_nodes.remove(u)
                yield from kage_construction_backing_track(k, g, G, key_nodes)
                G.remove_edge(u, v)
                if k == (G.degree(u) - 1):
                    key_nodes.append(u)

def cage_add_node(k, g, G, key_nodes):
    while not nx.is_regular(G):
        add_node(k, g, G, key_nodes)
        conectar = kage_construction_backing_track(k, g, G.copy(), key_nodes.copy())
        try:
            return next(conectar).edges() 
        except StopIteration:
            pass

def add_node(k, g, G, key_nodes):
    nuevo = G.number_of_nodes()
    G.add_node(nuevo)
    G.add_edge(nuevo - 1, nuevo)
    if k % 2 == 1:
        nuevo2 = nuevo + 1                 # Agregar otro nodo y conectarlo con el anterior
        G.add_node(nuevo2)
        G.add_edge(nuevo, nuevo2)
    key_nodes.append(nuevo)
    key_nodes.append(nuevo2)
    return G, key_nodes

def jaula(k, g):
    isomorfas = kage_construction_backing_track(k, g)
    try:
        return next(isomorfas).edges()
    except StopIteration:
        G, key_nodes = base_of_cage(k, g)
        return cage_add_node(k, g, G, key_nodes)


def draw_kage(G):
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    ax = axes.flatten()
    opciones = {
        "node_color": "lightblue",
        "node_size": 400,
        "font_size": 10,
        "font_weight": "bold",
        "edge_color": "gray",
        "alpha": 0.8
    }
    layouts = [
        (nx.kamada_kawai_layout, "Kamada-Kawai (Energía)"),
        (nx.spectral_layout, "Espectral (Matrices)"),
        (lambda g: nx.spring_layout(g, k=0.8, iterations=100), "Spring Layout (Resortes)"),
        (nx.circular_layout, "Circular (Regularidad)")
    ]
    for i, (layout_func, title) in enumerate(layouts):
        pos = layout_func(G)
        nx.draw(G, pos, ax=ax[i], with_labels=True, **opciones)
        ax[i].set_title(title, fontsize=14)
    plt.tight_layout()
    plt.show()
    
print(jaula(3,7))