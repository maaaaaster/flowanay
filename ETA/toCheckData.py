from ELModel import loadData,findOne
from utils import readDataFromKeys
import json
from ETA.Connect import Packets2Time
from ETA.Cipher import cipher2features

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
    dataGen = loadData(sslTable)
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            cipher = readDataFromKeys(data, 'TLS.ClientHello.CipherSuite')
            certList = readDataFromKeys(data, 'TLS.Cert')
            if cipher is None or certList is None or len(certList) == 0:
                continue
            connectData = readConnectFromKey(connectKey)

            if connectData is None:
                continue

            certHash = certList[0]
            connectKey = readDataFromKeys(data, 'ConnectInfor.ConnectKeyID')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            extensions = readDataFromKeys(data, 'TLS.ClientHello.Extension.List',[])
            serverName = readDataFromKeys(data, 'TLS.ClientHello.Extension.ServerName','Null')
            clientIP = getClientIP(data,serverIP)

            basic = {
                'certHash':certHash,
                'ConnectKeyID':connectKey,
                'serverIP':serverIP,
                'clientIP':clientIP,
                'serverName':serverName
            }
            features = {}
            connectFeatures = Packets2Time(readDataFromKeys(connectData, 'Statistics.Packets', []))
            cipherFeatures = cipher2features(cipher)
            features.update(connectFeatures)
            features.update(cipherFeatures)




if __name__=='__main__':
    toCheckData = readFromTable('ssl_20180827')