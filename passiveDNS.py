from ELModel import loadData
from utils import readDataFromKeys


def ip2domain(tablename,key):
    result = []
    detail = {
        "query": {
            "match": {
                "DNS.Answers.Value": key
                # "DNS.Queries.Name":key
            }
        }
    }
    sources = ["DNS.Queries.Name",'PacketInfor.TimeStamp']
    dataGen = loadData(table=tablename, detail=detail,sources=sources)
    for dataList in dataGen:
        for data in dataList:
            data = data['_source']
            domain = readDataFromKeys(data,"DNS.Queries")[0]['Name']
            timeStmp = readDataFromKeys(data,"PacketInfor.TimeStamp")
            print(domain,timeStmp)
            result.append({
                'domain':domain,
                'timeStmp':timeStmp
            })
    return result


if __name__== '__main__':
    ip = '169.229.150.100'
    # domain = 'rsfglh.com'
    ip2domain('dns_20180824', ip)
