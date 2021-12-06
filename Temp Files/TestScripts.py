import json
from urllib.request import urlopen
url = 'https://psapi.nrk.no/tv/catalog/programs/FØST70001093'

data = urlopen(url).parse.read()

json = json.loads(data)

print(json)