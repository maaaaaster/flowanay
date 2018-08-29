from ELModel import loadData
from utils import readDataFromKeys

def checkCert(tablename,certname):
    serverSet,clientSet,recordTimeSet = set(),set(),set()
    detail = {
        "query": {
            "match_phrase": {
                "TLS.Cert": certname
            }
        }
    }
    dataGen = loadData(table=tablename, detail=detail)
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            firstIP = readDataFromKeys(data,'ConnectInfor.first')
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            recordTime = readDataFromKeys(data, 'ConnectInfor.RecordTime')
            print(readDataFromKeys(data, 'ConnectInfor'))
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
    print('serverSet', serverSet)
    print('clientSet', clientSet)
    print('recordTimeSet', recordTimeSet)




if __name__=='__main__':
    certname = '863A502B3FD37E9B837B8B5A39599958FADF1B70'
    # certname = 'E74220B93FF9342779CE66F6A233356EA11614C8'
    checkCert('ssl_20180819',certname)

