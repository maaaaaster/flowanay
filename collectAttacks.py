from ELModel import loadData
from utils import readDataFromKeys,addCountToMap
import json,os
from FetchData import fetchWithPayload,makePayload


def loadIPSet():
    detail = {}
    dataists = loadData(table="http_20180825",detail=detail)
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
    ipset = ["news.tsinghua.edu.cn_58.250.125.124", "news.tsinghua.edu.cn_111.202.101.118", "www.law.tsinghua.edu.cn_222.186.190.163", "news.tsinghua.edu.cn_58.250.125.100", "news.tsinghua.edu.cn_106.38.241.188", "www.sem.tsinghua.edu.cn_42.189.246.170", "auth.cic.tsinghua.edu.cn_222.186.190.163"]
    ipset.extend(['www.imir.tsinghua.edu.cn_219.243.208.20', 'smarx.tsinghua.edu.cn_219.243.208.20', 'www.arts.tsinghua.edu.cn_219.243.208.20', 'www.ime.tsinghua.edu.cn_219.243.208.20', 'www.sss.tsinghua.edu.cn_219.243.208.20', 'www.lsx.tsinghua.edu.cn_219.243.208.20', 'guofang.tsinghua.edu.cn_219.243.208.20', 'www.castu.tsinghua.edu.cn_219.243.208.20', 'www.ad.tsinghua.edu.cn_219.243.208.20', 'www.dpi.tsinghua.edu.cn_219.243.208.20', 'math.tsinghua.edu.cn_219.243.208.20', 'www.dps.tsinghua.edu.cn_219.243.208.20', 'stat.download.xunlei.com:8099_166.111.127.16', 'www.ee.tsinghua.edu.cn_219.243.208.20', 'www.au.tsinghua.edu.cn_219.243.208.20', 'lad.arch.tsinghua.edu.cn_219.243.208.20', 'www.env.tsinghua.edu.cn_219.243.208.20'])
    outf = open('attacks.txt','w+')
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

        dataists = loadData(table="http_20180825", detail=detail)
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
    with open("connect_keys.txt","w+") as outf:
        for connectKey in connectKeySet:
            outf.write(connectKey+"\n")

def loadFromKeys():
    outf = open('attacks.txt','w+')
    for line in open("connect_keys.txt").readlines():
        key = line.strip()
        match = {"ConnectInfor.ConnectKeyID": key}
        http_payload = makePayload("20180825","http",match)
        connect_payload = makePayload("20180825", "connect", match)
        http_data = fetchWithPayload(http_payload)[0]["_source"]
        get = readDataFromKeys(http_data, keys="HTTP_Client.GET", default="")
        host = readDataFromKeys(http_data, keys="HTTP_Client.Host", default="")
        connect_data = fetchWithPayload(connect_payload)[0]["_source"]
        connect_data['http'] = {'host':host,'get':get}

        outf.write(json.dumps(connect_data)+'\n')

if __name__=="__main__":
    loadIPSet()
    # loadConnectKey()
    # loadFromKeys()

