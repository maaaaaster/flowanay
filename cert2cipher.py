from ELModel import loadData
from utils import readDataFromKeys,addCountToMap
import json
def saveGraph():
    result = {}
    count = 0
    outf = open('data/graph_test.txt','w+')
    dataGen = loadData('ssl_20180819',["ConnectInfor.first", "TLS.Cert", "TLS.ClientHello.CipherSuite"])
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            cipher = readDataFromKeys(data,'TLS.ClientHello.CipherSuite')
            # ip = readDataFromKeys(data,'ConnectInfor.first')
            cert = readDataFromKeys(data,'TLS.Cert')
            if cipher is None or cert is None or len(cert) == 0:
                continue
            cert = cert[0]
            key = cipher+'_'+cert
            addCountToMap(result,key)
        count+=len(datalist)
        print(count)
        json.dump(result,outf)

saveGraph()