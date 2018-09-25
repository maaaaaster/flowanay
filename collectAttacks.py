import json

from ELModel import loadData
from FetchData import fetchWithPayload, makePayload
from utils import readDataFromKeys, addCountToMap


def loadIPSet():
    detail = {}
    dataists = loadData(table="http_20180918",detail=detail)
    ipset = {}
    for datalist in dataists:
        for data in datalist:
            data = data["_source"]
            get = readDataFromKeys(data,keys="HTTP_Client.GET",default="")
            ip = readDataFromKeys(data,"ConnectInfor.first")
            host = readDataFromKeys(data, keys="HTTP_Client.Host", default="")
            getLowser = get.lower()
            if "alert"  in  getLowser and 'script' in getLowser:
                print(host,ip,get)
                key = host+"_"+ip
                addCountToMap(ipset,key)
        print(ipset.keys())
    return ipset

def loadConnectKey():
    connectKeySet = set()
    ipset = ['www.chemeng.tsinghua.edu.cn_219.243.208.20', 'www.sss.tsinghua.edu.cn_219.243.208.20', 'www.ime.tsinghua.edu.cn_219.243.208.20', 'guofang.tsinghua.edu.cn_219.243.208.20', 'eproxy2.lib.tsinghua.edu.cn_223.72.75.87']
    outf = open('attacks_0918.txt','w+')
    for ip in ipset:
        vals = ip.strip().split("_")
        detail = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"ConnectInfor.first": vals[1]}},
                        {"term": {"HTTP_Client.Host": vals[0]}}
                    ]
                }
            }
        }

        dataists = loadData(table="http_20180918", detail=detail)
        for datalist in dataists:
            for data in datalist:
                data = data["_source"]
                key = readDataFromKeys(data, keys="ConnectInfor.ConnectKeyID", default="")
                get = readDataFromKeys(data, keys="HTTP_Client.GET", default="")
                ip = readDataFromKeys(data, "ConnectInfor.first")
                host = readDataFromKeys(data, keys="HTTP_Client.Host", default="")
                print(host,ip,get)
                outf.write(json.dumps(data)+'\n')
                connectKeySet.add(key)
    with open("connect_keys_0918.txt","w+") as outf:
        for connectKey in connectKeySet:
            outf.write(connectKey+"\n")

def loadFromKeys():
    outf = open('attacks_connect_0918.txt','w+')
    for line in open("connect_keys_0918.txt").readlines():
        key = line.strip()
        match = {"ConnectInfor.ConnectKeyID": key}
        # http_payload = makePayload("20180825","http",match)
        # http_data = fetchWithPayload(http_payload)[0]["_source"]
        # get = readDataFromKeys(http_data, keys="HTTP_Client.GET", default="")
        # host = readDataFromKeys(http_data, keys="HTTP_Client.Host", default="")
        # connect_data['http'] = {'host':host,'get':get}
        connect_payload = makePayload("20180918", "connect", match)
        result = fetchWithPayload(connect_payload)
        if len(result)>0:
            connect_data = result[0]["_source"]
            print(connect_data,key)
            outf.write(json.dumps(connect_data)+'\n')

if __name__=="__main__":
    # loadIPSet()
    # loadConnectKey()
    loadFromKeys()

