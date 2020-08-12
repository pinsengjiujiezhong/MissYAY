#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/5/2 21:01'

import pymongo,requests,re
from datetime import datetime
from elasticsearch import Elasticsearch

conn = pymongo.MongoClient('127.0.0.1')
mydb = conn.testhome


host = pymongo.MongoClient('140.143.15.155')
testerhome = host.testerhome
communityh = testerhome.community
# college = mydb.colleges
# cursor = college.find()
# for item in cursor:
#     print(item)
community = mydb.community
cursor = community.find({})
for item in cursor:
    del item['_id']
    communityh.insert(item)
# favs = mydb.favs
# follow = mydb.follow
# node = mydb.node
# user = mydb.user
# es = Elasticsearch(hosts="140.143.15.155", port=9200)
# mongoList = ['colleges', 'community', 'favs', 'follow', 'node', 'user']
# mongoList = ['favs', 'follow', 'node', 'user']
# for mongo in mongoList:
#     result = mydb[mongo]
#     cursor = result.find({})
#     esIndex = 'testerhome_' + mongo
#     print('esIndex: ', esIndex)
#     for item in cursor:
#         del item['_id']
#         res = es.index(index=esIndex, doc_type=mongo, body=item)
# es.indices.delete('testerhome_community')

