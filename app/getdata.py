import requests
import json
import datetime 
from flask import flash
import os, re


badList = [
    u'Pagina_principale',
    u'Speciale:Ricerca',
    u'Speciale:CercaCollegamenti',
    u'Main_Page',
    u'Special:Search',
    u'Portada',
    u'Especial:Buscar',
    u'Hauptseite',
    u'Spezial:Suche',
    u'Wikip\xe9dia:Accueil_principal',
    u'Fran\xe7ois_Fillon'
]


def getViews(query):
    try:
        data = []
        for q in query['query']:

            languages = ('en', 'English'), ('it', 'Italian'), ('nl','Nederlands'), ('sv','Swedish'),('ceb','Cebuano'),('de','German'),('fr', 'French'),('ru', 'Russian'),('es','Spanish')
            
            for lang in languages:
                
                base = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' + lang[0] + '.wikipedia/all-access/all-agents'

                url = "/".join([base, q, 'daily', query['start']+'00', query['end']+'00'])

                response = requests.get(url)
                if response.json().has_key('items'):
                    stats = response.json()['items']
                    for s in stats:
                        if s.has_key('views'):
                            s[q.replace('(', '').replace(')', '').replace("'", '_').replace(" ", '_')+'_views'] = s['views']

                    data += stats

        return data, response.content

    except(KeyError):
        print "No data"
        return None, response.content



def saveJson(data, filename="data"):
 with open(filename+'.json', 'wb') as f:
    f.write(json.dumps(data))


def getTrends(day=datetime.date.today()-datetime.timedelta(days=1), lang='en'):
    
    try:
        data = []
        url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/'+str(lang)+'.wikipedia/all-access/'+str(day.year)+'/'+str(day.month)+'/'+str(day.day)
        print url
        response = requests.get(url)
        if response.json().has_key('items'):
            stats = response.json()['items']
            for s in stats[0]['articles']:
                s['project'] = stats[0]['project']
            data += stats[0]['articles']
        else:
            day=datetime.date.today()-datetime.timedelta(days=2)
            url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/'+str(lang)+'.wikipedia/all-access/'+str(day.year)+'/'+str(day.month)+'/'+str(day.day)
            response = requests.get(url)
            if response.json().has_key('items'):
                stats = response.json()['items']
                for s in stats[0]['articles']:
                    s['project'] = stats[0]['project']
                data += stats[0]['articles']


        for b in badList:
            for d in data:
                if b in d.values(): data.remove(d)

        return data, day, response.content

    except(KeyError):
        print "No data"
        return None, day ,response.content


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



