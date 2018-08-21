import requests
import json
headers = {"Content-Type": "application/json","Accept":"application/json"}
jsonPayload = '{"TABLE": ["dns"], "OPRTYPE":"select","WHERE":{"query":{"match_all":{}}}}'
r = requests.post("http://202.112.51.162:8201/database",headers=headers,data=jsonPayload)
result = r.text
print(result)
