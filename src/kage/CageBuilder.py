import networkx as nx
import copy
import matplotlib.pyplot as plt
import time

class CageBuilder:
    def __init__(self, k, g):
        self.k = k
        self.g = g
        self.G = self._base_of_cage(k, g)
        self.M = copy.deepcopy(self.G)
        self.exceso = 0 # Initialize 'exceso' here

        self.caminos_fijos = {n: set(nx.shortest_path(self.M, source=n, target=0))
                             for n in self.M.nodes()}

        self.parent_map = {}
        for u, v in self.M.edges():
            p, h = (u, v) if u < v else (v, u)
            self.parent_map[h] = p

    # Constructor del arbol de los vertices minimos necesarios
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

    # Generando las nuevas ramas a partir de cada hoja previa
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

    # Determina si al conectar 2 vertices no produce un ciclo menor a g
    def calcular_compatibles(self):
        # Todos los nodos que necesitan aristas (incluyendo los de exceso)
        necesitados = [n for n in self.G.nodes() if self.G.degree(n) < self.k and n != 0]
        compatibles = {n: [] for n in necesitados}

        for u in necesitados:
            cam_u = self.caminos_fijos.get(u, None)

    # Evita que se produzcan auto ciclos
            for v in necesitados:
                if u >= v: continue

                cam_v = self.caminos_fijos.get(v, None)

                # Caso A: Ambos son del árbol original (usamos intersección)
                if cam_u is not None and cam_v is not None:
                    if cam_u.intersection(cam_v) == {0}:
                        compatibles[u].append(v)
                        compatibles[v].append(u)

                # Caso B: Al menos uno es de exceso
                # No tienen camino fijo, así que son compatibles por defecto.
                # El radar de peligro en backtrack hará el trabajo sucio.
                else:
                    compatibles[u].append(v)
                    compatibles[v].append(u)
        return compatibles

    # Agrega aristas recursivamente a vertices disponibles
    def _backtrack(self, compatibles):
    # Toma vertices que no tienen grado k
        necesitados = [n for n in self.G.nodes() if self.G.degree(n) < self.k and n != 0]
        if not necesitados:
            return True

        # Heurística MRV: Nodo con mayor grado (más cerca de completarse)
        u = max(necesitados, key=lambda n: self.G.degree(n))
    # Detecta si al conectar nodos se producen ciclos menores a g
        peligro = nx.single_source_shortest_path_length(self.G, source=u, cutoff=self.g-2)

    # Conjuntos de conexiones equivalentes
        hermanas_probadas = set()

        for v in compatibles.get(u, []):
    # Filtra a los vertices eliminando los que producen ciclos menores a g
            if self.G.degree(v) >= self.k or self.G.has_edge(u, v) or v in peligro:
                continue

            # --- PODA DE SIMETRÍA ---
            firma_v = (self.parent_map.get(v, None), self.G.degree(v))
            if firma_v in hermanas_probadas:
                continue

            # --- INTENTO DE CONEXIÓN ---
            self.G.add_edge(u, v)

            # --- PODA LOOK-AHEAD (Cota de Candidatos) ---
            # Si después de esta arista, algún nodo se queda sin suficientes
            # candidatos para completar su grado k, abortamos inmediatamente.
            posible = True
            for nodo in necesitados:
                grado_faltante = self.k - self.G.degree(nodo)
                if grado_faltante > 0:
                    # Contamos cuántos candidatos reales le quedan a este nodo
                    cands_reales = 0
                    # Usamos una versión ligera de la validación
    # Verificacion de candidatos validos restantes
                    for c in compatibles.get(nodo, []):
                        if self.G.degree(c) < self.k and not self.G.has_edge(nodo, c):
                            cands_reales += 1

    # Si no hay suficientes candidatos requiere de mayor cantidad de vertices (Pasa a agregar vertices)
                    if cands_reales < grado_faltante:
                        posible = False
                        break

    # Continua con la recursión
            if posible and self._backtrack(compatibles):
                return True

            # Deshacer si no funcionó
            self.G.remove_edge(u, v)
            hermanas_probadas.add(firma_v)

        return False

    def add_vertices_exceso(self):
        # Determinamos cuántos nodos añadir (puedes ajustar este paso)
        cantidad = 2 if self.k % 2 != 0 else 1
        proximo_id = max(self.G.nodes()) + 1
        nuevos = [] # Initialize 'nuevos' list

        for i in range(cantidad):
            nuevo_nodo = proximo_id + i
            self.G.add_node(nuevo_nodo)
            nuevos.append(nuevo_nodo) # Populate 'nuevos' list
            # IMPORTANTE: No añadimos aristas aquí.
            # El nodo entra "limpio" para que el backtracking tenga libertad total.

    # Si se agregan 2 vertices se conectan entre si
        if len(nuevos) == 2:
            self.G.add_edge(nuevos[0], nuevos[1]) # Add edge between new nodes if two

        # Anclaje al árbol (Puente entre ramas lejanas) - This part was moved from the solve method
        hojas_m = [n for n in self.M.nodes() if self.M.degree(n) == 1]
        for i, extra in enumerate(nuevos):
            if hojas_m:
                # Sumamos el exceso actual para que en cada iteración de solve()
                # se empiece desde un punto diferente de la lista de hojas.
                salto = (i * (len(hojas_m) // 2)) + self.exceso
                target = hojas_m[salto % len(hojas_m)]
                self.G.add_edge(extra, target)

        self.exceso += cantidad

    def solve(self, max_iter=10):
        print(f"Buscando Jaula ({self.k}, {self.g})...")
        for i in range(max_iter):
            print(f"Intento {i+1}: Nodos={len(self.G.nodes())}, Exceso={self.exceso}")
            compatibles = self.calcular_compatibles()

            start = time.time()

    # Intenta completar la grafica
            if self._backtrack(compatibles):
                print(f"¡ÉXITO! Tiempo: {time.time()-start:.2f}s")
                return self.G

    # Agrega vertices extra cuando no es posible la jaula con solo el arbol base
            print(f"Fallo. Añadiendo exceso...")
            self.add_vertices_exceso()
        return self.G

# Dibuja la grafica mediante layouts que permiten distinguir las conexiones
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
