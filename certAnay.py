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
    checkCert('ssl_20180829','61749734B3246F1584029DEB4F5276C64DA00ADA')
    # checkCipher('ssl_20180829','C030C02CC028C024C014C00A00A3009F006B006A0039003800880087C032C02EC02AC026C00FC005009D003D00350084C02FC02BC027C023C013C00900A2009E0067004000330032009A009900450044C031C02DC029C025C00EC004009C003C002F009600410007C011C007C00CC00200050004C012C00800160013C00DC003000A0015001200090014001100080006000300FF')
