import pandas as pd
import networkx as nx
import os
from TrainData import realTest
from TrainGraph import makeClientKey

edgefile = '/home/FlowAnay/Cluster/edges0920.txt'
vecfile = '/home/FlowAnay/Cluster/vec0920.txt'
def saveGraph(infile,outfile):
    df = pd.read_csv(infile)
    G = nx.Graph()
    df['client'] = df.apply(makeClientKey, axis=1)
    def addToGraph(data):
        G.add_edge(data['client'],data['cert'])
    df.apply(addToGraph, axis=1)
    g = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    nx.write_adjlist(g,outfile)

def node2vec(inname,outname):
    cmd = 'python /home/networkEmbedding/OpenNE/src/main.py --method node2vec --input %s --graph-format adjlist\
     --output %s --q 0.65 --p 0.15 --representation-size 32'%(inname,outname)
    print(cmd)
    os.system(cmd)


if __name__=='__main__':
    # saveGraph(realTest,edgefile)
    node2vec(edgefile,vecfile)