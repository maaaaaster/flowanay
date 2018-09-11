import pandas as pd


whiteFile = '/home/OpenCode/FlowAnay/Cluster/data/ssl_graph.csv'
blackFile = '/home/OpenCode/FlowAnay/Cluster/data/black_cluster.csv'
whiteFil2 = '/home/OpenCode/FlowAnay/Cluster/data/20180909.csv'
whiteFil3 = '/home/OpenCode/FlowAnay/Cluster/data/20180909_graph.csv'

def joinFromRaw(inname,outname):
    def checkIP(data):
        return data.drop_duplicates().count()
    df = pd.read_csv(inname)
    edge_count = df.groupby(['cert', 'cipher', 'extensions'], as_index=False).agg({'clientIP': checkIP, 'serverIP': 'count'})
    edge_count.rename(columns={'serverIP': 'cnt', 'clientIP': 'ipCnt'}, inplace=True)
    edge_count.to_csv(outname, index=False)

def loadEdges():
    white = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/data/test_20180909.csv')
    white = white[white.cnt>100]
    white['label'] = 'white'
    black = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/test_black_cluster.csv')
    # black = black[black.cnt<20]
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

joinFromRaw(whiteFil2,whiteFil3)