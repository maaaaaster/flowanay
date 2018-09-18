from sklearn.cluster import DBSCAN
import json
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import get_named_colors_mapping


from matplotlib.colors import get_named_colors_mapping
from TrainGraph import checkCluster

colorList = list(get_named_colors_mapping().values())

def loadVecs(filename):
    inf = open(filename)
    print(inf.readline())
    result = {}
    for line in inf.readlines():
        vals = line.split(' ')
        data = []
        for val in vals[1:]:
            data.append(float(val))
        key = vals[0]
        result[key] = data
    return result



def clusterGraph():
    node2vec = loadVecs('/home/OpenCode/FlowAnay/Cluster/data/vec_32.txt')
    X = list(node2vec.keys())
    features = pd.DataFrame(list(node2vec.values()))
    print('start cluster')
    y_pred = DBSCAN(min_samples=20,eps = 0.55).fit_predict(features)
    print('ends cluster')
    group2Names = {}
    cDict = {}
    # pca = PCA(n_components=2).fit(features)
    # pca_2d = pca.transform(features)
    for i in range(len(y_pred)):
        group = y_pred[i]
        if group not in group2Names:
            group2Names[group] = []
        group2Names[group].append(X[i])
        # cDict[group] = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c=colorList[group+1], marker='o')

    # del (cDict[-1])
    # drawList = list(cDict.values())
    # titles = list('Cluster %d' % d for d in cDict.keys())
    # plt.legend(drawList, titles)
    # plt.title('DBSCAN finds %d clusters and Noise' % len(drawList))
    # plt.show()\
    if -1 in group2Names:
        del(group2Names[-1])
    group2Names = dict((str(x),group2Names[x]) for x in group2Names)
    json.dump(group2Names, open('group2names.json', 'w+'))
    checkCluster()
    # for group in group2Names:
    #     if group==-1 or len(group2Names[group])>80:
    #         continue
    #
    #     # print(group,len(group2Names[group]))
    #     black, white = 0, 0
    #     for name in group2Names[group]:
    #         if name in blackMap:
    #             black +=blackMap[name]
    #         if name in whiteMap:
    #             white +=whiteMap[name]
    #     if black+white<1000:
    #         blackCount += black
    #         whiteCount += white
    #         if black==0:
    #             print(group2Names[group])
    #     # else:
    #     #     print('white',white)
    #     # print(blackCount,whiteCount)
    # print(len(group2Names.keys()))
    # dumpGroup = group2Names.copy()
    # del (dumpGroup[-1])
    # json.dump(list(dumpGroup.values()), open('clusterResult.json', 'w+'))
    #
    # del (cDict[-1])
    # drawList = list(cDict.values())
    # titles = list('Cluster %d' % d for d in cDict.keys())
    # plt.legend(drawList, titles)
    # plt.title('DBSCAN finds %d clusters and Noise' % len(drawList))
    # plt.show()
    # dumpGroup = group2Names.copy()
    # del(dumpGroup[-1])
    # json.dump(list(dumpGroup.values()),open('clusterResult.json','w+'))

if __name__=='__main__':
    clusterGraph()
