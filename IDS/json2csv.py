import json

def featuresFromConnectFile(filename):
    inf = open(filename)
    for line in inf.readlines():
        connect = json.loads(line)
        featureData = hwConnect2Features(connect)
        break

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
        'recPort':recPort
    }
    return result


if __name__=='__main__':
    featuresFromConnectFile('/home/eta/pku/Connect/0817_2.pcap4199_DjPQUc')