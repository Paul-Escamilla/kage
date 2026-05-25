---
sidebar_position: 3
title: El Algoritmo de Búsqueda
---

# Construyendo la Jaula: El Algoritmo 

El núcleo del Proyecto Kage es la clase `CageBuilder`. En lugar de intentar conectar vértices al azar y verificar si forman una jaula, nuestro algoritmo sigue una estrategia determinista de tres fases: **Construcción Base**, **Búsqueda por Backtracking con Poda**, y **Adición de Exceso**.

A continuación explicamos cada fase de la ejecución.

---

## Fase 1: El Árbol Base (Cota de Moore)

Como vimos en la sección anterior, la Cota de Moore nos da el número mínimo de vértices. El método `_base_of_cage` construye un árbol (o dos árboles unidos por una arista si el cuello $g$ es par) que se expande hacia abajo como si fueran ramas.

1. **Raíz:** Comenzamos con un vértice central (o dos).
2. **Capas:** Expandimos el grafo conectando nuevos vértices hasta alcanzar el diámetro permitido por el cuello $g$.
3. **Resultado:** Obtenemos una gráfica "incompleta" (las hojas del árbol no tienen grado $k$). Matemáticamente, sabemos que estas hojas deben conectarse entre sí de alguna manera para cerrar el grafo sin crear ciclos cortos.

---

## Fase 2: Backtracking Inteligente y Poda

Una vez que tenemos el árbol base, necesitamos conectar las hojas. Aquí entra el método `_backtrack`. Un enfoque de fuerza bruta probaría todas las combinaciones posibles, lo cual tomaría años para jaulas grandes. Nosotros lo optimizamos utilizando las siguientes estrategias:

### 1. Heurística MRV (Minimum Remaining Values)
El algoritmo no elige qué vértice conectar al azar. Busca el vértice que esté **más cerca de completarse** (el que tiene mayor grado actual pero menor a $k$). Esto fuerza al algoritmo a fallar rápido si va por el camino equivocado, ahorrando millones de iteraciones.

### 2. Detección de Peligro (Prevención de Ciclos Cortos)
Antes de siquiera intentar unir dos vértices, el algoritmo escanea a su alrededor usando `nx.single_source_shortest_path_length`. Si el vértice destino está a una distancia menor a $g-2$, conectarlos crearía un ciclo menor a $g$. Esta conexión se descarta instantáneamente.

### 3. Poda de Simetría
Los grafos tienen muchas ramas idénticas (simetría). Si el algoritmo intenta conectar el vértice $A$ con el $B$ y fracasa, no tiene sentido intentar conectar el $A$ con el hermano gemelo del $B$. Usando un `parent_map`, el algoritmo guarda las "firmas" de las ramas probadas y se salta los intentos redundantes.

### 4. Poda Look-Ahead (Visión a futuro)
Esta es la técnica más poderosa. Cada vez que se añade una arista, el algoritmo revisa el resto de los vértices. Si detecta que a algún vértice ya no le quedan suficientes "candidatos válidos" para alcanzar su grado $k$, aborta toda la rama de búsqueda. No espera a llegar al final para darse cuenta de que era un callejón sin salida.

---

## Fase 3: El Manejo del Exceso

Se sabe matemáticamente que **no todas las $(k, g)$-jaulas son Gráficas de Moore**. Muchas veces, es imposible cerrar el grafo solo con los vértices de la cota teórica.

Si el backtracking determina con 100% de seguridad que no hay solución con el árbol base, el método `add_vertices_exceso` entra en acción:
* Añade 1 o 2 vértices nuevos (dependiendo de la paridad de $k$).
* Los "ancla" estratégicamente a las hojas del árbol original.
* Vuelve a lanzar el algoritmo de backtracking con este nuevo espacio de búsqueda. 

Este proceso se repite incrementando el tamaño del grafo hasta que encuentra la jaula óptima.

---

## Visualización de Resultados

Para facilitar el análisis, el algoritmo incluye la función `draw_kage`, la cual renderiza la gráfica encontrada utilizando la librería `matplotlib` y `networkx` bajo 4 layouts matemáticos distintos (Energía, Espectral, Resortes y Circular). Esto permite a los investigadores identificar visualmente las propiedades de simetría de la jaula generada.