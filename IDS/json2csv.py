import json
import os
import pandas as pd
from multiprocessing import Pool
from ELModel import loadData

def isConnectOK(connect):
    if  'port.src' in connect['ConnectInfor']:
        if isServer(connect['ConnectInfor']['port.src']) or isServer(connect['ConnectInfor']['port.dst']):
            return True
    return False


def isServer(serverPort):
    return serverPort in [443,80]

def readConnectFromFiles(fileList,outname):
    pool = Pool(20)
    dataLists = pool.map(featuresFromConnectFile,fileList)
    result = []
    for data in dataLists:
        result.extend(data)
    df = pd.DataFrame(result)
    df.to_csv(outname,index=0)

    
def featuresFromConnectFile(filename):
    inf = open(filename,encoding='latin1')
    result = []
    for line in inf.readlines():
        try:
            connect = json.loads(line)
        except:
            line.replace('-nan','0')
            connect = json.loads(line)
        if isConnectOK(connect):
            featureData = connect2Features(connect)
            result.append(featureData)
    return result

def newFeatures(connect):
    clientIP = connect['ConnectInfor']['sIP']
    serverIP = connect['ConnectInfor']['dIP']
    sendByte = connect['ConnectInfor']['sBytes']
    recByte = connect['ConnectInfor']['dBytes']
    sendNum = connect['ConnectInfor']['sNum']
    recNum = connect['ConnectInfor']['dNum']
    sendPort = connect['ConnectInfor']['dPort']
    recPort = connect['ConnectInfor']['sPort']
    timestmp = connect['ConnectInfor']['StartTime']
    result = {
        'timestmp': timestmp,
        'clientIP': clientIP,
        'serverIP': serverIP,
        'sendByte': sendByte,
        'recByte': recByte,
        'sendNum': sendNum,
        'recNum': recNum,
        'sendPort': sendPort,
        'recPort': recPort,
        'flowNum': sendNum + recNum,
        'packetRatio': sendNum / (recNum + 0.01),
        'byteRatio': sendByte / (recByte + 0.01)

    }
    reSetSource(result)
    return result

def reSetSource(result):
    if isServer(result['sendPort']):
        result['sendByte'],result['recByte']  = result['recByte'],result['sendByte']
        result['sendNum'], result['recNum'] = result['recNum'], result['sendNum']
        result['clientIP'], result['serverIP'] = result['serverIP'], result['clientIP']
        result['sendPort'], result['recPort'] = result['recPort'], result['sendPort']

def newFeaturesFromConnectFile(filename):
    inf = open(filename,encoding='latin1')
    result = []
    for line in inf.readlines():
        connect = json.loads(line)
        result.append(newFeatures(connect))
    return result

def connect2Features(connect):
    clientIP = connect['ConnectInfor']['ip.src']
    serverIP = connect['ConnectInfor']['ip.dst']
    sendByte = connect['ConnectInfor']['Bytes.src']
    recByte = connect['ConnectInfor']['Bytes.dst']
    sendNum = connect['ConnectInfor']['Num.src']
    recNum = connect['ConnectInfor']['Num.dst']
    sendPort = connect['ConnectInfor']['port.src']
    recPort = connect['ConnectInfor']['port.dst']
    timestmp = connect['ConnectInfor']['StartTime']
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
    reSetSource(result)
    return result

def pku2csv():
    dirname = '/home/eta/pku/Connect/'
    fileList = [os.path.join(dirname, x) for x in os.listdir(dirname)]
    readConnectFromFiles(fileList,'pku.csv')

def scanner2csv():
    dirname = '/home/eta/attacks/json/'
    fileList = []
    for root,dir,names in os.walk(dirname):
        for name in names:
            if 'Connect' in root:
                fileList.append(os.path.join(root,name))
    readConnectFromFiles(fileList,'scanner.csv')

def loadWhite():
    dirname = '/home/eta/newjson/'
    fileList = []
    for root,dir,names in os.walk(dirname):
        for name in names:
            if 'Connect' in root:
                fileList.append(os.path.join(root,name))
    readConnectFromFiles(fileList,'white.csv')

def loadHttpAttack():
    result = newFeaturesFromConnectFile('attacks_connect_0827.txt')
    df = pd.DataFrame(result)
    df.to_csv('http_attack.csv',index=0)


def readTimeData():
    dataGen = loadData('connect_20180824')
    result = []
    cnt = 0
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            features = newFeatures(data)
            result.append(features)
            cnt+=1
        print(cnt)
    df = pd.DataFrame(result)
    df.to_csv('tsinghua.csv',index=0)

if __name__=='__main__':
    # pku2csv()
    # scanner2csv()
    # loadWhite()
    # loadHttpAttack()
    readTimeData()