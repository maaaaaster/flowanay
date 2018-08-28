import json
import os
import time
from OpenSSL import crypto
from multiprocessing import Pool
import pandas as pd


def certTime2int(timeb):
    strTime = timeb.decode('utf-8')
    timeArray = time.strptime(strTime, "%Y%m%d%H%M%SZ")
    return int(time.mktime(timeArray))


def loadCertFile(filename):
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, open(filename, 'rb').read())
    ddl = certTime2int(cert.get_notAfter())
    birth = certTime2int(cert.get_notBefore())
    duration = int((ddl - birth + 1) / 86400)
    result = {
        'filename': filename,
        'cert_duration': duration,
        'self_signed': 0,
        'subject': cert.get_subject()
    }

    if cert.get_issuer().hash() == cert.get_subject().hash():
        result['self_signed'] = 1
    else:
        result['self_signed'] = 0

    result['SAN'] = ''
    result['isCA'] = 0
    for i in range(cert.get_extension_count()):
        shortname = cert.get_extension(i).get_short_name()
        if shortname == b'subjectAltName':
            content = str(cert.get_extension(i))
            result['SAN'] = content
        elif shortname == 'basicConstraints':
            content = str(cert.get_extension(i))
            if "TRUE" in content:
                result['isCA'] = 1
    return result


def loadUsedCerts(sslDir):
    result = set()
    if not os.path.exists(sslDir):
        return result
    for name in os.listdir(sslDir):
        filename = os.path.join(sslDir, name)
        for line in open(filename).readlines():
            data = json.loads(line)
            if 'TLS' in data and 'Cert' in data['TLS']:
                certname = data['TLS']['Cert'][0]
                result.add(certname)
    return result


def certInDir(dirname):
    certDir = os.path.join(dirname, 'Cert/5')
    sslDir = os.path.join(dirname, 'Extract/5/SSL')
    usedCerts =loadUsedCerts(sslDir)
    hash2path = {}
    for name in usedCerts:
        hash2path[name] = os.path.join(certDir,name)+'.cert'
    return hash2path

def dirList2certMap(dirLists):
    pool = Pool(20)
    hash2pathLists = pool.map(certInDir, dirLists)
    pool.close()
    pool.join()
    result = {}
    for hash2pathList in hash2pathLists:
        result.update(hash2pathList)
    return result



def filterCerts(basedir = '/home/eta/json/'):
    blackDirs = []
    whiteDirs = []
    result = []
    for name in os.listdir(basedir):
        dirname = os.path.join(basedir, name)
        if 'black' in name:
            blackDirs.append(dirname)
        else:
            whiteDirs.append(dirname)
    blackCertMap = dirList2certMap(blackDirs)
    whiteCertMap = dirList2certMap(whiteDirs)
    toCheck = set(blackCertMap.keys()) & set(whiteCertMap.keys())#set(blackCertMap.keys())-set(whiteCertMap.keys())
    for certHash in toCheck:
        certPath = blackCertMap[certHash]
        result.append(loadCertFile(certPath))
    df = pd.DataFrame(result)
    df.to_csv('/home/eta/white_certs.csv')


def filterhosts(dirname):
    result = set()
    httpDir =os.path.join(dirname,'Extract/5/HTTP')
    if not os.path.exists(httpDir):
        return result
    for name in os.listdir(httpDir):
        filename = os.path.join(httpDir, name)
        for line in open(filename,encoding='latin1').readlines():
            data = json.loads(line)
            if 'HTTP_Client' in data and 'Host' in data['HTTP_Client']:
                host = data['HTTP_Client']['Host']
                result.add(host)
    hostList = ';'.join(list(result))
    return {'dirname':dirname, 'host':hostList}


def dirList2HostMap(basedir = '/home/eta/json/'):
    dirLists = []
    for name in os.listdir(basedir):
        dirname = os.path.join(basedir, name)
        if 'black' in name:
            dirLists.append(dirname)
    pool = Pool(20)
    hostList = pool.map(filterhosts, dirLists)
    pool.close()
    pool.join()
    df = pd.DataFrame(hostList)
    df.to_csv('/home/eta/hostmap.csv',index=0)

if __name__=='__main__':
    filterCerts()
    # dirList2HostMap()