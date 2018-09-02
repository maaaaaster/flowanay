from OpenSSL import crypto
import time
import json
from multiprocessing import Pool
import pandas as pd
import os

def certTime2int(timeb):
    strTime = timeb.decode('utf-8')
    timeArray = time.strptime(strTime, "%Y%m%d%H%M%SZ")
    return int(time.mktime(timeArray))

def certname2hash(filename):
    return filename.split('/')[-1].split('.')[0]

def loadCertFile(filename):
    result = {}
    hashname = certname2hash(filename)
    result['hash'] = hashname
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, open(filename, 'rb').read())
    ddl = certTime2int(cert.get_notAfter())
    birth = certTime2int(cert.get_notBefore())
    duration = int((ddl - birth + 1) / 86400)
    result['cert_duration'] = duration
    result['self_signed'] = 0
    # print(cert.get_issuer(),cert.get_subject())
    if cert.get_issuer().hash() == cert.get_subject().hash():
        result['self_signed'] = 1
    else:
        result['self_signed'] = 0

    result['SAN_count'] = 0
    result['isCA'] = 0
    result['SAN'] = 'None'

    for i in range(cert.get_extension_count()):
        shortname = cert.get_extension(i).get_short_name()
        if shortname == b'subjectAltName':
            content = str(cert.get_extension(i))
            result['SAN_count'] = len(content.split(','))
            result['SAN'] = content
        elif shortname == 'basicConstraints':
            content = str(cert.get_extension(i))
            if "TRUE" in content:
                result['isCA'] = 1
    return result




def readCertFromFile(basicdir,inname,outname):
    hashSet = set(json.load(open(inname)))
    result = []
    allLen = len(hashSet)
    for root,sub,names in os.walk(basicdir):
        left = len(hashSet)
        if left==0:
            break
        if 'Cert' not in root:
            continue
        for name in names:
            filename = os.path.join(root,name)
            hashname = certname2hash(filename)
            if hashname in hashSet:
                hashSet.remove(hashname)
                result.append(loadCertFile(filename))
                left = len(hashSet)
                print("left %d / %d"%(left,allLen))

    df = pd.DataFrame(result)
    df.to_csv(outname,index=False)

if __name__=='__main__':
    readCertFromFile('/Tsinghua_LanProbe/FlowLog/Cert','/home/OpenCode/collectCert/ssl_20180827_certs.txt','/home/OpenCode/collectCert/ssl_20180827_certs.csv')