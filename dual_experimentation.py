import networkx as nx
import matplotlib.pyplot as plt

# DEPENDENCY OF THE PROJECT:
# Graph Analysis: NetworkX
# Graph Visualisation: Gephi

# Below are some Graph Libraries I can use:
# - NetworkX (Mainly Graph Analysis)
# - Rustworkx
# - GRAPE

# Graph Visualisation Tools:
# - "Cytoscape, Gephi, Graphviz and, for LaTeX typesetting, PGF/TikZ"

G = nx.petersen_graph()

nx.write_gexf(G, "petersen.gexf")
