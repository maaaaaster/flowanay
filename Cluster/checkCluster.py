import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
from sklearn.cluster import DBSCAN
import json
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from Graph import edgeKey,makeClientKey,showGraph


df = pd.read_csv('graph_join.csv')
G = nx.Graph()
colorMap ={}



def addToGraph(data):
    colorMap[edgeKey(data['cert'],data['client'])] = 'g' if data['label']=='white' else 'r'
    colorMap[data['cert']] = 'b'
    colorMap[data['client']] = 'y'
    G.add_edge(data['client'],data['cert'])

df['client'] = df.apply(makeClientKey, axis=1)
df.apply(addToGraph,axis=1)
print('GraphMaked')


# for k in range(2, 100):
#     cs = list(nx.k_clique_communities(G,k))
#     if len(cs) == 0:
#         break
#     for c in cs:
#         sub_g = G.subgraph(c)
#         showGraph(sub_g, colorMap)

groupLists = json.load(open('clusterResult.json'))
for group in groupLists[::-1]:
    g = nx.Graph()
    cnt = 2
    for node in group:
        for k, v in nx.bfs_successors(G, node):
            for node2 in v:
                g.add_edge(k, node2)
            cnt-=1
            if cnt<=0:
                break
    showGraph(g,colorMap)
