import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

def loadEdges():
    white = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/ssl_graph.csv')
    white = white[white.cnt>100]
    white['label'] = 'white'
    black = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/data/black_cluster.csv')
    black = black[black.cnt<20]
    black['label'] = 'black'
    result = pd.concat([black,white])
    t = result.groupby(['cert','cipher','extensions'], as_index=False).agg({'cnt':'count'})
    sameSet = set(t[t.cnt>1]['cert'])
    print(len(sameSet))
    def inSameCert(cert):
        if cert in sameSet:
            return 1
        return 0
    result['sameCert'] = result['cert'].map(inSameCert)
    result = result[(result['sameCert']==0) | (result['label']=='white')]
    result.to_csv('graph_join.csv',index=False)

def makeClientKey(data):
    clientKey = data['cipher']
    if data['extensions'] is not None:
        clientKey = clientKey + '_' + data['extensions']
    return clientKey


def edgeKey(data1,data2):
    if data1<data2:
        data1,data2 = data2,data1
    return '/'.join([data1,data2])

def showGraph(g,colorMap):
    nodeColors = []
    edgeColors = []
    for k in g.degree():
        print(k)
    for node in g.nodes():
        nodeColors.append(colorMap[node])
    for edge in g.edges():
        color = colorMap[edgeKey(edge[0], edge[1])]
        edgeColors.append(color)
    nx.draw_networkx(g, node_color=nodeColors, edge_color=edgeColors, with_labels=False)
    plt.show()
def drawGraph():
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

    outf = open('edge.txt','w+')
    for largest_components in sorted(nx.connected_components(G), key=len, reverse=True)[0:1]:
        g = G.subgraph(largest_components)
        # showGraph(g)
        for edge in g.edges:
            outf.write('%s %s\n'%(edge[0],edge[1]))
if __name__=='__main__':
    # loadEdges()
    # makeEdgeFile()
    drawGraph()
