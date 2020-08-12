#coding=utf-8
from pyquery import PyQuery as pq
import requests
import pymongo


client = pymongo.MongoClient('127.0.0.1')
mydb = client.testerhome
nodes = mydb.node


def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None



def parse_data(url):
    html = request(url)
    doc = pq(html)
    nodeitems = doc('div.node-list>div.node').items()
    item = {}
    for node in nodeitems:
        item['node'] = node('div.node>label.media-left').text()
        nodeChilds = node('div.node span.name>a').items()
        nodechild = []
        for nodecChild in nodeChilds:
            result = {}
            result['id'] = nodecChild.attr('data-id')
            result['title'] = nodecChild.text()
            nodechild.append(result)
        item['nodechild'] = nodechild
        yield item

def mongo(url):
    for item in parse_data(url):
        print(item)
        nodes.insert(item.copy())


url = 'https://testerhome.com/questions'
mongo(url)