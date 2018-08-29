import json
import os
import pandas as pd
from multiprocessing import Pool

def pku2csv(dirname):
    filelist = [os.path.join(dirname, x) for x in os.listdir(dirname)]
    pool = Pool(20)
    dataLists = pool.map(featuresFromConnectFile,filelist)
    result = []
    for data in dataLists:
        result.extend(data)
    df = pd.DataFrame(result)
    df.to_csv('pku.csv',index=0)

def featuresFromConnectFile(filename):
    inf = open(filename,encoding='latin1')
    result = []
    for line in inf.readlines():
        connect = json.loads(line)
        featureData = hwConnect2Features(connect)
        result.append(featureData)
    return result
def hwConnect2Features(connect):
    clientIP = connect['ConnectInfor']['ip.src']
    serverIP = connect['ConnectInfor']['ip.dst']
    sendByte = connect['ConnectInfor']['Bytes.src']
    recByte = connect['ConnectInfor']['Bytes.dst']
    sendNum = connect['ConnectInfor']['Num.src']
    recNum = connect['ConnectInfor']['Num.dst']
    sendPort = connect['ConnectInfor']['port.src']
    recPort = connect['ConnectInfor']['port.dst']
    timestmp = connect['ConnectInfor']['StartTime']
    if serverIP != connect['ConnectInfor']['ServerIP']:
        sendByte,recByte = recByte,sendByte
        sendNum,recNum = recNum,sendNum
        clientIP,serverIP = serverIP,clientIP
        sendPort,recPort = recPort,sendPort
    result = {
        'timestmp':timestmp,
        'clientIP':clientIP,
        'serverIP':serverIP,
        'sendByte':sendByte,
        'recByte':recByte,
        'sendNum':sendNum,
        'recNum':recNum,
        'sendPort':sendPort,
        'recPort':recPort,
        'flowNum':sendNum + recNum,
        'packetRatio':sendNum / (recNum + 0.01),
        'byteRatio': sendByte / (recByte + 0.01)

    }
    return result


if __name__=='__main__':
    pku2csv('/home/eta/pku/Connect/')