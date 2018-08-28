import json

def featuresFromConnectFile(filename):
    inf = open(filename)
    for line in inf.readlines():
        connect = json.loads(line)
        featureData = hwConnect2Features(connect)
        break

def hwConnect2Features(connect):
    sendByte = connect['ConnectInfor']['Bytes.dst']
    recByte = connect['ConnectInfor']['Bytes.src']
    sendNum = connect['ConnectInfor']['Num.dst']
    recNum = connect['ConnectInfor']['Num.src']
    print(sendByte,sendNum,recNum,recByte)


if __name__=='__main__':
    featuresFromConnectFile('/home/eta/pku/Connect/0817_2.pcap4199_DjPQUc')