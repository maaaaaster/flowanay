import networkx as nx

G = nx.read_edgelist('D:/join_edges.txt')
print(len(G.nodes))
for largest_components in sorted(nx.connected_components(G), key=len, reverse=True):
    g = G.subgraph(largest_components)
    nx.write_edgelist(g,'D:/sub.txt')
    break
