import requests, re, json
res = requests.get(r'http://tnd-conm-app-1.burnsmcd.com:9000/cmapi/rest/v1/locationservice/locations',
                   params={'locationSystem.id': '12', 'locationLevel.id': '35'},
                   auth=('cmapi', 'cmapi'),
                   headers={'Range': 'items=1-1'})

ctLocs = re.sub(r'items 1-1/(\d+)', r'\1', res.headers['Content-Range'])

res = requests.get(r'http://tnd-conm-app-1.burnsmcd.com:9000/cmapi/rest/v1/locationservice/locations',
                   params={'locationSystem.id': '12', 'locationLevel.id': '35'},
                   auth=('cmapi', 'cmapi'),
                   headers={'Range': f'items=1-{ctLocs}'})

locs = json.loads(res.content)
paramString = ''

for i in locs:
    paramString += f'{i["fullName"]}%'

paramString = paramString[:-1]
print(paramString)