from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import get_named_colors_mapping

colorList= list(get_named_colors_mapping().values())

def loadVecs(filename):
    inf = open(filename)
    # print(inf.readline())
    certSet,cipherSet = loadHash()
    result = {}
    for line in inf.readlines():
        vals = line.split(' ')
        data = []
        for val in vals[1:]:
            data.append(float(val))
        key = vals[0]
        if key in certSet or key in cipherSet:
            result[key] = data
    return result


def clusterGraph():
    keyMap = {}
    inf = open('/home/OpenCode/FlowAnay/vec_44.txt')
    inf.readline()
    for line in inf.readlines():
        vals = line.split(' ')
        data = []
        for val in vals[1:]:
            data.append(float(val))
        key = vals[0]
        keyMap[key] = data

    df = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/ssl_graph.csv')
    def edgeFeatures(data):
        clientKey = data['cipher']
        if data['extensions'] is not None:
            clientKey = clientKey + '_' + data['extensions']
        result = keyMap[data['cert']]+keyMap[clientKey]
        result = dict((index,result[index]) for index in range(len(result)))
        return pd.Series(result)

    features = pd.DataFrame(df.apply(edgeFeatures,axis=1))
    features = features.iloc[:10000,:]
    print('start cluster')
    y_pred = DBSCAN(min_samples=3,eps = 0.6).fit_predict(features)
    print('ends cluster')
    group2Names = {}
    for i in range(len(y_pred)):
        for i in range(len(y_pred)):
            if y_pred[i] not in group2Names:
                group2Names[y_pred[i]] = []
            group2Names[y_pred[i]].append(df.at[i,'cert'])
    for group in group2Names:
        print(group, len(group2Names[group]))
        print(group2Names[group][:10])
    pca = PCA(n_components=2).fit(features)
    pca_2d = pca.transform(features)

def culster(clusterData):
    Names = list(clusterData.keys())
    X = list(clusterData.values())
    y_pred = DBSCAN(min_samples=5,eps = 0.5).fit_predict(X)
    group2Names = {}
    cDict = {}
    pca = PCA(n_components=2).fit(X)
    pca_2d = pca.transform(X)
    for i in range(len(y_pred)):
        group = y_pred[i]
        if group not in group2Names:
            group2Names[group] = []
        group2Names[group].append(Names[i])
        cDict[group] = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c=colorList[group+1], marker='o')
    for group in group2Names:
        print(group,len(group2Names[group]))
        print(group2Names[group][:10])


    del(cDict[-1])
    drawList = list(cDict.values())
    titles = list('Cluster %d'%d for d in cDict.keys())
    plt.legend(drawList, titles)
    plt.title('DBSCAN finds %d clusters and Noise'%len(drawList))
    plt.show()


def loadHash():
    df = pd.read_csv('data/ssl_graph.csv')
    certHashSet = set(df.key.map(lambda x: x.split('/')[0]))
    cipherHashSet = set(df.key.map(lambda x: x.split('/')[1]))
    return certHashSet,cipherHashSet

if __name__=='__main__':
    clusterData = loadVecs('join_all.txt')
    culster(clusterData)
    # clusterGraph()
