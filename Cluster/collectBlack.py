import os
import json
from multiprocessing import Pool
import pandas as pd
from domain import psl,loadWhiteMap

whiteSet = loadWhiteMap()

def readDataFromKeys(data,keys,default=None):
    temp = data.copy()
    for key in keys.split('.'):
        if key in temp:
            temp = temp[key]
        else:
            return default
    return temp

def loadDNSFile(filename):
    result = {}
    for line in open(filename,encoding='latin1').readlines():
        data = json.loads(line)
        domain = readDataFromKeys(data, "DNS.Queries",None)
        answers = readDataFromKeys(data, "DNS.Answers",None)
        if domain is None or answers is None:
            continue
        domain = domain[0]['Name']
        for answer in answers:
            if answer['Type'] == 1:
                ip = answer['Value']
                if ip not in result:
                    result[ip] = set()
                result[ip].add(domain)
    return result

def loadDNSFiles():
    filelist =[]
    for root,sub,names in os.walk('/home/eta/newjson'):
        if 'DNS' in root and 'black' in root:
            for name in names:
                filelist.append(os.path.join(root,name))
    p = Pool(20)
    ipSets = p.map(loadDNSFile,filelist)
    p.close()
    p.join()
    result = {}
    for ipset in ipSets:
        for ip in ipset:
            if ip not in result:
                result[ip] = set()
            result[ip] = result[ip] | ipset[ip]
    for ip in result:
        result[ip] = list(result[ip])
    json.dump(result,open('ip2domain.json','w+'))

def cert2json(df):
    result = {}
    def addToDict(x):
        domains = set()
        domains.add(psl.get_public_suffix(x['CN']))
        for domain in x['SAN'].split(','):
            domains.add(psl.get_public_suffix(domain))
        result[x['hash']] = domains
    df.apply(addToDict,axis=1)
    return result

def combineData():
    ip2Domain = json.load(open('data/ip2domain.json'))
    for ip in ip2Domain:
        domainSet = set()
        for domain in ip2Domain[ip]:
            domainSet.add(psl.get_public_suffix(domain))
        ip2Domain[ip] = domainSet
    blackCerts = pd.read_csv('data/black_certs.csv')
    cert2Domain = cert2json(blackCerts)
    rawConnect = pd.read_csv('data/black_cluster_raw.csv')
    sameIPSet = {}
    hashMap = {}
    def checkConnect(data):
        serverIP = data['serverIP']
        hash = data['cert']
        if serverIP in ip2Domain:
            passiveDomainSet = ip2Domain[serverIP]
            certDomainSet = cert2Domain[hash]
            sameDomains = certDomainSet & passiveDomainSet & whiteSet
            if hash not in hashMap:
                hashMap[hash] = {
                    'serverIP':set(),
                    'serverDomains':set(),
                }
                hashMap[hash]['serverIP'].add(serverIP)
                hashMap[hash]['serverDomains'] = hashMap[hash]['serverDomains'] & passiveDomainSet
            if len(sameDomains)>0:
                sameIPSet[serverIP] = sameDomains
                print(sameDomains)
                return -1
                # print(serverIP,sameDomains)
        return 1
    rawConnect['isMalware'] = rawConnect.apply(checkConnect,axis=1)
    for ip in sameIPSet:
        print(ip,sameIPSet[ip])
    result = []
    for hash in hashMap:
        result.append({
            'hash':hash,
            'serverIP': ';'.join(list(hashMap[hash]['serverIP'])),
            'serverDomains': ';'.join(list(hashMap[hash]['serverDomains'])),
            'certDomains': ';'.join(list(cert2Domain[hash]))
            })
    pd.DataFrame(result).to_csv('data/blackCheck.csv')
    rawConnect.to_csv('test.csv')

def checkIP(data):
     return data.drop_duplicates().count()

def joinFromRaw(inname,outname):
    df = pd.read_csv(inname)
    edge_count = df.groupby(['cert', 'cipher', 'extensions'], as_index=False).agg({'clientIP': checkIP, 'serverIP': 'count'})
    edge_count.rename(columns={'serverIP': 'cnt', 'clientIP': 'ipCnt'}, inplace=True)
    edge_count.to_csv(outname, index=False)
if __name__=='__main__':
    combineData()
    # joinFromRaw('/home/OpenCode/FlowAnay/Cluster/data/20180909.csv','/home/OpenCode/FlowAnay/Cluster/data/test_20180909.csv')
    # joinFromRaw('test.csv','test_black_cluster.csv')

