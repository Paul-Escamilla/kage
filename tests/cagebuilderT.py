from kage.CageBuilder import CageBuilder
import matplotlib.pyplot as plt
import networkx as nx
import pytest

def test_casos_borde():
    with pytest.raises(ValueError):
        CageBuilder(k=1, g=5)
        
    with pytest.raises(ValueError):
        CageBuilder(k=3, g=2)

def test_cage_builder_base():
    builder = CageBuilder(k=2, g=3)
    grafo = builder.solve(max_iter=5)
    
    assert nx.is_k_regular(grafo, 2)
    assert nx.girth(grafo) == 3
    assert len(grafo.nodes()) == 3

def test_exceso_vertices():
    builder = CageBuilder(k=3, g=7)
    
    assert builder.exceso == 0
    builder.add_vertices_exceso()
    assert builder.exceso > 0

    grafo = builder.solve(max_iter=5)
    
    assert nx.is_k_regular(grafo, 3)
    assert nx.girth(grafo) == 7
    assert len(grafo.nodes()) == 24