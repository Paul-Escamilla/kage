import networkx as nx
import numpy as np

def base_tree(k, g):
    G = nx.Graph()

    # label dictionary
    etiquetas = {}

    # Case g == 2*n
    if g % 2 == 0:
        nodos = 2
        friends_down = [0, 1]
        next_friend = 2

        # raíces
        G.add_edge(0, 1)
        etiquetas[0] = [0]
        etiquetas[1] = [1]

        for _ in range(1, g // 2):
            nuevos = []

            for i in friends_down:
                for idx in range(k - 1):
                    G.add_edge(i, next_friend)

                    # label construction
                    etiquetas[next_friend] = etiquetas[i] + [idx]

                    nuevos.append(next_friend)
                    next_friend += 1

            friends_down = nuevos
            nodos = next_friend

    # Case g == 2*n + 1
    else:
        nodos = k + 1
        friends_down = [i for i in range(1, k + 1)]
        next_friend = k + 1

        etiquetas[0] = [0]

        # frist level
        for i in range(1, k + 1):
            G.add_edge(0, i)
            etiquetas[i] = [0, i - 1]

        for i in range((g - 1) // 2 - 1):
            nuevos = []

            for j in friends_down:
                for idx in range(k - 1):
                    G.add_edge(j, next_friend)

                    etiquetas[next_friend] = etiquetas[j] + [idx]

                    nuevos.append(next_friend)
                    next_friend += 1

            friends_down = nuevos
            nodos = next_friend

    # Save labels
    nx.set_node_attributes(G, etiquetas, "etiqueta")

    return G

def obtener_hojas(G):
    # create a list of leafs
    return [n for n in G.nodes() if G.degree(n) == 1]

# SEGUNDA ENTRADA DE LA ETIQUETA
def segunda_entrada(etiquetas, v):
    et = etiquetas[v]
    if len(et) < 2:
        return None
    else:
        return et[1]

# DISTANCIAS DESDE UN NODO
def calcular_distancias(G, origen):
    """
    Calcula todas las distancias más cortas desde un nodo origen.
    """
    return nx.single_source_shortest_path_length(G, origen)

# VERIFICAR SI SE PUEDE AGREGAR UNA ARISTA
def es_valida(distancias, v, g):
    """
    Verifica si la distancia cumple la condición de girth.
    """
    d = distancias.get(v, float("inf"))
    return d >= g - 1

# FILTRAR CANDIDATOS POR ETIQUETA
def filtrar_candidatos(hojas, hoja_base, etiquetas):
    """
    Filtra nodos candidatos que:
    - No sean la hoja base
    - Tengan distinta segunda etiqueta
    - No repitan segunda etiqueta
    """
    s_base = segunda_entrada(etiquetas, hoja_base)
    usados = set()
    candidatos = []

    for v in hojas:
        if v == hoja_base:
            continue

        s = segunda_entrada(etiquetas, v)

        if s != s_base and s not in usados:
            candidatos.append(v)
            usados.add(s)

    return candidatos

# CONECTAR UNA HOJA CON RESTRICCIONES
def conectar_hoja(G, hoja, hojas, etiquetas, g, limite=None):
    """
    Conecta una hoja con otras hojas válidas.
    
    Parámetros:
    - limite: número máximo de conexiones (None = sin límite)
    """
    distancias = calcular_distancias(G, hoja)
    candidatos = filtrar_candidatos(hojas, hoja, etiquetas)

    count = 0

    for v in candidatos:
        if es_valida(distancias, v, g):
            G.add_edge(hoja, v)
            count += 1

        if limite is not None and count >= limite:
            break

# FUNCIÓN PRINCIPAL
def conectar_hojas_girth(G, k, g):
    """
    Conecta hojas de un grafo respetando restricciones de girth
    y etiquetas.
    """
    etiquetas = nx.get_node_attributes(G, "etiqueta")
    hojas = obtener_hojas(G)

    if not hojas:
        return G

    # PRIMERA HOJA (CONTROLADA)
    conectar_hoja(G, hojas[0], hojas, etiquetas, g, limite=k - 1)

    # RESTO DE HOJAS
    for hoja in hojas[1:]:
        conectar_hoja(G, hoja, hojas, etiquetas, g)

    return G