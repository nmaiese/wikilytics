import requests
import json
from datetime import datetime


def getViews(base, query):
    try:
        data = []
        for q in query['query']:
            url = "/".join([base, q, 'daily', query['start']+'00', query['end']+'00'])
            response = requests.get(url)
            stats = response.json()['items']
            results = []
            for s in stats:
                data.append({'name': q,
                             'day': s['timestamp'][:-2],
                             'views': s['views'] })
                data += results


        return stats

    except(KeyError):
        print "No data"



def saveJson(data, filename="data"):
 with open(filename+'.json', 'wb') as f:
    f.write(json.dumps(data))




def launchQuery(query, start, end):

    # start = "20161101"
    # end = "20161114"
    # query = 'Donald Trump'

    viewsUrl = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents'
    q = {'query': [query],
         'start': str(start),
         'end': (end)}

    data = getViews(viewsUrl, q)
    return data
#data = getViews(viewsUrl, q)

#if data:
#    saveJson(data, "-".join(q['query']))


