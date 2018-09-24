from sklearn.cluster import DBSCAN
import json
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import get_named_colors_mapping


from matplotlib.colors import get_named_colors_mapping
from TrainGraph import checkCluster
from TrainData import graphfile

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
    node2vec = loadVecs('/home/networkEmbedding/OpenNE/join_all_128.txt')
    certSet= set(pd.read_csv(graphfile)['cert'])
    X = set(node2vec.keys()) & certSet
    features = pd.DataFrame([node2vec[x] for x in X])
    print('start cluster')
    y_pred = DBSCAN(min_samples=5,eps = 0.55).fit_predict(features)
    print('ends cluster')
    group2Names = {}

    for i in range(len(y_pred)):
        group = y_pred[i]
        if group not in group2Names:
            group2Names[group] = []
        group2Names[group].append(X[i])
    if -1 in group2Names:
        del(group2Names[-1])
    group2Names = dict((str(x),group2Names[x]) for x in group2Names)
    json.dump(group2Names, open('group2names.json', 'w+'))
    checkCluster()


if __name__=='__main__':
    clusterGraph()
