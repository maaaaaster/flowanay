from ELModel import loadData
from utils import readDataFromKeys,addCountToMap,addSetToMap,saveCount,saveMap
import pandas as pd
import json
from multiprocessing import  Pool

def tlsCollect(tablename):
    result = []
    count = 0
    dataGen = loadData(tablename,["ConnectInfor", "TLS.Cert", "TLS.ClientHello.CipherSuite","TLS.ClientHello.Extension.List"])
    for datalist in dataGen:
        for data in datalist:
            data = data['_source']
            cipher = readDataFromKeys(data,'TLS.ClientHello.CipherSuite')
            cert = readDataFromKeys(data,'TLS.Cert')
            if cipher is None or cert is None or len(cert) == 0:
                continue
            cert = cert[0]
            serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
            dIP = readDataFromKeys(data, 'ConnectInfor.dIP')
            sIP = readDataFromKeys(data, 'ConnectInfor.sIP')
            dPort = readDataFromKeys(data, 'ConnectInfor.dPort')
            sPort = readDataFromKeys(data, 'ConnectInfor.sPort')
            if dIP == serverIP:
                clientIP = sIP
                clientPort = sPort
                serverPort = dPort
            else:
                clientIP = dIP
                clientPort = dPort
                serverPort = sPort
            serverName = readDataFromKeys(data, 'TLS.ClientHello.Extension.ServerName','NotExist')
            extensions = readDataFromKeys(data, 'TLS.ClientHello.Extension.List',[])
            StartTime = readDataFromKeys(data, 'ConnectInfor.StartTime')
            extensionTypes = []
            for extensionData in extensions:
                extensionTypes.append(str(extensionData['Type']))
            if len(extensionTypes)==0:
                extensionTypes.append('None')
            extensionTypes.sort()
            extensions = ';'.join(extensionTypes)

            result.append({
                'clientIP':clientIP,
                'serverIP':serverIP,
                'clientPort':clientPort,
                'serverPort':serverPort,
                'serverName':serverName,
                'extensions':extensions,
                'cipher':cipher,
                'cert':cert,
                'startTime':StartTime

            })
        count+=len(datalist)
        print(count)
    df = pd.DataFrame(result)
    df.to_csv('data/'+tablename+'_raw.csv',index=0)

def graph_key(data):

    key = data['cert']+'/'+data['cipher']
    if data['extensions'] is not None:
        key = key +'_' +data['extensions']
    return key

def checkIP(data):
    return data.drop_duplicates().count()

def csv2graph(dates):
    concatData = []
    for day in dates:
        filename = 'data/ssl_2018%s_raw.csv'%day
        df = pd.read_csv(filename)
        # df['key'] = df.apply(graph_key, axis = 1)
        edge_count = df.groupby(['cert','cipher','extensions'], as_index=False).agg({'clientIP':checkIP,'serverIP':'count'})
        edge_count.rename(columns={'serverIP': 'cnt', 'clientIP': 'ipCnt'}, inplace=True)
        print(edge_count)
        concatData.append(edge_count)
    print('startConcat')
    data = pd.concat(concatData)
    print('stopConcat')
    data =data.groupby(['cert','cipher','extensions'], as_index=False).agg({'cnt': 'sum','ipCnt':'max'})
    data.to_csv('ssl_graph_raw.csv',index=False)
    data = data[data.cnt>1]
    data.to_csv('ssl_graph.csv', index=False)

def graph2edgefile(graphfile,edgefile):
    data = pd.read_csv(graphfile)
    outf = open(edgefile,'w+')
    for key in list(data['key']):
        vals = key.split('/')
        cert = vals[0]
        cipher = vals[1]
        outf.write('%s %s\n'%(cert,cipher))

def loadFromFile(filename):
    result = []
    count = 0
    for line in open(filename):
        data = json.loads(line)
        cipher = readDataFromKeys(data, 'TLS.ClientHello.CipherSuite')
        cert = readDataFromKeys(data, 'TLS.Cert')
        if cipher is None or cert is None or len(cert) == 0:
            continue
        cert = cert[0]
        serverIP = readDataFromKeys(data, 'ConnectInfor.ServerIP')
        dIP = readDataFromKeys(data, 'ConnectInfor.dIP')
        sIP = readDataFromKeys(data, 'ConnectInfor.sIP')
        dPort = readDataFromKeys(data, 'ConnectInfor.dPort')
        sPort = readDataFromKeys(data, 'ConnectInfor.sPort')
        StartTime = readDataFromKeys(data, 'ConnectInfor.StartTime')
        if dIP == serverIP:
            clientIP = sIP
            clientPort = sPort
            serverPort = dPort
        else:
            clientIP = dIP
            clientPort = dPort
            serverPort = sPort
        serverName = readDataFromKeys(data, 'TLS.ClientHello.Extension.ServerName', 'NotExist')
        extensions = readDataFromKeys(data, 'TLS.ClientHello.Extension.List', [])
        extensionTypes = []
        for extensionData in extensions:
            extensionTypes.append(str(extensionData['Type']))
        if len(extensionTypes) == 0:
            extensionTypes.append('None')
        extensionTypes.sort()
        extensions = ';'.join(extensionTypes)

        result.append({
            'clientIP': clientIP,
            'serverIP': serverIP,
            'clientPort': clientPort,
            'serverPort': serverPort,
            'serverName': serverName,
            'extensions': extensions,
            'cipher': cipher,
            'cert': cert,
            'startTime':StartTime
        })
    return result
def loadFromFiles():
    from datetime import timedelta, datetime
    import os
    # yesterday_d = (datetime.today() + timedelta(-1)).strftime("%Y-%m-%d")
    day = (datetime.today()).strftime("%Y-%m-%d")
    pre_h = (datetime.today() + timedelta(hours=-1)).strftime("%Y-%m-%d_%H")
    print(pre_h)
    fileList = []
    dnsList = []
    for root,sub,names in os.walk('/data_TH'):
        if day not in root:
            continue
        for name in names:
            if pre_h not in name:
                continue
            filename = os.path.join(root, name)
            if 'SSL' in root:
                fileList.append(filename)
            elif 'DNS' in root:                
                dnsList.append(filename)
    print(fileList[:10])
    print(dnsList[:10])
    pool = Pool(20)
    connects = pool.map(loadFromFile,fileList)
    pool.close()
    pool.join()
    result = []
    for dnsList in connects:
        result.extend(dnsList)
    df = pd.DataFrame(result)
    df.to_csv('/home/zouyuan/data/%s.csv'%pre_h,index=False)

if __name__=='__main__':
    loadFromFiles()

    # dates = [
    #     '0820','0821','0823','0824','0825','0827','0829'
    # ]
    #
    # for date in dates:
    #     tlsCollect('ssl_2018%s'%date)
    # csv2graph(dates)
    # graph2edgefile('data/ssl_graph.csv','data/edge_ssl.txt')
