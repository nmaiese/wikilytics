import requests
import json
from datetime import datetime
from flask import flash

def getViews(query):
    try:
        data = []
        for q in query['query']:

            languages = ('en', 'English'), ('it', 'Italian'), ('de', 'Deutsch'), ('nl','Nederlands'), ('sv','Swedish'),('ceb','Cebuano'),('de','German'),('fr', 'French'),('ru', 'Russian'),('es','Spanish')
            
            for lang in languages:
                
                base = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' + lang[0] + '.wikipedia/all-access/all-agents'

                url = "/".join([base, q, 'daily', query['start']+'00', query['end']+'00'])

                response = requests.get(url)
                if response.json().has_key('items'):
                    stats = response.json()['items']
                    data += stats

        return data, response.content

    except(KeyError):
        print "No data"
        return None, response.content



def saveJson(data, filename="data"):
 with open(filename+'.json', 'wb') as f:
    f.write(json.dumps(data))




def launchQuery(query, start, end):

    # start = "20161101"
    # end = "20161114"
    # query = 'Donald Trump'

    query = query.split(",")

    for i in range(0, len(query)): 
        if query[i][0] == ' ':
            query[i] = query[i][1:]        
        if query[i][-1] == ' ':
            query[i] = query[i][:-1]

    q = {'query': query,
         'start': str(start),
         'end': (end)}

    data, errors = getViews(q)
    return data, errors
#data = getViews(viewsUrl, q)

#if data:
#    saveJson(data, "-".join(q['query']))


