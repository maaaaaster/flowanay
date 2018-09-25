inf = '/home/OpenCode/FlowAnay/ThreatInfo/query.ip.result'

blackMap = [0]*3

for line in open(inf).readlines():
    vals = line.strip().split('[')
    data = eval('['+vals[1])
    blackCnt = 0
    for key in data:
        if key.endswith('Y'):
            blackCnt+=1
    print(line.strip())
    # if blackCnt ==0 :
    #     print(vals[0])
    blackMap[blackCnt]+=1
print(blackMap)

