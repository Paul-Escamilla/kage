import networkx as nx
import copy
import matplotlib.pyplot as plt
import time

class CageBuilder:
    def __init__(self, k, g):
        if k < 2:
            raise ValueError("El grado (k) debe ser al menos 2.")
        if g < 3:
            raise ValueError("El cuello (g) debe ser al menos 3.")
        self.k = k
        self.g = g
        self.G = self._base_of_cage(k, g)
        self.M = copy.deepcopy(self.G)
        self.exceso = 0     # Initialize "exceso" counter

        self.caminos_fijos = {n: set(nx.shortest_path(self.M, source=n, target=0))
                             for n in self.M.nodes()}

        self.parent_map = {}
        for u, v in self.M.edges():
            p, h = (u, v) if u < v else (v, u)
            self.parent_map[h] = p

    # Build the minimal base tree required for the (k, g)-cage
    def _base_of_cage(self, k, g):
        G = nx.Graph()

        if g % 2 == 0:
            G.add_edge(0, 1)
            hojas = [0, 1]
            capas = (g - 2) // 2
        else:
            G.add_node(0)
            hojas = [0]
            capas = (g - 1) // 2

        # Generate new branches from each previous leaf
        for _ in range(capas):
            proximas = []

            for padre in hojas:
                num_hijos = self.k if (g % 2 != 0 and padre == 0) else self.k - 1

                for _ in range(num_hijos):
                    hijo = len(G.nodes())
                    G.add_edge(padre, hijo)
                    proximas.append(hijo)

            hojas = proximas
        return G

    # Determine compatible leaf pairs that do not generate
    # cycles smaller than the target girth g
    def calcular_compatibles(self):

        necesitados = [n for n in self.G.nodes() if self.G.degree(n) < self.k and n != 0]

        compatibles = {n: [] for n in necesitados}

        for u in necesitados:
            for v in necesitados:

                # Avoid duplicate pairs and self-connections
                if u >= v:
                    continue

                compatibles[u].append(v)
                compatibles[v].append(u)

        return compatibles

    # Recursive backtracking edge construction
    def _backtrack(self, compatibles):

        # Leaves that have not yet reached degree k
        necesitados = [n for n in self.G.nodes() if self.G.degree(n) < self.k and n != 0]
        if not necesitados:
            return True

        # MRV heuristic:
        # Select the leaf with the highest current degree
        u = max(necesitados, key=lambda n: self.G.degree(n))

        # Detect dangerous connections that would create
        # cycles smaller than g
        peligro = nx.single_source_shortest_path_length(self.G, source=u, cutoff=self.g-2)

        # Store already-tested equivalent configurations
        hermanas_probadas = set()

        for v in compatibles.get(u, []):

            # Filter invalid candidate leaves
            if self.G.degree(v) >= self.k or self.G.has_edge(u, v) or v in peligro:
                continue

            # Symmetry pruning
            firma_v = (self.parent_map.get(v, None), self.G.degree(v))

            if firma_v in hermanas_probadas:
                continue

            # Attempt connection
            self.G.add_edge(u, v)

            # Look-ahead pruning:
            # Abort immediately if any leaf loses enough
            # candidates to complete degree k
            posible = True

            for nodo in necesitados:
                grado_faltante = self.k - self.G.degree(nodo)

                if grado_faltante > 0:
                    # Count remaining valid candidates
                    cands_reales = 0

                    # Lightweight validation pass
                    # for remaining compatible leaves
                    for c in compatibles.get(nodo, []):
                        if self.G.degree(c) < self.k and not self.G.has_edge(nodo, c):
                            cands_reales += 1

                    # If insufficient candidates remain,
                    # additional excess leaves are required
                    if cands_reales < grado_faltante:
                        posible = False
                        break

            # Continue recursive exploration
            if posible and self._backtrack(compatibles):
                return True

            # Undo failed connection attempt
            self.G.remove_edge(u, v)
            hermanas_probadas.add(firma_v)

        return False

    def add_vertices_exceso(self):

        # Determine how many excess leaves must be added
        cantidad = 2 if self.k % 2 != 0 else 1
        proximo_id = max(self.G.nodes()) + 1
        nuevos = []     # Store newly created excess leaves

        for i in range(cantidad):
            nuevo_nodo = proximo_id + i
            self.G.add_node(nuevo_nodo)
            nuevos.append(nuevo_nodo)
            # The new leaf starts "clean" so backtracking

        # If two excess leaves are added,
        # connect them together
        if len(nuevos) == 2:
            self.G.add_edge(nuevos[0], nuevos[1])

        # Tree anchoring:
        # Create edges between distant branches
        hojas_m = [n for n in self.M.nodes() if self.M.degree(n) == 1]
        for i, extra in enumerate(nuevos):
            if hojas_m:

                # Offset using the current exceso counter so that
                # each solve() iteration starts from a different
                # region of the leaf list
                salto = (i * (len(hojas_m) // 2)) + self.exceso
                target = hojas_m[salto % len(hojas_m)]
                self.G.add_edge(extra, target)

        self.exceso += cantidad

    # Main function for cage creation 
    def solve(self, max_iter=10):
        print(f"Construyendo Jaula ({self.k}, {self.g})...")

        for i in range(max_iter):
            print(f"Iteración {i+1}: Vertices={len(self.G.nodes())}, Vertices extra={self.exceso}")
            compatibles = self.calcular_compatibles()

            # Start generation timer
            start = time.time()

            # Attempt graph completion
            if self._backtrack(compatibles):
                print(f"¡ÉXITO! Tiempo de construcción: {time.time()-start:.2f}s")
                return self.G

            # Add excess leaves when the base tree alone
            # cannot produce a valid cage
            print(f"Fallo. Añadiendo vertices extras...")
            self.add_vertices_exceso()
        return self.G

    # Draw the graph using multiple layouts to better visualize
    # structural connections
    def draw_kage(self):
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
            pos = layout_func(self.G) # Changed G to self.G
            nx.draw(self.G, pos, ax=ax[i], with_labels=True, **opciones)
            ax[i].set_title(title, fontsize=14)
        plt.tight_layout()
        plt.show()

# Function for the user
def cage(k, g, max_iter=10):
    # Generate a (k, g)-cage graph.
    # Returns    networkx.Graph

    builder = CageBuilder(k, g)

    return builder.solve(max_iter=max_iter)

# Function to draw the graph as an object of networkx
def draw_kage(G):

    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    ax = axes.flatten()
    opciones = {
        "node_color": "lightblue",
        "node_size": 400,
        "font_size": 10,
        "font_weight": "bold",
        "edge_color": "black",
        "alpha": 0.8
    }

    layouts = [
        (nx.kamada_kawai_layout, "Kamada-Kawai"),
        (nx.spectral_layout, "Spectral"),
        (lambda g: nx.spring_layout(g, k=0.8, iterations=100), "Spring"),
        (nx.circular_layout, "Circular")
    ]

    for i, (layout_func, title) in enumerate(layouts):

        pos = layout_func(G)

        nx.draw(G, pos, ax=ax[i], with_labels=True, **opciones)

        ax[i].set_title(title, fontsize=14)

    plt.tight_layout()
    plt.show()