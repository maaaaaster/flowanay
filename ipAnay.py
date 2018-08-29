from ELModel import loadData
from utils import readDataFromKeys
def checkIP(tablename,ip):
    detail = {
        "query": {
            "match_phrase": {
                "ConnectInfor.ServerIP": ip
                # "ConnectInfor.dIP": ip

            }
        }
    }
    dataGen = loadData(table=tablename, detail= detail )
    serverSet = set()
    clientSet = set()
    recordTimeSet = set()
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            host = readDataFromKeys(data,'HTTP_Client.Host')
            ua = readDataFromKeys(data,'HTTP_Client.User-Agent')

            firstIP = readDataFromKeys(data,'ConnectInfor.first')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            recordTime = readDataFromKeys(data, 'ConnectInfor.RecordTime')
            print(firstIP,host,ua,recordTime)
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
    print(serverSet)
    print(clientSet)
    # print(recordTimeSet)


if __name__=='__main__':
    tablename = 'http_20180825'
    # ipname = '166.111.5.195'
    # ipname = '185.156.3.20'
    # ipname = '91.149.186.229'
    ipname = '169.229.150.100'
    checkIP(tablename,ipname)