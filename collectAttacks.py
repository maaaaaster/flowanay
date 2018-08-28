from ELModel import loadData
from utils import readDataFromKeys
import json,os
detail = {

}
dataists = loadData(table='http_20180825',detail=detail)

ipset = set()
for datalist in dataists:
    for data in datalist:
        data = data['_source']
        get = readDataFromKeys(data,keys='HTTP_Client.GET',default='')
        ip = readDataFromKeys(data,'ConnectInfor.first')
        if 'group_concat' in get.lower():
            print(ip,get)
            ipset.add(ip)
    if len(ipset)>10:
        break
print(ipset)
connectKeySet = set()
dataists = loadData(table='http_20180825',detail=detail)
# ipset = {'42.189.246.170', '166.111.4.100', '58.250.125.124', '103.26.77.218', '106.38.241.188', '58.250.125.100', '111.202.101.118', '222.186.190.163'}
for ip in ipset:
    detail = detail = {
        "query": {
            'match':{
                'ConnectInfor.sIP':ip
            }
        }
    }
    for datalist in dataists:
        for data in datalist:
            data = data['_source']
            key = readDataFromKeys(data, keys='ConnectInfor.ConnectKeyID', default='')
            connectKeySet.add(key)
        if len(connectKeySet)>10000:
            break
with open('connect_keys.txt','w+') as outf:
    for connectKey in connectKeySet:
        outf.write(connectKey+'\n')