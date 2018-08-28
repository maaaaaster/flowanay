import requests
import json
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
    print(r.text)
    result = r.json()
    return result['hits']['hits']

def makePayload(day,table,match):
    data = jsonPayload.copy()
    data['TABLE'].append("{table}_{day}".format(day=day,table=table))
    data['WHERE']['query']['match'] = match
    result = json.dumps(data)
    print(result)
    return result

fetchWithPayload(makePayload('20180825','http',match={"ConnectInfor.RecordTime": "2018-08-25 10:11:04"}))

