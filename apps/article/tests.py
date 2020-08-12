#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/5/2 21:01'

import pymongo,requests,re
from datetime import datetime
from elasticsearch import Elasticsearch

conn = pymongo.MongoClient('127.0.0.1')
mydb = conn.testerhome
# college = mydb.colleges
# cursor = college.find()
# for item in cursor:
#     print(item)
# community = mydb.community
# favs = mydb.favs
# follow = mydb.follow
# node = mydb.node
# user = mydb.user
es = Elasticsearch(hosts="140.143.15.155", port=9200)
mongoList = ['favs', 'follow', 'user']
mongoList = ['user']
for mongo in mongoList:
    result = mydb[mongo]
    cursor = result.find({})
    esIndex = 'testerhome_' + mongo
    print('esIndex: ', esIndex)
    for item in cursor:
        del item['_id']
        res = es.index(index=esIndex, doc_type=mongo, body=item)
# es.indices.delete('testerhome_user')

