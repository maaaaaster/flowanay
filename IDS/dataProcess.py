import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import preprocessing

def inTsinghua(ip):
    if ip.startswith('166.111'):
        return 1
    return -1

df = pd.read_csv('443attack_test_0823.csv')
df['inTsinghua'] = df['clientIP'].map(inTsinghua)
# df['inTsinghua'] = df['serverIP'].map(inTsinghua)

df=df[df['inTsinghua']<0]
# df = df[df.serverIP=='166.111.4.100']
data = df.groupby(['clientIP'], as_index=False).agg({
    'sNum': 'std',
    'dNum': 'std',
    'serverPort':'count',
    'sBytes':'max',
    'dBytes':'min'
})

data.fillna(0, inplace = True)
data = data.rename(columns={'serverPort': 'cnt'})

ips = list(data['clientIP'])
del(data['clientIP'])
X = preprocessing.scale(data, axis=0, with_mean=True, with_std=True, copy=True)
# X['cnt'] = data['cnt'].copy()
y_pred = DBSCAN(min_samples=5, eps=0.5).fit_predict(X)
group2Names = {}
for i in range(len(y_pred)):
    if ips[i] in ['110.16.13.30','116.25.41.97','202.112.26.123']:
        print(y_pred[i])
    if y_pred[i] not in group2Names:
        group2Names[y_pred[i]] = []
    group2Names[y_pred[i]].append(ips[i])
print(len(group2Names.keys()))
for group in range(0,4):
    print(group, len(group2Names[group]))
    result = {}
    for clientIP in group2Names[group]:
        serverSet = set(df[df['clientIP']==clientIP]['serverIP'])
        for serverIP in serverSet:
            if serverIP=='166.111.4.40':
                print(clientIP)
            if serverIP not in result:
                result[serverIP] = 0
            result[serverIP]+=1
    print(result)
