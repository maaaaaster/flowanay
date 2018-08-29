from ELModel import loadData
from utils import readDataFromKeys
def checkPort(tablename,port):
    sources = [ "ConnectInfor", "TLS.Cert", "TLS.ClientHello.CipherSuite"]
    detail = {
        "query": {
            'bool':{
                'should':{
                    "match_phrase": {
                        "ConnectInfor.sPort": port
                    },
                    "match_phrase": {
                        "ConnectInfor.dPort": port
                    }
                }
            }

        }
    }
    dataGen = loadData(table=tablename,sources=sources, detail= detail )
    serverSet = set()
    clientSet = set()
    recordTimeSet = set()
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            print(data)
            firstIP = readDataFromKeys(data,'ConnectInfor.first')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            recordTime = readDataFromKeys(data, 'ConnectInfor.RecordTime')
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
    print(serverSet)
    print(clientSet)
    print(recordTimeSet)


if __name__=='__main__':
    checkPort('ssl_20180819','3389')