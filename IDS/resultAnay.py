from utils import addCountToMap
inf = open('result.txt')
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
    if clientMap[ip] > 1:
        print(ip,clientMap[ip])

print(len(clientMap),len(serverMap))