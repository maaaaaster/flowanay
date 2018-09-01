from ELModel import loadData
from utils import readDataFromKeys,addCountToMap
import json

def CountQuery(tablename,detail):
    serverSet, clientSet, recordTimeSet = set(), set(), set()
    dataGen = loadData(table=tablename, detail=detail)
    cipherCount = {}
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            firstIP = readDataFromKeys(data, 'ConnectInfor.first')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            recordTime = readDataFromKeys(data, 'ConnectInfor.RecordTime')
            cipher = readDataFromKeys(data,'TLS.ClientHello.CipherSuite')
            addCountToMap(cipherCount,cipher)
            print(json.dumps(data))
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
    print('serverSet', serverSet)
    print('clientSet', clientSet)
    # print('recordTimeSet', recordTimeSet)
    print('cipherCount',cipherCount)

def checkCipher(tablename,cipher):
    detail = {
        "query": {
            "match_phrase": {
                "TLS.ClientHello.CipherSuite": cipher
            }
        }
    }
    CountQuery(tablename,detail)


def checkCert(tablename,certname):
    detail = {
        "query": {
            "match_phrase": {
                "TLS.Cert": certname
            }
        }
    }
    CountQuery(tablename,detail)






if __name__=='__main__':

    checkCert('ssl_20180829','7047539AB110251CFC67A3DBBFD9AE95928A6333')
    # checkCipher('ssl_20180819','006B00FF')
