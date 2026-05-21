# Kage 

En este repositorio se desarrolla un algoritmo eficiente para la creación de **jaulas**. Para lograr esto, el algoritmo se apoya fuertemente en la técnica de **backtracking** (vuelta atrás). 

El objetivo de esta documentación es explicar desde cero la teoría detrás del problema y cómo nuestra implementación lo resuelve de manera óptima.
## 📚 Conceptos Previos

Antes de adentrarnos en la lógica del algoritmo, es crucial entender los elementos básicos que componen este problema.
### Grafica k regular

Una gráfica G es k-regular o simplemente regular si para todo vértice u en G se tiene que $d_G(u) = k$.

Un ejemplo para contrastar la definicion de una grafica G 3-regular es la siguente 

<a id="ejemplo-1"></a>
<img width="444" height="348" alt="Ejemplo 3 regular" src="https://github.com/user-attachments/assets/74c5ab46-b141-4eec-b1a6-fe8182e43940" />
<p><em>Figura 1: Ejemplo de una grafica 3-regular.</em></p>

### Ciclo de una grafica

Un ciclo es un camino cerrado no-trivial y que no repite vértices, salvo el primero y el último.
Notese que la anterior grafica [Figura 1](#ejemplo-1). Tiene los siguientes ciclos: (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3). Es decir que su ciclo mas corto es de longuitud 3.

A esto de hecho se le conoce como una (3, 3) Jaula 

### Jaula 

Una (k, g)-Jaula es una grafica k-regular con con cuello g, donde el cuello de una grafica es el ciclo mas corto de una grafica, de manera en que se use la menor cantidad posible de vertices. Otro ejemplo de una grafica es la famosa grafica de Petersen 

<a id="ejemplo-2"></a>
<img width="412" height="376" alt="image" src="https://github.com/user-attachments/assets/b259c922-700c-4132-ad8e-bc8e976c486c" />
<p><em>Figura 2: Grafica de Petersen.</em></p>



