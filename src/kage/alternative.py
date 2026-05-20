import networkx as nx
from collections import deque
from itertools import combinations


# ============================================================
# COTA DE MOORE
# ============================================================

def moore_bound(k, g):
    """
    Calcula la cota inferior de Moore para una (k,g)-jaula.
    """

    if g % 2 == 1:
        # g impar
        r = (g - 3) // 2
        total = 1

        for i in range(r + 1):
            if i == 0:
                total += k
            else:
                total += k * (k - 1) ** i

        return total

    else:
        # g par
        r = g // 2 - 1
        total = 0

        for i in range(r + 1):
            total += (k - 1) ** i

        return 2 * total


# ============================================================
# BFS PARA VERIFICAR EL CUELLO
# ============================================================

def edge_is_safe(G, u, v, g):
    """
    Verifica si agregar la arista (u,v)
    crea un ciclo de longitud menor que g.

    Se hace BFS desde u hasta profundidad g-2.
    """

    if u == v:
        return False

    if G.has_edge(u, v):
        return False

    visited = {u}
    queue = deque([(u, 0)])

    while queue:

        node, dist = queue.popleft()

        if dist >= g - 2:
            continue

        for neighbor in G.neighbors(node):

            if neighbor == v:
                return False

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return True


# ============================================================
# VERIFICAR SI EL GRAFO ES k-REGULAR
# ============================================================

def is_k_regular(G, k):
    """
    Verifica si todos los vértices tienen grado k.
    """

    return all(deg == k for _, deg in G.degree())


# ============================================================
# SELECCIÓN RECURSIVA DE VECINOS
# ============================================================

def select_edges(G, u, candidates, needed, idx, chosen, k, g):
    """
    Selecciona exactamente 'needed' vértices
    de la lista de candidatos.
    """

    # Caso base: ya elegimos suficientes vecinos
    if len(chosen) == needed:

        # Agregar aristas
        added_edges = []

        for v in chosen:
            G.add_edge(u, v)
            added_edges.append((u, v))

        # Continuar backtracking
        if backtrack(G, k, g, u + 1):
            return True

        # Retroceder
        G.remove_edges_from(added_edges)

        return False

    # No hay más candidatos
    if idx >= len(candidates):
        return False

    v = candidates[idx]

    # ========================================================
    # OPCIÓN 1: incluir v
    # ========================================================

    if edge_is_safe(G, u, v, g):

        G.add_edge(u, v)

        if select_edges(
            G,
            u,
            candidates,
            needed,
            idx + 1,
            chosen + [v],
            k,
            g
        ):
            return True

        G.remove_edge(u, v)

    # ========================================================
    # OPCIÓN 2: no incluir v
    # ========================================================

    return select_edges(
        G,
        u,
        candidates,
        needed,
        idx + 1,
        chosen,
        k,
        g
    )


# ============================================================
# BACKTRACK PRINCIPAL
# ============================================================

def backtrack(G, k, g, u=0):
    """
    Construcción recursiva del grafo.
    """

    n = G.number_of_nodes()

    # ========================================================
    # TODOS LOS VÉRTICES PROCESADOS
    # ========================================================

    if u >= n:
        return is_k_regular(G, k)

    # ========================================================
    # SI EL VÉRTICE YA TIENE GRADO k
    # ========================================================

    if G.degree(u) == k:
        return backtrack(G, k, g, u + 1)

    needed = k - G.degree(u)

    # ========================================================
    # GENERAR CANDIDATOS
    # ========================================================

    candidates = []

    for v in range(u + 1, n):

        if G.degree(v) >= k:
            continue

        if edge_is_safe(G, u, v, g):
            candidates.append(v)

    # Poda
    if len(candidates) < needed:
        return False

    # ========================================================
    # SELECCIONAR VECINOS
    # ========================================================

    return select_edges(
        G,
        u,
        candidates,
        needed,
        0,
        [],
        k,
        g
    )


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def build_cage(k, g, max_n=30):
    """
    Busca una (k,g)-jaula incrementando n
    desde la cota de Moore.
    """

    n0 = moore_bound(k, g)

    for n in range(n0, max_n + 1):

        print(f"Intentando n = {n}")

        G = nx.Graph()
        G.add_nodes_from(range(n))

        success = backtrack(G, k, g)

        if success:

            print(f"\nJaula encontrada con n = {n}")
            return G

    return None


# ============================================================
# VISUALIZACIÓN
# ============================================================

def draw_graph(G):
    """
    Dibuja el grafo usando NetworkX.
    """

    import matplotlib.pyplot as plt

    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700,
        font_size=12
    )

    plt.show()