import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
from TrainData import graphfile,checkBlackFile,checkWhiteFile


def edgeKey(data1,data2):
    if data1<data2:
        data1,data2 = data2,data1
    return '/'.join([data1,data2])

def makeClientKey(data):
    clientKey = data['cipher']
    if data['extensions'] is not None:
        clientKey = clientKey + '_' + data['extensions']
    return clientKey


def countGraph(g,blackMap,whiteMap):
    blackCount = 0
    whiteCount = 0
    for node in g.nodes():
        if node in blackMap:
            blackCount+=blackMap[node]
            print(node)
        elif node in whiteMap:
            whiteCount+=whiteMap[node]
    return blackCount,whiteCount
def showGraph(g,colorMap):
    nodeColors = []
    edgeColors = []
    blackCount = 0
    print('___________________')
    for k in g.degree():
        print(k)
    for node in g.nodes():
        nodeColors.append(colorMap[node])

    for edge in g.edges():
        color = colorMap[edgeKey(edge[0], edge[1])]
        edgeColors.append(color)
    nx.draw_networkx(g, node_color=nodeColors, edge_color=edgeColors, with_labels=False)
    plt.show()


def loadMap(filename):
    result = {}
    blackFile=pd.read_csv(filename)
    def addToMap(data):
        result[data['cert']] = data['cnt']
    blackFile.apply(addToMap,axis=1)
    return result

def makeGraph():
    df = pd.read_csv(graphfile)
    G = nx.Graph()
    colorMap ={}
    def addToGraph(data):
        colorMap[edgeKey(data['cert'],data['client'])] = 'g' if data['label']=='white' else 'r'
        colorMap[data['cert']] = 'b'
        colorMap[data['client']] = 'y'
        G.add_edge(data['client'],data['cert'])
    df['client'] = df.apply(makeClientKey, axis=1)
    df.apply(addToGraph, axis=1)
    return G,colorMap

def checkSub():
    G,colorMap = makeGraph()
    blackMap,whiteMap = loadMap(checkBlackFile),loadMap(checkWhiteFile),
    subConnects = sorted(nx.connected_components(G), key=len, reverse=True)
    print(len(subConnects))
    totalWhite,totalBlack = 0,0
    for largest_components in subConnects[10:]:
        g = G.subgraph(largest_components)
        black,white = countGraph(g,blackMap,whiteMap)
        totalBlack+=black
        totalWhite+=white
        # if white>0:
        #     showGraph(g,colorMap)
        print(totalBlack,totalWhite)



def checkCluster():
    G,colorMap = makeGraph()
    data = json.load(open('group2names.json'))
    blackMap,whiteMap = loadMap(checkBlackFile),loadMap(checkWhiteFile)
    totalBlack,totalWhite = 0,0
    for groupID in data:
        nodes = data[groupID]
        g = G.subgraph(nodes)
        # newG = nx.Graph()
        # for node in nodes:
        #     newG.add_node(node)
        #     cnt = 2
        #     for k, v in nx.bfs_successors(g, node):
        #         for node2 in v:
        #             newG.add_edge(k, node2)
        #         cnt -= 1
        #         if cnt <= 0:
        #             break
        # print(groupID,len(nodes),len(newG.nodes))
        black, white = countGraph(g, blackMap, whiteMap)
        totalBlack += black
        totalWhite += white
        print(totalBlack, totalWhite)
        # showGraph(g,colorMap)

if __name__=='__main__':
    # makeGraph()
    checkCluster()