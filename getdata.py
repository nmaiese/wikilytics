import requests
import json
from datetime import datetime

viewsUrl = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents'

def getViews(base, query):
    data = []
    for q in query['query']:
        url = "/".join([base, q, 'daily', query['start']+'00', query['end']+'00'])
        response = requests.get(url)
        try:
            stats = response.json()['items']
            results = []
            for s in stats:
                data.append({'name': q,
                         'day': '/'.join([s['timestamp'][-4:-2], s['timestamp'][5:7], s['timestamp'][:4]]),
                         'views': s['views'] })
            data += results
        except(KeyError):
            print "No data"
    return data

def saveJson(data, filename):
 with open('output/'+filename+'.json', 'wb') as f:
    f.write(json.dumps(data))



q = {'query':['Donald_Trump', 'Hillary_Clinton'],
     'start':'20150101',
     'end':'20161110'}


data = getViews(viewsUrl, q)

if data:
    saveJson(data, "-".join(q['query']))


