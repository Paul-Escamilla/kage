import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from kage import jaula
import networkx as nx
import matplotlib.pyplot as plt

G = jaula(3,3)
G2 = jaula(3,5)
G3 = jaula(3,8)

def test_jaula():
    assert nx.is_k_regular(G, 3) == True
    assert nx.girth(G) == 3
    assert nx.is_k_regular(G2, 3) == True
    assert nx.girth(G2) == 5
    assert nx.is_k_regular(G3, 3) == True
    assert nx.girth(G3) == 8
def guardar_grafo(grafo, nombre_archivo):
    plt.figure(figsize=(10,8))
    # Usa un layout para ordenar los nodos (puedes probar spring_layout, circular_layout, etc.)
    pos = nx.spring_layout(grafo, seed=42)  # seed para reproducibilidad
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=300, font_size=8)
    plt.title(f"Jaula (k={grafo.degree(0) if grafo.nodes else 3}, g={nx.girth(grafo)})")
    plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight')
    plt.close()   # cerrar figura para liberar memoria
    print(f"Gráfico guardado: {nombre_archivo}")

# Guardar cada grafo
guardar_grafo(G, "jaula_3_3.png")
guardar_grafo(G2, "jaula_3_5.png")
guardar_grafo(G3, "jaula_3_8.png")