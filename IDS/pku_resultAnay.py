def addCountToMap(data,key,count=1):
    if key not in data:
        data[key] = 0
    data[key]+=count

inf = open('result.txt')
clientMap = {}
serverMap = {}

def inPku(ip):
    if ip.startswith('162.105') or ip.startswith('222.29') or ip.startswith('10.'):
        return True
    return False

for line in inf.readlines():
    vals = line.split(' ')
    key = vals[0]
    value = vals[-1].strip()
    if key == 'clientIP':
        addCountToMap(clientMap,value)
    if key == 'serverIP':
        addCountToMap(serverMap,value)
outf = open('toCheck.txt','w+')
for ip in clientMap:
    if not inPku(ip):
        print(ip,clientMap[ip])
        outf.write(ip+'\n')

print(len(clientMap),len(serverMap))