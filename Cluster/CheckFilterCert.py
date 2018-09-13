import json
import pandas as pd

from TrainData import filterCertList

RealAttackFile = '/home/OpenCode/FlowAnay/Cluster/data/ActualBlack.csv'



def loadRealAttack():
    result = set()
    for line in open('ActualBlack.txt'):
        hashCert = line.strip()
        result.add(hashCert)
    return result

# certSet = json.load(open(filterCertList))
# certSet = loadRealAttack()
# df = pd.read_csv('/home/OpenCode/FlowAnay/Cluster/data/white_graph.csv')
# t = df[df['cert'].map(lambda x:x in certSet)]
# t.to_csv(RealAttackFile,index=False)
