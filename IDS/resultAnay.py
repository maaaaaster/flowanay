from utils import addCountToMap
inf = open('result3.txt')
clientMap = {}
serverMap = {}
for line in inf.readlines():
    vals = line.split(' ')
    key = vals[0]
    value = vals[-1].strip()
    if key == 'clientIP':
        addCountToMap(clientMap,value)
    if key == 'serverIP':
        addCountToMap(serverMap,value)
for ip in clientMap:
    if not ip.startswith('10.') and not ip.startswith('162.105.') and not ip.startswith('222.29'):
        print(ip,clientMap[ip])

print(len(clientMap),len(serverMap))