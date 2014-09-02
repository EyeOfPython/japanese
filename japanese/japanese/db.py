'''
Created on 02.09.2014

@author: ruckt
'''

import pymongo
import os
os.environ['http_proxy'] = '16.44.10.137:8080'
os.environ['https_proxy'] = '16.44.10.137:8080'

try:
    mongo_server = pymongo.MongoClient('localhost', 27017)
except:
    mongo_server = pymongo.MongoClient('ultimus.sytes.net', 27017)
    
japanese_db = mongo_server.kanjis
kanjis = japanese_db.kanjis