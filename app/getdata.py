import requests
import json
import datetime
from flask import flash
import os, re
from bs4 import BeautifulSoup
import urllib

badList = [
    u'Pagina_principale',
    u'Speciale:Ricerca',
    u'Speciale:CercaCollegamenti',
    u'Speciale:Entra',
    u'Speciale:Libro',
    u'Speciale:CreaUtenza',
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
            for lang in query['langs']:

                base = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' + lang + '.wikipedia/all-access/all-agents'

                url = "/".join([base, q, 'daily', query['start']+'00', query['end']+'00'])

                response = requests.get(url)
                if response.json().has_key('items'):
                    stats = response.json()['items']
                    for s in stats:
                        if s.has_key('views'):
                            replace = ''.join(e for e in s['article'] if e.isalnum())
                            s[replace + 'views'] = s['views']
                    data += stats

        if data == []: data = None

        return data, response.content

    except(KeyError):
        print "No data"
        return None, response.content


def getTrends(day=datetime.date.today()-datetime.timedelta(days=1), langs=['en']):

    try:
        data = []

        for lang in langs:
            url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/'+str(lang)+'.wikipedia/all-access/'+str('%02d' % day.year)+'/'+str('%02d' % day.month)+'/'+str('%02d' % day.day)
            response = requests.get(url)
            if response.json().has_key('items'):
                stats = response.json()['items']
                for s in stats[0]['articles']:
                    s['project'] = stats[0]['project']
                data += stats[0]['articles']
            else:
                day=datetime.date.today()-datetime.timedelta(days=2)
                url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/'+str(lang)+'.wikipedia/all-access/'+str('%02d' % day.year)+'/'+str('%02d' % day.month)+'/'+str('%02d' % day.day)
                response = requests.get(url)
                if response.json().has_key('items'):
                    stats = response.json()['items']
                    for s in stats[0]['articles']:
                        s['project'] = stats[0]['project']
                    data += stats[0]['articles']


            for b in badList:
                for d in data:
                    if b in d.values(): data.remove(d)
                    d['lang'] = lang

        return data, day, response.content

    except(KeyError):
        print "No data"
        return None, day ,response.content



def launchQuery(query, start, end, langs):

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
         'end': str(end),
         'langs': langs
         }

    data, errors = getViews(q)
    return data, errors




def acquireTrends(langs=['en']):
    trends, day, errors = getTrends(langs=langs)
    query_list = ''
    query_title = ''
    timestamp = str('%02d' % day.year) + str('%02d' % day.month) + str('%02d' % day.day) + '00'
    toappend = []

    i = 0

    for d in trends:

        query_list += ((d['article'])+',')
        query_title += ((d['article'])+' - ')
        article = ''.join(e for e in d['article'] if e.isalnum())

        toappend += [{u'access': u'all-access', u'views': d['views'], u'timestamp': timestamp, u'agent': u'all-agents', u'project': d['lang']+'.wikipedia', article+'views': d['views'], u'granularity': u'daily', u'article': d['article']}]

        i += 1
        if i > 4: break

    query_list = query_list[:-1]
    query_title = query_title[:-2]
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=7)

    startDate = str('%02d' % start.year)+str('%02d' % start.month)+str('%02d' % start.day)
    endDate =  str('%02d' % end.year)+str('%02d' % end.month)+str('%02d' % end.day)

    data, errors = launchQuery(query_list, startDate, endDate, langs)
    if not data:
        flash("No data, retry")
        flash(errors)
    data += toappend
    return data, query_list, query_title


def enrichArticles(articles, lang):
    object_articles = []
    for article in articles:
        url = 'https://'+lang+'.wikipedia.org/wiki/'+article;
        content = urllib.urlopen(url).read()
        page = BeautifulSoup(content, "html.parser")
        title = page.find('h1', id="firstHeading").text
        description = page.find('div', id="bodyContent").find('p').text
        image = page.find('div', id="bodyContent").find('img')['src']
        object_articles.append({'title':title, 'url':url, 'image':image, 'description':description})
    return object_articles
