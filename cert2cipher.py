from ELModel import loadData
from utils import readDataFromKeys,addCountToMap,addSetToMap
import json
import pandas as pd

def saveMap(mapData,outname):
    outf = open(outname,'w+')
    outf.write('cert,ciphers\n')
    for key in mapData:
        ciphers = ';'.join(list(mapData[key]))
        line = '%s,%s\n'%(key,ciphers)
        outf.write(line)
def saveGraph():
    result = {}
    certMap = {}
    cipherMap = {}
    count = 0
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
            addSetToMap(certMap,cert,cipher)
            addSetToMap(cipherMap, cipher, cert)
        count+=len(datalist)
        print(count)
        # print(len(list(certMap.keys())))
        # if count < 100000:
        #     continue
        # for cert,ciphers in sorted(certMap.items(),key=lambda x:len(x[1]),reverse=False)[:100]:
        #     if len(ciphers)>1:
        #         break
        #     print(cert)
        #
        # json.dump(result,outf)
    saveMap(certMap,'data/cert2ciphers')
    saveMap(cipherMap, 'data/cipher2Certs')

def filterGraph():
    df = pd.read_csv('data/cert2ciphers')
    df['cipher_num'] = df['ciphers'].map(lambda x:x.count(';'))
    certs = set(df[df['cipher_num']==0]['cert'])
    df2 = pd.read_csv('data/cipher2Certs')
    df2['cipher_num'] = df['ciphers'].map(lambda x: x.count(';'))
    certs2 = set(df2[df2['cipher_num']==0]['ciphers'])
    print(certs&certs2)


# saveGraph()
filterGraph()