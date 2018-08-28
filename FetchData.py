import requests
import json
import copy
jsonPayload = \
    {
        "TABLE": [],
        "OPRTYPE": "select",
        "size": 1000,
        "WHERE": {
           "query": {

           }
        }
   }
def fetchWithPayload(payload):
    headers = {"Content-Type": "application/json", "Accept":"application/json"}
    r = requests.post("http://202.112.51.162:8201/database", headers=headers, data=payload)
    result = r.json()
    return result['hits']['hits']

def makePayload(day,table,match):
    data = copy.deepcopy(jsonPayload)
    data['TABLE'].append("{table}_{day}".format(day=day,table=table))
    data['WHERE']['query']['match'] = match
    result = json.dumps(data)
    return result

# fetchWithPayload(makePayload('20180825','http',match={"ConnectInfor.RecordTime": "2018-08-25 10:11:04"}))

