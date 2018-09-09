from ELModel import loadData
from utils import readDataFromKeys
import json

def checkIP(tablename,ip):
    detail = {
        "query": {
            "bool":{
                "should": [
                    {"term": {"ConnectInfor.sIP": ip}},
                    {"term": {"ConnectInfor.dIP": ip}}
                ]
            }

        }
    }
    # detail = {
    #     "query": {
    #         "match": {
    #             "ConnectInfor.sIP": ip
    #         }
    #     }
    # }
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
            cert = readDataFromKeys(data,'TLS.Cert')
            # print(firstIP,host,ua,recordTime,cert)
            serverSet.add(serverIP)
            clientSet.add(firstIP)
            recordTimeSet.add(recordTime)
            get = readDataFromKeys(data,keys="HTTP_Client.GET",default="")
            if host is not None:
                print(host+get)
            else:
                print(serverIP)
    print(serverSet)
    print(clientSet)
    # print(recordTimeSet)


if __name__=='__main__':
    tablename = 'http_20180824'
    # ipname = '166.111.5.195'
    # ipname = '185.156.3.20'
    # ipname = '91.149.186.229'
    # ipname = '202.162.108.57'
    ipname = '2402:f000:1:1501:200:5efe:d220:96a0'
    checkIP(tablename,ipname)