import pandas as pd
import json

whiteFile1 = '/home/OpenCode/FlowAnay/Cluster/data/ssl_graph.csv'
whiteFile2 = '/home/OpenCode/FlowAnay/Cluster/data/20180909_graph.csv'
blackFile = '/home/OpenCode/FlowAnay/Cluster/data/black_cluster.csv'
whiteJoinFile = '/home/OpenCode/FlowAnay/Cluster/data/white_graph_raw.csv'
certToCollect = '/home/OpenCode/FlowAnay/Cluster/data/white_cert.txt'
filterdwhiteJoinFile = '/home/OpenCode/FlowAnay/Cluster/data/white_graph.csv'
filterCertList = '/home/OpenCode/FlowAnay/Cluster/data/filter_white_cert.json'
filterdBlackJoinFile = '/home/OpenCode/FlowAnay/Cluster/data/black_graph.csv'
egdeFilePath = '/home/OpenCode/FlowAnay/Cluster/data/edges_graph.txt'
graphfile = '/home/OpenCode/FlowAnay/Cluster/data/final_graph.txt'
checkBlackFile = '/home/OpenCode/FlowAnay/Cluster/data/checkBlack.txt'
checkWhiteFile = '/home/OpenCode/FlowAnay/Cluster/data/checkWhite.txt'

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

def filterWhite():
    result = []
    for filename in [whiteFile1,whiteFile2]:
        result.append(pd.read_csv(filename))
    result = pd.concat(result)
    result.groupby(['cert', 'cipher', 'extensions'], as_index=False).agg({'cnt': 'sum'})
    result.to_csv(whiteJoinFile,index=False)

def filterCert():
    from CheckFilterCert import loadRealAttack
    realAttackCerts = loadRealAttack()
    df = pd.read_csv(whiteJoinFile)
    t = df.groupby('cert', as_index=False).agg({'cnt':'sum','ipCnt':'max'})
    certSet = set(t[(t.cnt>250) & (t.ipCnt>100)]['cert']) - set(realAttackCerts)
    certSet = set(df[(df.cnt>100) & (df.ipCnt>10)]['cert']) - set(realAttackCerts)
    whiteEdges = df[df['cert'].map(lambda x:x in certSet)][df.ipCnt>1]
    whiteEdges.to_csv(filterdwhiteJoinFile,index=False)
    # t = df[(df.cnt>100) & (df.ipCnt>10)]
    # t.to_csv(filterdwhiteJoinFile, index=False)


def filterBlack():
    df = pd.read_csv(blackFile)
    certSet = set(json.load(open(filterCertList)))
    t = df[df['cert'].map(lambda x: x not in certSet )]
    t.to_csv(filterdBlackJoinFile,index=False)


def combineData():
    black = pd.read_csv(filterdBlackJoinFile)
    black['label'] = 'black'
    aBlack = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/data/ActualBlack.csv')
    aBlack['label'] = 'black'
    white = pd.read_csv(filterdwhiteJoinFile)
    white['label'] ='white'
    result = pd.concat([black,aBlack,white])
    result.to_csv(graphfile,index=False)

def recordCert():
    result = pd.read_csv(graphfile)
    blackCerts = result[result.label == 'black'].groupby(['cert'], as_index=False).agg({'cnt':'sum'})
    blackCerts.to_csv(checkBlackFile,index=False)
    blackCerts = result[result.label == 'white'].groupby(['cert'], as_index=False).agg({'cnt':'sum'})
    blackCerts.to_csv(checkWhiteFile,index=False)

if __name__ == '__main__':
    filterCert()
    # filterBlack()
    combineData()
    recordCert()