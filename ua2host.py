from ELModel import loadData
from utils import readDataFromKeys,addCountToMap,addSetToMap,saveCount,saveMap
import json
import pandas as pd


def saveGraph(tablename):
    hostMap = {}
    ipMap = {}
    hostCount = {}
    count = 0
    dataGen = loadData(tablename)
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            host = readDataFromKeys(data, keys="HTTP_Client.Host", default=None)
            ip = readDataFromKeys(data, keys="ConnectInfor.ServerIP", default=None)
            ua = readDataFromKeys(data, keys="HTTP_Client.User-Agent", default=None)
            if ua is None or host is None:
                continue
            addCountToMap(hostCount,host)
            addSetToMap(hostMap,host,ua)
            addSetToMap(ipMap,ip,ua)
        count+=len(datalist)
        print(count)
    saveMap(hostMap, 'data/host2ua_%s.csv'%tablename)
    saveMap(ipMap, 'data/ip2ua_%s.csv'%tablename)
    saveCount(hostCount, 'data/hostCount_%s.csv'%tablename)

def filterGraph(tablename):
    oneUAHosts = set()
    with open('data/ip2ua_%s.csv'%tablename) as inf:
        for line in inf.readlines():
            index = line.find(',')
            host = line[:index]
            uas = line[index+1:].split('\t')
            if len(uas)==1:
                oneUAHosts.add(host)
                print(host,uas)
    print(len(oneUAHosts))
    # df = pd.read_csv('data/hostCount_%s.csv'%tablename)
    # oneTimeHost = set(list(df[df['count']==1]['key']))
    # toCheck = oneUAHosts - oneTimeHost
    # for host in toCheck:
    #     print(host)


# saveGraph('http_20180825')
filterGraph('http_20180825')