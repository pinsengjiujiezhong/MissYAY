#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/7/18 15:19'
import pymongo
import requests
import os

from elasticsearch import Elasticsearch

def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        fo = response.content
        return fo
    else:
        return None


def writer_img(url, path):
    fo = request(url)
    with open(path, 'wb') as f:
        f.write(fo)


client = pymongo.MongoClient('127.0.0.1')
mydb = client.testhome
college = mydb.college
colleges = mydb.colleges
items = college.find({})
# for item in items:
#     url = item['img_url']
#     path = 'E:\\Pycharm\\django\\testhome\\media' + item['img'].replace('/', '\\')
#     print(path)
#     dirs = path.rsplit('\\', 1)[0]
#     print(dirs)
#     if not os.path.exists(dirs):
#         os.makedirs(dirs)
#     writer_img(url, path)
# for item in items:
#     item['title'] = item['title'].strip()
#     userList = []
#     for user in item['users']:
#         user['role'] = user['role'].strip()
#         userList.append(user)
#     item['users'] = userList
#     colleges.insert(item)
es = Elasticsearch(hosts="127.0.0.1", port=9200)
# es.indices.delete('testerhome_college')
cursor = colleges.find({})
# for item in cursor:
#     del item['_id']
#     res = es.index(index="testerhome_college", doc_type="college", body=item)

