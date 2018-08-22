from ELModel import loadData
from utils import readDataFromKeys
def checkIP(tablename,ip):
    sources = [ "ConnectInfor", "TLS.Cert", "TLS.ClientHello.CipherSuite"]
    detail = {
        "query": {
            "match_phrase": {
                "ConnectInfor.dIP": ip
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
    tablename = 'ssl_20180821'
    # ipname = '166.111.5.195'
    # ipname = '185.156.3.20'
    ipname = '91.149.186.229'
    ipname = '166.111.5.195'
    checkIP(tablename,ipname)