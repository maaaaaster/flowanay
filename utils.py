def readDataFromKeys(data,keys,default=None):
    temp = data.copy()
    for key in keys.split('.'):
        if key in temp:
            temp = temp[key]
        else:
            return default
    return temp

def addCountToMap(data,key,count=1):
    if key not in data:
        data[key] = 0
    data[key]+=count

def addSetToMap(data,key,val):
    if key not in data:
        data[key] = set()
    data[key].add(val)

def saveMap(mapData, outname):
    outf = open(outname, 'w+')
    outf.write('key, data\n')
    for key in mapData:
        ciphers = '\t'.join(list(mapData[key]))
        line = '%s, %s\n' % (key, ciphers)
        outf.write(line)

def saveCount(key2count, outname):
    outf = open(outname, 'w+')
    outf.write('key, count\n')
    for key in key2count:
        line = '%s, %d\n' % (key, key2count[key])
        outf.write(line)