import networkx as nx
from CageBuilder import CageBuilder
def test_cage():
k_val = 3
g_val = 7
cage_builder = CageBuilder(k_val, g_val)
cage = cage_builder.solve()

if cage:
    print(f"Jaula ({k_val},{g_val}) encontrada con {len(cage.nodes())} vértices.")
    cage_builder.draw_kage()
else:
    print(f"No se pudo encontrar la jaula ({k_val},{g_val}) dentro del número máximo de iteraciones.")
test_cage()
