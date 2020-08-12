#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/7/19 15:39'
from pyquery import PyQuery as pq
import requests
import pymongo

client = pymongo.MongoClient('127.0.0.1')
mydb = client.testhome
node_mongo = mydb.node


def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_node(url):
    html = request(url)
    doc = pq(html)
    items = doc('.node-list .node').items()
    for item in items:
        node = {}
        node['title'] = item('.media-left').text()
        node['childnode'] = []
        childnodes = item('.nodes>span.name>a').items()
        for childnode in childnodes:
            child = {}
            child['id'] = childnode('a').attr('data-id')
            child['title'] = childnode('a').attr('title')
            node['childnode'].append(child)
        node_mongo.insert(node)

url = 'https://testerhome.com/bugs'
parse_node(url)



