import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from kage.CageBuilder import CageBuilder
import networkx as nx
import matplotlib.pyplot as plt

def guardar_grafo(grafo, nombre_archivo, k, g):
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(grafo, seed=42)  # No requiere scipy
    nx.draw(grafo, pos, with_labels=False, node_size=50, node_color='lightblue', edge_color='gray')
    plt.title(f"Jaula ({k},{g}) - {len(grafo.nodes())} vértices, {len(grafo.edges())} aristas")
    plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Gráfico guardado: {nombre_archivo}")

# Parámetros
k_val = 4
g_val = 8
cage_builder = CageBuilder(k_val, g_val)
cage = cage_builder.solve()

if cage:
    print(f"Jaula ({k_val},{g_val}) encontrada con {len(cage.nodes())} vértices.")
    # Guarda la imagen en lugar de mostrar
    guardar_grafo(cage, f"jaula_{k_val}_{g_val}.png", k_val, g_val)
else:
    print(f"No se pudo encontrar la jaula ({k_val},{g_val}) dentro del número máximo de iteraciones.")