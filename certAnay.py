from ELModel import loadData
from utils import readDataFromKeys
from FetchData import *
def checkCert(day,table,certname):
    dataList = fetchWithPayload(makePayload(day, table, match={"TLS.Cert": certname}))
    serverSet,clientSet,recordTimeSet = set(),set(),set()
    for data in dataList:
        data = data['_source']
        print(data['TLS']['Cert'])
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
    certname = '0F929C1BDEF5A02C9B79995AE3CBCB0C363A05DC'
    checkCert('20180819','ssl',certname)

