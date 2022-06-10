import requests, re, json
res = requests.get(r'<redacted>',
                   params={'locationSystem.id': '12', 'locationLevel.id': '35'},
                   auth=('cmapi', '<redacted>'),
                   headers={'Range': 'items=1-1'})

ctLocs = re.sub(r'items 1-1/(\d+)', r'\1', res.headers['Content-Range'])

res = requests.get(r'<redacted>',
                   params={'locationSystem.id': '12', 'locationLevel.id': '35'},
                   auth=('cmapi', '<redacted>'),
                   headers={'Range': f'items=1-{ctLocs}'})

locs = json.loads(res.content)
paramString = ''

for i in locs:
    paramString += f'{i["fullName"]}%'

paramString = paramString[:-1]
print(paramString)
