import json
import pandas as pd
from ELModel import loadData
from utils import readDataFromKeys, addCountToMap


def loadIPSet():
    detail = {}
    dataLists = loadData(table="ssl_20180827",detail=detail)
    result80 = []
    result443 = []
    count = 0
    for datalist in dataLists:
        for data in datalist:
            data = data["_source"]
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            dIP = readDataFromKeys(data, 'ConnectInfor.dIP')
            sIP = readDataFromKeys(data, 'ConnectInfor.sIP')
            dPort = readDataFromKeys(data, 'ConnectInfor.dPort')
            sPort = readDataFromKeys(data, 'ConnectInfor.sPort')
            dNum = readDataFromKeys(data, 'ConnectInfor.dNum')
            sNum = readDataFromKeys(data, 'ConnectInfor.sNum')
            sBytes = readDataFromKeys(data, 'ConnectInfor.sBytes')
            dBytes = readDataFromKeys(data, 'ConnectInfor.dBytes')
            StartTime = readDataFromKeys(data, 'ConnectInfor.StartTime')
            if dPort in [80,443]:
                clientIP = sIP
                serverIP = dIP
                clientPort = sPort
                serverPort = dPort
            else:
                clientIP = dIP
                serverIP = sIP
                clientPort = dPort
                serverPort = sPort
                dNum,sNum = sNum,dNum
                dBytes,sBytes = sBytes,dBytes
            features = {
                    'clientIP': clientIP,
                    'serverIP': serverIP,
                    'clientPort': clientPort,
                    'serverPort': serverPort,
                    'dBytes':dBytes,
                    'sBytes':sBytes,
                    'dNum':dNum,
                    'sNum': sNum,
                    'StartTime':StartTime
                }
            if dPort==80:
                result80.append(features)
            elif dPort==443:
                result443.append(features)

        count+=len(datalist)
        print(count)
    pd.DataFrame(result80).to_csv('80attack_test_0823.csv',index=0)
    pd.DataFrame(result443).to_csv('443attack_test_0823.csv', index=0)


if __name__=='__main__':
    loadIPSet()