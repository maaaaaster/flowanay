from ELModel import loadData,findOne
from utils import readDataFromKeys
import json
from ETA.Connect import Packets2Time
from ETA.Cipher import cipher2features, extension2features
import pandas as pd
def getClientIP(data,serverIP):
    dIP = readDataFromKeys(data, 'ConnectInfor.dIP')
    sIP = readDataFromKeys(data, 'ConnectInfor.sIP')
    if dIP.startswith(serverIP):
        return sIP
    else:
        return dIP

def readConnectFromKey(connectKey):
    tablename =  'connect_20180827'
    detail = {
        'query':{
            'match_phrase': {
                'ConnectInfor.ConnectKeyID': connectKey.replace('-',' ')
            }
        }
    }
    return findOne(tablename,detail=detail)

def readFromTable(sslTable):
    certSet = set()
    checkData = []
    dataGen = loadData(sslTable)
    cnt = 0
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            cipher = readDataFromKeys(data, 'TLS.ClientHello.CipherSuite')
            certList = readDataFromKeys(data, 'TLS.Cert')
            if cipher is None or certList is None or len(certList) == 0:
                continue
            connectKey = readDataFromKeys(data, 'ConnectInfor.ConnectKeyID')
            connectData = readConnectFromKey(connectKey)
            if connectData is None:
                continue

            certHash = certList[0]
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            extensions = readDataFromKeys(data, 'TLS.ClientHello.Extension.List',[])
            serverName = readDataFromKeys(data, 'TLS.ClientHello.Extension.ServerName','Null')
            clientIP = getClientIP(data,serverIP)

            features = {
                'certHash':certHash,
                'ConnectKeyID':connectKey,
                'serverIP':serverIP,
                'clientIP':clientIP,
                'serverName':serverName
            }
            connectFeatures = Packets2Time(readDataFromKeys(connectData, 'Statistics.Packets', []))
            cipherFeatures = cipher2features(cipher)
            extensionFeatures =  extension2features(extensions)
            features.update(connectFeatures)
            features.update(cipherFeatures)
            features.update(extensionFeatures)
            features.update()
            certSet.add(certHash)
            checkData.append(features)
        cnt+=len(datalist)
        print(cnt)
    df = pd.DataFrame(checkData)
    df.to_csv(sslTable+'.txt',index=0)
    json.dump(list(certSet), open(sslTable+'_certs.txt', 'w+'))

def cert2features(cert):
    return (cert['hash'], {
            'SAN_count': cert['SAN_count'],
            'self_signed': cert['self_signed'],
            'cert_duration': cert['cert_duration'],
            'isCA': cert['isCA']
        })



def makeTestData(tablename):
    tlsfile = '%s.txt' % tablename
    tlsData = pd.read_csv(tlsfile)
    certfile = '%s_certs.csv' % tablename
    certData = pd.read_csv(certfile)
    certMap = dict(list(certData.apply(cert2features, axis=1)))
    certFeatures = pd.DataFrame(list(tlsData['certHash'].map(lambda x:certMap[x])))
    test_data = pd.concat([tlsData,certFeatures],axis=1)
    test_data.to_csv('%s_test.csv'%tablename,index=False)

if __name__=='__main__':
    # toCheckData = readFromTable('ssl_20180827')
    makeTestData('ssl_20180827')