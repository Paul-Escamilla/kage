---
sidebar_position: 2
title: Conceptos Previos
---

Antes de adentrarnos en la lógica del algoritmo, es crucial entender los elementos básicos que componen este problema.

## Gráfica $k$-regular

Una gráfica $G$ es $k$-regular o simplemente regular si para todo vértice $u$ en $G$ se tiene que $d_G(u) = k$.

Un ejemplo de una gráfica $3$-regular es el siguiente: 

<a id="ejemplo-1"></a>
<img width="444" height="348" alt="Ejemplo 3 regular" src="https://github.com/user-attachments/assets/74c5ab46-b141-4eec-b1a6-fe8182e43940" />
<p><em>Figura 1: Ejemplo de una gráfica 3-regular.</em></p>

## Ciclo de una gráfica

Un ciclo es un camino cerrado no-trivial y que no repite vértices, salvo el primero y el último. 

Nótese que la gráfica anterior ([Figura 1](#ejemplo-1)) tiene los siguientes ciclos: (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2, 3), (0, 1, 3, 2) y (0, 2, 1, 3). Es decir que su ciclo más corto es de longitud 3.

A esto de hecho se le conoce como una $(3, 3)$-jaula.

## Jaula 

Una $(k, g)$-jaula es una gráfica $k$-regular con cuello $g$ (donde el cuello es la longitud del ciclo más corto en la gráfica) construida de manera que se use la menor cantidad posible de vértices. Otro ejemplo es la famosa gráfica de Petersen: 

<a id="ejemplo-2"></a>
<img width="412" height="376" alt="image" src="https://github.com/user-attachments/assets/b259c922-700c-4132-ad8e-bc8e976c486c" />
<p><em>Figura 2: Gráfica de Petersen, la cual es una (3, 5)-jaula.</em></p>

## Cota de Moore

Para saber cuántos vértices necesitará nuestra jaula, nos basamos en un límite teórico conocido como la **Cota de Moore**. Esta cota establece el número mínimo de vértices $n$ que debe tener una gráfica $k$-regular con cuello $g$.

Dependiendo de si el cuello $g$ es par o impar, la cota inferior se calcula de la siguiente manera:

* **Si el cuello $g$ es impar** (donde $g = 2d + 1$):
  $$n \ge 1 + k \sum_{i=0}^{d-1} (k-1)^i$$

* **Si el cuello $g$ es par** (donde $g = 2d$):
  $$n \ge 2 \sum_{i=0}^{d-1} (k-1)^i$$

Las gráficas que logran igualar exactamente esta cota inferior teórica se conocen como **Gráficas de Moore**. 

En el contexto de nuestro algoritmo de backtracking, la Cota de Moore es una herramienta de optimización crucial: nos dicta el tamaño inicial del conjunto de vértices a explorar, ya que sabemos matemáticamente que es imposible construir una $(k, g)$-jaula con un número de vértices menor al que indica esta fórmula.

## Árboles en la Teoría de Grafos

En la teoría de grafos, un **árbol** es una gráfica conexa que no contiene ningún ciclo. Se puede ver como una estructura jerárquica que nace de un vértice "raíz" y se ramifica hacia afuera en "hojas" (vértices de grado 1).

Entender esto es fundamental para nuestro proyecto, ya que la primera fase de construcción de una jaula consiste precisamente en crear un árbol base. A partir de un nodo central (o dos), el algoritmo ramifica la gráfica hasta el límite permitido por el cuello $g$. El reto del problema de las jaulas radica en cómo conectar las "hojas" de ese árbol entre sí para cerrar la gráfica (creando ciclos) sin romper la regla del ciclo más corto.

## Simetría e Isomorfismo

Dos gráficas son **isomorfas** si tienen exactamente la misma estructura de conexiones, incluso si sus vértices están dibujados en posiciones diferentes o tienen nombres distintos. Es decir, son estructuralmente la misma gráfica.

En el contexto de gráficas regulares, los árboles de búsqueda generan una enorme cantidad de **simetría**. Hay muchas ramas que son "gemelas" idénticas. Si intentar conectar el vértice $A$ a cierta rama no lleva a una solución, intentar conectarlo a una rama isomorfa (simétrica) tampoco lo hará. Nuestro algoritmo aprovecha esta propiedad matemática realizando una "poda de simetría" para no evaluar dos veces la misma estructura, ahorrando así una cantidad masiva de tiempo de cómputo.