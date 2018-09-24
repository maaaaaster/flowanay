from sklearn.cluster import DBSCAN
import json
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import get_named_colors_mapping

colorList= list(get_named_colors_mapping().values())
from TrainGraph import *

def loadVecs(filename):
    inf = open(filename)
    print(inf.readline())
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

def loadMap(filename):
    result = {}
    blackFile=pd.read_csv(filename)
    def addToMap(data):
        result[data['cert']] = data['cnt']
    blackFile.apply(addToMap,axis=1)
    return result

def clusterGraph():
    from matplotlib.colors import get_named_colors_mapping
    colorList = list(get_named_colors_mapping().values())
    keyList = []
    trainList = []
    inf = open('embedding.txt')
    inf.readline()
    for line in inf.readlines():
        vals = line.split(' ')
        data = []
        for val in vals[1:]:
            data.append(float(val))
        key = vals[0]
        keyList.append(key)
        trainList.append(data)

    blackMap,whiteMap = loadMap(checkBlackFile),loadMap(checkWhiteFile),
    blackCount = 0
    whiteCount = 0
    features = pd.DataFrame(trainList)
    print('start cluster')
    y_pred = DBSCAN(min_samples=2,eps = 0.6).fit_predict(features)
    print('ends cluster')
    group2Names = {}
    cDict = {}
    pca = PCA(n_components=2).fit(features)
    pca_2d = pca.transform(features)
    for i in range(len(y_pred)):
        group = y_pred[i]
        if group not in group2Names:
            group2Names[group] = []
        group2Names[group].append(keyList[i])
        # cDict[group] = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c=colorList[group+1], marker='o')
    for group in group2Names:
        if group==-1 or len(group2Names[group])>80:
            continue

        # print(group,len(group2Names[group]))
        black, white = 0, 0
        for name in group2Names[group]:
            if name in blackMap:
                black +=blackMap[name]
            if name in whiteMap:
                white +=whiteMap[name]
        if black+white<1000:
            blackCount += black
            whiteCount += white
            if black==0:
                print(group2Names[group])
        # else:
        #     print('white',white)
        # print(blackCount,whiteCount)
    print(len(group2Names.keys()))
    dumpGroup = group2Names.copy()
    del (dumpGroup[-1])
    json.dump(list(dumpGroup.values()), open('clusterResult.json', 'w+'))

    del (cDict[-1])
    drawList = list(cDict.values())
    titles = list('Cluster %d' % d for d in cDict.keys())
    plt.legend(drawList, titles)
    plt.title('DBSCAN finds %d clusters and Noise' % len(drawList))
    plt.show()
    dumpGroup = group2Names.copy()
    del(dumpGroup[-1])
    json.dump(list(dumpGroup.values()),open('clusterResult.json','w+'))

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

    dumpGroup = group2Names.copy()
    del(dumpGroup[-1])
    json.dump(list(dumpGroup.values()),open('clusterResult.json','w+'))

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
    # clusterData = loadVecs('join_all.txt')
    # culster(clusterData)
    clusterGraph()
