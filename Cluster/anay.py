import pandas as pd
def clientKey(data):
    key = data['cipher']
    if data['extensions'] is not None:
        key = key +'_' +data['extensions']
    return  key

def distinct(data):
    return data.drop_duplicates().count()

def filterCert():

    df = pd.read_csv('ssl_graph.csv')
    df['clientKey'] = df.apply(clientKey, axis = 1)
    oneClientCert = df.groupby('cert', as_index=False).agg({'clientKey':'count','ipCnt':'max'})
    oneClientCert = oneClientCert[(oneClientCert.clientKey==1) & (oneClientCert.ipCnt>1)]
    oneCertClient = df.groupby('clientKey', as_index=False).agg({'cert':'count','ipCnt':'max'})
    oneCertClient = oneCertClient[(oneCertClient.cert==1) & (oneCertClient.ipCnt>1)]
    clientSet = set(oneCertClient['clientKey'])
    certSet = set(oneClientCert['cert'])
    def filterData(data):
        result = 0
        if data['cert'] in certSet:
            result += 10
        if data['clientKey'] in clientSet:
            result +=1
        return result
    df['ok'] = df.apply(filterData,axis=1)
    print(df.ok)
    return df


def certList():
    import json
    df = pd.read_csv('ssl_graph.csv')
    certs = list(df['cert'].drop_duplicates())
    print(len(certs))
    json.dump(certs,open('data/cluster_certs.txt','w+'))



def checkCert():
    df = pd.read_csv('data/cluster_certs.csv')
    df['hasIP'] = df['SAN'].map(lambda x : 'IP Address:' in x)


if __name__=='__main__':
    # filterCert()
    certList()
