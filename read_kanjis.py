'''
Created on 02.09.2014

@author: ruckt
'''

import requests
from htmldom import htmldom
import sys
from urllib import parse
import re
import pymongo

reg = re.compile( '''<strong>
        (\d*)
    <\/strong>
    of 2500 most used kanji in newspapers''' )

def read_kanji(kanji,  reg=reg):
    r = requests.get('http://jisho.org/kanji/details/%s' % parse.quote(kanji, '/', 'utf-8'))
    
    dom = htmldom.HtmlDom().createDom(r.text)
    
    d = {'kun':[], 'on':[], 'names':[], 'meanings':None, 'freq': 0, 'kanji':kanji}
    key = None
    for line in dom.find('.japanese_readings').text().split('\n'):
        newkey = next( (k for k in d if k in line), None )
        line = line.strip()
        if not newkey:
            if line:
                d[key] += [ e for e in line.split('&#12289; ') if e ]
        else:
            key = newkey
    
    d['meanings'] = [ e.strip()[:-1] for e in dom.find('.english_meanings h2 + p').text().split('\n') if e ]
    m = reg.search(dom.find('.specs').html())
    d['freq'] = int(0 if not m else m.group(1))
    return d
    
mongo_server = pymongo.MongoClient('ultimus.sytes.net', 27017)
n = 1
for k in mongo_server.kanjis.kanjis.find({'freq': {'$gt':0}}, sort=[('freq',1)]):
    if k['freq'] != n:
        break
    n += 1
    print(k)
    
if __name__ == '__main__1':
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
    
    kanjis = open('kanjidict.csv', encoding='utf-8')
    
    try:
        mongo_server = pymongo.MongoClient('localhost', 27017)
    except:
        mongo_server = pymongo.MongoClient('ultimus.sytes.net', 27017)
    db = mongo_server.kanjis
    db_kanjis = db.kanjis
    for l in kanjis:
        kanji = l[0]
        kanji_info = read_kanji(kanji)
        db_kanjis.remove({'kanji': kanji})
        s = db_kanjis.save(kanji_info)
        print('saved', s, 'with', kanji_info)
    
    for k in db_kanjis.find():
        print(k)