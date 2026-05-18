from kage import jaula
import networkx as nx

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