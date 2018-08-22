def readDataFromKeys(data,keys,default=None):
    temp = data.copy()
    for key in keys.split('.'):
        if key in temp:
            temp = temp[key]
        else:
            return default
    return temp

def addCountToMap(data,key):
    if key not in data:
        data[key] = 0
    data[key]+=1

def addSetToMap(data,key,val):
    if key not in data:
        data[key] = set()
    data[key].add(val)