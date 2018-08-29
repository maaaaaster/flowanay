from ELModel import loadData
from utils import readDataFromKeys,addCountToMap,addSetToMap,saveCount,saveMap
import json
import pandas as pd



def saveGraph(tablename):
    certMap = {}
    certCount = {}
    cipherMap = {}
    count = 0
    dataGen = loadData(tablename,["ConnectInfor.first", "TLS.Cert", "TLS.ClientHello.CipherSuite"])
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            cipher = readDataFromKeys(data,'TLS.ClientHello.CipherSuite')
            # ip = readDataFromKeys(data,'ConnectInfor.first')
            cert = readDataFromKeys(data,'TLS.Cert')
            if cipher is None or cert is None or len(cert) == 0:
                continue
            cert = cert[0]
            addCountToMap(certCount,cert)
            addSetToMap(certMap,cert,cipher)
            addSetToMap(cipherMap, cipher, cert)
        count+=len(datalist)
        print(count)
    saveMap(certMap, 'data/cert2ciphers_%s.csv'%tablename)
    saveMap(cipherMap, 'data/cipher2Certs_%s.csv'%tablename)
    saveCount(certCount, 'data/cert2count_%s.csv'%tablename)

def filterGraph(tablename):
    df = pd.read_csv('data/cert2ciphers_%s.csv'%tablename)
    df['data_num'] = df['data'].map(lambda x:x.count(';')+1)
    oneCipherCerts = set(df[df['data_num']==1]['key'])

    df2 = pd.read_csv('data/cert2count_%s.csv'%tablename)
    oneTimeCerts = set(df2[df2['count']==1]['key'])
    tocheck = list(oneCipherCerts - oneTimeCerts)[:100]
    print(tocheck)


# saveGraph('ssl_20180825')
filterGraph('ssl_20180825')