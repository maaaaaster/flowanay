import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import preprocessing

def inPku(ip):
    if ip.startswith('162.105') or ip.startswith('222.29'):
        return 1
    return -1

df = pd.read_csv('pku_cluster.csv')
df['inPku'] = df['clientIP'].map(inPku)
# df=df[df['inTsinghua']<0]

data = df.groupby(['clientIP'], as_index=False).agg({
    'sendNum': 'std',
    'recNum': 'std',
    'recPort':'count',
    'sendByte':'max',
    'recByte':'min',
    'byteRatio':'mean',
    'packetRatio':'mean',
})

data.fillna(0, inplace = True)
data = data.rename(columns={'recPort': 'cnt'})

ips = list(data['clientIP'])
del(data['clientIP'])
X = preprocessing.scale(data, axis=0, with_mean=True, with_std=True, copy=True)
y_pred = DBSCAN(min_samples=5, eps=0.5).fit_predict(X)

group2Names = {}
for i in range(len(y_pred)):
    if y_pred[i] not in group2Names:
        group2Names[y_pred[i]] = []
    group2Names[y_pred[i]].append(ips[i])

groupLen = len(group2Names.keys())
print(groupLen)

del(group2Names[-1])
groupList = sorted(list(group2Names.values()),key=lambda x:len(x))[:-1]
outf = open('clusterIP.txt','w+')
for group in groupList:
    result = {}
    for clientIP in group:
        outf.write(clientIP+'\n')

