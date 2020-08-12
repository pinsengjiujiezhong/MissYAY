#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/5/2 21:01'

import pymongo,requests,re
from datetime import datetime
from elasticsearch import Elasticsearch

conn = pymongo.MongoClient('127.0.0.1')
mydb = conn.testhome
community = mydb.community
communitys = mydb.communitys
user = mydb.user
users = mydb.users
college = mydb.college
follow = mydb.follow
node = mydb.node

cursor = communitys.find()
print(cursor.count())
# for item in cursor:
    # item['content'] = item['content'].replace('<img src="/images', '<img src="/media/images')
    # del item['_id']
    # communitys.insert(item)
es = Elasticsearch(hosts="127.0.0.1", port=9200)
i = 1
for item in cursor:
    print(i)
    i += 1
    del item['_id']
    res = es.index(index="testerhome_community", doc_type="community", body=item)
# res = es.indices.delete('testerhome_community')