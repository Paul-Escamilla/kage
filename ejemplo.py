from kage.CageBuilder import CageBuilder
import networkx as nx
import matplotlib.pyplot as plt

def main():
    print("¡Bienvenido al generador de Jaulas (Kage)!")
    print("------------------------------------------")
    
    k = 3 
    g = 5  
    
    print(f"\nGenerando una jaula para k={k} y g={g} (Grafo de Petersen)...")
    
    builder = CageBuilder(k=k, g=g)
    grafo_resultado = builder.solve(max_iter=15)
    nodos_totales = len(grafo_resultado.nodes())
    aristas_totales = len(grafo_resultado.edges())
    
    print("\n¡Resultados!")
    print(f"-> Vértices totales generados: {nodos_totales}")
    print(f"-> Aristas totales generadas: {aristas_totales}")
    print(f"-> Vértices extra utilizados (exceso): {builder.exceso}")
    

    print("\nGuardando la visualización en 'ejemplo_3_5.png'...")
    plt.figure(figsize=(8, 8))
    nx.draw(grafo_resultado, with_labels=True, node_color="lightblue", font_weight="bold")
    plt.savefig("ejemplo_3_5.png")
    print("¡Proceso terminado con éxito!")

if __name__ == "__main__":
    main()