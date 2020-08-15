from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
import json,re
import time
from elasticsearch import Elasticsearch
from django.shortcuts import render, HttpResponse
import pymongo
es = Elasticsearch([{'host': '140.143.15.155', 'port': 9200}])
client = pymongo.MongoClient('127.0.0.1')
mydb = client.testerhomes
sites = mydb.sites

# index页面
class Index(View):
    def get(self, request):
        page = request.GET.get('page', '')
        keyword = request.GET.get('keyword', '')
        if not page:
            page = 1
        else:
            page = int(page)
        new_body = {"query": {"match_all": {}}, 'from': 0, 'size': 6, 'sort': {"release_time": {"order": "desc"}}}
        new_items = es.search(index='testerhome_community', doc_type='community', body=new_body)
        new_result = [{
            'title': item['_source']['title'],
            'portrait': item['_source']['portrait'],
            'uname': item['_source']['username'],
            'uid': item['_source']['uid'],
            'id': item['_source']['id'],
            'teamname': item['_source']['teamname'],
            'teamuid': item['_source']['teamuid'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'comments': item['_source']['comments'],
            'release_time': item['_source']['release_time'],
            'recovery_time': item['_source']['recovery_time'],
        } for item in new_items['hits']['hits']]
        awesome_body = {"query": {"match": {'awesome': True}}, 'from': 0, 'size': 20, 'sort': {"release_time": {"order": "desc"}}}
        awesome_items = es.search(index='testerhome_community', doc_type='community', body=awesome_body)
        awesome_result = [{
            'title': item['_source']['title'],
            'portrait': item['_source']['portrait'],
            'uname': item['_source']['username'],
            'uid': item['_source']['uid'],
            'id': item['_source']['id'],
            'teamname': item['_source']['teamname'],
            'teamuid': item['_source']['teamuid'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'release_time': item['_source']['release_time'],
            'recovery_time': item['_source']['recovery_time'],
        } for item in awesome_items['hits']['hits']]
        stick_body = {"query": {"terms": {'id': ['24702', '24159', '24221']}}, 'from': 0, 'size': 4, 'sort': {"release_time": {"order": "desc"}}}
        stick_items = es.search(index='testerhome_community', doc_type='community', body=stick_body)
        stick_result = [{
            'title': item['_source']['title'],
            'portrait': item['_source']['portrait'],
            'uname': item['_source']['username'],
            'uid': item['_source']['uid'],
            'id': item['_source']['id'],
            'teamname': item['_source']['teamname'],
            'teamuid': item['_source']['teamuid'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'release_time': item['_source']['release_time'],
            'recovery_time': item['_source']['recovery_time'],
        } for item in stick_items['hits']['hits']]
        new_user_body = {"query": {"match_all": {}}, 'from': 0, 'size': 10, 'sort': {"date": {"order": "desc"}}}
        new_user_items = es.search(index='testerhome_user', doc_type='user', body=new_user_body)
        new_user_result = [{
            'uid': item['_source']['uid'],
            'uname': item['_source']['uname'],
            'img': item['_source']['img'],
        } for item in new_user_items['hits']['hits']]
        nodechiled_items = es.search(index='testerhome_node', doc_type='node', body={
            "query": {
                "match_all": {}
            },
            "size": 100,
        })
        nodechilds = [{
            'title': item['_source']['node'],
            'nodechild': item['_source']['nodechild']
        } for item in nodechiled_items['hits']['hits']]
        hot_nodes = []
        for nodechild in nodechilds:
            for node in nodechild['nodechild']:
                hot_nodes.append(node)
        hot_nodes = hot_nodes[:30]
        current_time = int(time.time())
        hot_communtiy_body = {"query": {"range": {'recovery_time': {'gte': current_time - 2592000, 'lte': current_time}}}, 'from': 0, 'size': 10}
        hot_communtiy_items = es.search(index='testerhome_community', doc_type='community', body=hot_communtiy_body)
        hot_communtiy_result = [{
            'title': item['_source']['title'],
            'id': item['_source']['id'],
            'index': hot_communtiy_items['hits']['hits'].index(item) + 1,
        } for item in hot_communtiy_items['hits']['hits']]
        new_bugs_body = {"query": {"match": {'flag': 'Bug 曝光台'}}, 'from': 0, 'size': 5, 'sort': {"release_time": {"order": "desc"}}}
        new_bugs_items = es.search(index='testerhome_community', doc_type='community', body=new_bugs_body)
        new_bugs_result = [{
            'title': item['_source']['title'],
            'id': item['_source']['id'],
            'index': new_bugs_items['hits']['hits'].index(item) + 1,
        } for item in new_bugs_items['hits']['hits']]
        new_result = [new_result[0:3], new_result[3:6]]
        stick_result = [stick_result[0:2], stick_result[2:len(stick_result)+1]]
        awesome_result = [awesome_result[0:10], awesome_result[10:20]]
        return render(request, 'index.html', {'new_results': new_result, 'awesome_results': awesome_result, 'stick_results': stick_result, 'hot_nodes': hot_nodes, 'new_bugs_results': new_bugs_result, 'hot_communtiy_results': hot_communtiy_result, 'new_user_results': new_user_result})


class Search(View):
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "match": {
                    "title": keyword
                }
            },
            "from": 0,
            "size": 10,
        })
        result = [{
            'title': item['_source']['title'],
            'url': '/community/' + item['_source']['id'],
        } for item in items['hits']['hits']]
        result = json.dumps(result)
        return HttpResponse(result)

    def post(self, request):
        pass


# 搜索框搜索数据
class GetArticle(View):
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        curr_page = request.GET.get('page', '')
        if not curr_page:
            curr_page = 1
        else:
            curr_page = int(curr_page)
        items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"title": keyword}},
                        {"match": {"content": keyword}}
                    ],
                    "tie_breaker": 0.3
                }
            },
            'size': 25,
            'from': 0
        })
        searchitems = [{
            'title': item['_source']['title'],
            'id': item['_source']['id'],
            'content': item['_source']['content'],
            'date': get_curr_time(item['_source']['release_time']),
            'url': 'http://127.0.0.1:8000/community/' + item['_source']['id'],
        } for item in items['hits']['hits']]
        searchs = []
        for search in searchitems:
            index = search['content'].lower().find(keyword.lower())
            if index-100 < 0:
                start = 0
            else:
                start = index - 100
            if index+100 > len(search['content']):
                end = len(search['content'])
            else:
                end = index + 100
            content = re.sub('<.+?>', '', search['content'])
            content = content[start: end]
            keywords = re.findall(keyword, content, flags=re.IGNORECASE)
            for keyword in keywords:
                content = content.replace(keyword, '<em>' + keyword + '</em>')
            search['content'] = content
            searchs.append(search)
        total = items['hits']['total']
        page_num = total // 25 + 2
        if page_num < 11:
            pageList = range(1, page_num)
        else:
            pageList = range(1, page_num)
            if curr_page < 5:
                pageList = range(1, page_num)[:10]
            elif curr_page > page_num - 5:
                pageList = range(1, page_num)[page_num - 11:]
            else:
                pageList = range(1, page_num)[curr_page - 5: curr_page + 5]
        return render(request, 'searchPage.html', {'searchs': searchs, 'keyword': keyword, 'total': total, 'pageList': pageList, 'curr_page': curr_page, 'page_num': page_num})

    def post(self, request):
        pass

# 文章详情页面
class GetCommunity(View):
    def get(self, request, Cid):
        items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "term": {
                    "id": str(Cid)
                }
            }
        })
        items['hits']['hits'][0]['_source']['content'] = items['hits']['hits'][0]['_source']['content'].replace('\n', '')
        community = items['hits']['hits'][0]['_source']
        i = 0
        for comment in community['comments']:
            if 'date' in comment.keys():
                comment['date'] = get_curr_time(comment['date'])
                if not comment['date']:
                    comment['date'] = comment['release_time']
            i += 1
        community['release_time'] = get_curr_time(community['release_time'])
        if 'recovery_time' in community.keys() and community['recovery_time']:
            community['recovery_time'] = get_curr_time(community['recovery_time'])
        uid = community['uid']
        college_body = {"query": {"bool": {"must": [{"term": {"users.uid.keyword": uid}}]}}, "from": 0, "size": 100}
        college_items = es.search(index='testerhome_college', doc_type='college', body=college_body)
        college_result = [{
            'img': item['_source']['img'],
            'id': item['_source']['id'],
            'title': item['_source']['title'],
        } for item in college_items['hits']['hits']]
        uid = community['uid']
        user_body = {"query": {"match": {"uid": uid}}}
        user_items = es.search(index='testerhome_user', doc_type='user', body=user_body)
        user_result = user_items['hits']['hits'][0]['_source']
        print('community: ', community)
        for comment in community['comments']:
            if 'reply_id' in comment.keys():
                print(comment['reply_id'])
        return render(request, 'community.html', {'community': community, 'college_items': college_result, 'user': user_result})

    def post(self, request):
        pass


def get_curr_time(date):
    if not date:
        return None
    curr_time = int(time.time()) - int(date)
    curr_time = int(curr_time)
    if int(date) < 1577808000:
        reply_time = time.strftime('%Y-%m-%d', time.localtime(date))
        curr_reply = list(reply_time)
        curr_reply.insert(4, '年')
        curr_reply.insert(8, '月')
        curr_reply.insert(12, '日')
        reply_time = ''.join(curr_reply).replace('-', '')
        return reply_time
    if curr_time < 3600:
        reply_time = str(curr_time // 60) + '分钟前'
    elif curr_time < 90000:
        reply_time = str(curr_time // 3600) + '小时前'
    elif curr_time < 2700000:
        reply_time = str(curr_time // 90000) + '天前'
    elif curr_time < 32400000:
        reply_time = str(curr_time // 2700000) + '月前'
    else:
        reply_time = time.strftime('%Y-%M-%D %H:%M:%S', time.localtime(date))
    return reply_time

def getUserAulf(Uid):
    user_items = es.search(index='testerhome_user', doc_type='user', body={
        "query": {
            "match": {
                "uid": Uid
            }
        }
    })
    user_result = user_items['hits']['hits'][0]['_source']
    college_body = {"query": {"bool": {"must": [{"term": {"users.uid.keyword": Uid}}]}}, "from": 0, "size": 100}
    college_items = es.search(index='testerhome_college', doc_type='college', body=college_body)
    college_result = [{
        'img': item['_source']['img'],
        'id': item['_source']['id'],
        'title': item['_source']['title'],
    } for item in college_items['hits']['hits']]
    return user_result, college_result


# 用户详情页面
class getUser(View):
    def get(self, request, Uid):
        user_result, college_result = getUserAulf(Uid)
        hot_topics = user_result['hot_topics']
        recent_posts = user_result['recently']
        topics_items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "terms": {
                    "id": hot_topics
                }
            }
        })
        hots_topics_community = [{
            'flag': hots_topic['_source']['flag'],
            'title': hots_topic['_source']['title'],
            'zan': hots_topic['_source']['zan'],
            'id': hots_topic['_source']['id'],
            'number': len(hots_topic['_source']['comments'])
        } for hots_topic in topics_items['hits']['hits']]
        posts_items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "terms": {
                    "id": recent_posts
                }
            }
        })
        topics_items_community = []
        for hots_topic in posts_items['hits']['hits']:
            item = {}
            item['title'] = hots_topic['_source']['title']
            item['id'] = hots_topic['_source']['id']
            last_comment = {}
            for comment in hots_topic['_source']['comments']:
                if 'uid' in comment.keys():
                    if comment['uid'] == Uid:
                        last_comment = comment
            if not last_comment:
                continue
            item['date'] = get_curr_time(last_comment['date'])
            item['content'] = last_comment['content']
            topics_items_community.append(item)
        return render(request, 'userinfo.html', {'type': 'user', 'user': user_result, 'colleges': college_result, 'hots_topics': hots_topics_community, 'recent_posts': topics_items_community})

    def post(self, request):
        pass



class GetTopics(View):
    def get(self, request, Uid):
        user_result, college_result = getUserAulf(Uid)
        page = request.GET.get('page', '')
        if not page:
            page = 1
        else:
            page = int(page)
        community_items = es.search(index='testerhome_community', doc_type='community', body={
            'query': {
                'match': {
                    'uid': Uid
                }
            },
            'from': (page-1)*20,
            'size': 20,
        })
        total = community_items['hits']['total']
        communitys = [{
            'flag': community['_source']['flag'],
            'title': community['_source']['title'],
            'date': get_curr_time(community['_source']['release_time']),
            'zan': community['_source']['zan'],
            'id': community['_source']['id'],
            'comments': community['_source']['comments'],
        } for community in community_items['hits']['hits']]
        if total % 20:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        if total_page > 500:
            total_page = 500
        page_list = []
        if total_page <= 10:
            page_list = range(1, total_page + 1)
        elif page < 5:
            page_list = range(1,  11)
        elif total_page - page < 5:
            page_list = range(total_page-10, total_page+1)
        else:
            page_list = range(page-4, page+6)
        return render(request, 'usertopics.html', {'type': 'topics', 'user': user_result, 'colleges': college_result, 'communitys': communitys, 'total': total, 'curr_page': page, 'page_list': page_list, 'total_page': total_page, 'up_page': page-1, 'next_page': page+1})

    def post(self, request):
        pass


class GetCollege(View):
    def get(self, request):
        college_items = es.search(index='testerhome_college', doc_type='college', body={
            "query": {
                "match_all": {}
            },
            'size': 1000,
        })
        result = [
            {
                'img': item['_source']['img'],
                'location': item['_source']['location'],
                'title': item['_source']['title'],
                'id': item['_source']['id'],
                'users': item['_source']['users'],
            } for item in college_items['hits']['hits']
        ]
        return render(request, 'college.html', {'colleges': result, 'total': college_items['hits']['total']})

    def post(self, request):
        pass


class GetCollegeDetail(View):
    def get(self, request, Uid):
        user_items = es.search(index='testerhome_college', doc_type='college', body={
            "query": {
                "match": {
                    "id": Uid
                }
            }
        })
        college = user_items['hits']['hits'][0]['_source']
        usersList = []
        for user in college['users']:
            user['img'] = user['img'].replace('/image', '/images')
            usersList.append(user)
        college['users'] = usersList
        teamname = college['title']
        page = request.GET.get('page', '')
        if not page:
            page = 1
        else:
            page = int(page)
        items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "match": {
                    "teamname": teamname
                }
            },
            "from": (page - 1) * 20,
            "size": 20,
        })
        total = items['hits']['total']
        communitys = [{
            'title': item['_source']['title'],
            'portrait': item['_source']['portrait'],
            'username': item['_source']['username'],
            'uid': item['_source']['uid'],
            'id': item['_source']['id'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'release_time': get_curr_time(item['_source']['release_time']),
            'recovery_time': get_curr_time(item['_source']['recovery_time']),
            'comments': item['_source']['comments']
        } for item in items['hits']['hits']]
        if total % 20:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        if total_page > 500:
            total_page = 500
        page_list = []
        if total_page <= 10:
            page_list = range(1, total_page + 1)
        elif page < 5:
            page_list = range(1,  11)
        elif total_page - page < 5:
            page_list = range(total_page-10, total_page+1)
        else:
            page_list = range(page-4, page+6)
        return render(request, 'college_detail.html', {'college': college, 'communitys': communitys, 'curr_page': page, 'page_list': page_list, 'total_page': total_page, 'up_page': page-1, 'next_page': page+1})

    def post(self, request, Uid):
        pass


class GetCollegeUser(View):
    def get(self, request, Uid):
        user_items = es.search(index='testerhome_college', doc_type='college', body={
            "query": {
                "match": {
                    "id": Uid
                }
            }
        })
        college = user_items['hits']['hits'][0]['_source']
        usersList = []
        for user in college['users']:
            user['img'] = user['img'].replace('/image', '/images')
            usersList.append(user)
        college['users'] = usersList
        return render(request, 'college_user.html', {'college': college})

    def post(self, request, Uid):
        pass


class GetQuestions(View):
    def get(self, request):
        return render(request, 'questions.html')

    def post(self, request):
        pass


class GetNode(View):
    def get(self, request, Nid):
        nodechiled_items = es.search(index='testerhome_node', doc_type='node', body={
            "query": {
                "match_all": {}
            },
            "size": 100,
        })
        nodechild = [{
            'title': item['_source']['node'],
            'nodechild': item['_source']['nodechild']
        } for item in nodechiled_items['hits']['hits']]
        page = request.GET.get('page', '')
        sort = request.GET.get('sort', '')
        if not page:
            page = 1
        else:
            page = int(page)
        if Nid == 'bugs':
            keyword = 'Bug 曝光台'
        elif Nid == 'questions':
            keyword = '问答'
        elif Nid == 'applications':
            keyword = '招聘'
        else:
            for node in nodechild:
                for childnode in node['nodechild']:
                    if childnode['id'] == Nid:
                        keyword = childnode['title']
                        body = {"query": {"match": {'query': keyword}}}
                        break
        if Nid == 'topics':
            keyword = '社区'
            body = {"query": {"match_all": {}}}
        else:
            body = {"query": {"match": {'flag': keyword}}}
        if sort == 'awesome':
            body['query'] = {"bool": {"must": [{"match": {"flag": keyword}}, {"match": {"awesome": True}}]}}
        elif sort == 'noreply':
            body['query'] = {"bool": {"must_not": {'exists': {'field': 'comments'}}}}
        elif sort == 'release':
            body['sort'] = [{"release_time": {"order": "desc"}}]
        elif sort == 'recovery':
            body['sort'] = [{"comments.date": {"order": "desc"}}]
        body['from'] = (page - 1) * 20
        body['size'] = 20
        items = es.search(index='testerhome_community', doc_type='community', body=body)
        total = items['hits']['total']
        node_items = [{
            'title': item['_source']['title'],
            'portrait': item['_source']['portrait'],
            'uname': item['_source']['username'],
            'uid': item['_source']['uid'],
            'id': item['_source']['id'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'awesome': item['_source']['awesome'],
            'comments': item['_source']['comments'],
            'release_time': get_curr_time(item['_source']['release_time']),
            'recovery_time': get_curr_time(item['_source']['recovery_time']),
        } for item in items['hits']['hits']]
        if total % 20:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        if total_page > 500:
            total_page = 500
        page_list = []
        if total_page <= 10:
            page_list = range(1, total_page + 1)
        elif page < 5:
            page_list = range(1,  11)
        elif total_page - page < 5:
            page_list = range(total_page-10, total_page+1)
        else:
            page_list = range(page-4, page+6)
        result = {'total': total, 'curr_page': page, 'page_list': page_list, 'total_page': total_page, 'up_page': page-1, 'next_page': page+1, 'keyword': keyword, 'Nid': Nid, 'nodechilds': nodechild}
        if Nid == 'bugs':
            result['bugs'] = node_items
            return render(request, 'bugs.html', result)
        elif Nid == 'questions':
            result['questionss'] = node_items
            return render(request, 'questions.html', result)
        elif Nid == 'applications':
            result['applicationss'] = node_items
            return render(request, 'applications.html', result)
        elif Nid == 'topics':
            result['topicss'] = node_items
            return render(request, 'topics.html', result)
        else:
            result['nodes'] = node_items
            return render(request, 'nodebase.html', result)

    def post(self, request):
        pass


class GetFollow(View):
    def get(self, request, Uid):
        user_result, college_result = getUserAulf(Uid)
        type = request.GET.get('follow', '')
        curr_page = request.GET.get('page', '')
        if not curr_page:
            curr_page = 1
        else:
            curr_page = int(curr_page)
        if type != 'following':
            type = 'followers'
        items = es.search(index='testerhome_follow', doc_type='follow', body={
            "query":{
                "match": {
                    "uid": Uid
                }
            }
        })
        follow = items['hits']['hits'][0]['_source'][type]
        total = len(follow)
        page_num = total // 60 + 2
        if page_num < 11:
            pageList = range(1, page_num)
        else:
            pageList = range(1, page_num)
            if curr_page < 5:
                pageList = range(1, page_num)[:10]
            elif curr_page > page_num - 5:
                pageList = range(1, page_num)[page_num - 11:]
            else:
                pageList = range(1, page_num)[curr_page - 5: curr_page + 5]
        start = (curr_page-1) * 60
        end = curr_page * 60
        if end > total:
            end = total
        follow = follow[start:end]
        return render(request, 'follow.html', {'user': user_result, 'colleges': college_result , 'uid': Uid, 'follows': follow, 'type': type, 'total': total, 'pageList': pageList, 'curr_page': curr_page, 'page_num': page_num})

    def post(self, request, Uid):
        pass


class GetFavs(View):
    def get(self, request, Uid):
        user_result, college_result = getUserAulf(Uid)
        curr_page = request.GET.get('page', '')
        if not curr_page:
            curr_page = 1
        else:
            curr_page = int(curr_page)
        items = es.search(index='testerhome_favs', doc_type='favs', body={
            "query":{
                "match": {
                    "uid": Uid
                }
            }
        })
        favs = items['hits']['hits'][0]['_source']['favs']
        total = len(favs)
        page_num = total // 25 + 2
        if page_num < 11:
            pageList = range(1, page_num)
        else:
            pageList = range(1, page_num)
            if curr_page < 5:
                pageList = range(1, page_num)[:10]
            elif curr_page > page_num - 5:
                pageList = range(1, page_num)[page_num - 11:]
            else:
                pageList = range(1, page_num)[curr_page - 5: curr_page + 5]
        start = (curr_page-1) * 25
        end = curr_page * 25
        if end > total:
            end = total
        favs = favs[start:end]
        return render(request, 'favs.html', {'type': 'favs', 'user': user_result, 'colleges': college_result, 'uid': Uid, 'favs': favs, 'total': total, 'pageList': pageList, 'curr_page': curr_page, 'page_num': page_num})

    def post(self, request, Uid):
        pass


class GetReplies(View):
    def get(self, request, Uid):
        user_result, college_result = getUserAulf(Uid)
        curr_page = request.GET.get('page', '')
        if not curr_page:
            curr_page = 1
        else:
            curr_page = int(curr_page)
        replies_items = es.search(index='testerhome_community', doc_type='community', body={
            "query": {
                "match": {
                    "comments.uid": Uid
                }
            },
            'size': 25,
            'from': (curr_page - 1) * 25,
            'sort': {
                'release_time': {
                    'order': 'desc'
                }
            }
        })
        replies_result = [{
            'title': item['_source']['title'],
            'uid': item['_source']['uid'],
            'comments': item['_source']['comments'],
            'id': item['_source']['id'],
            'recovery_username': item['_source']['recovery_username'],
            'recovery_uid': item['_source']['recovery_uid'],
            'url': item['_source']['url'],
            'flag': item['_source']['flag'],
            'release_time': get_curr_time(item['_source']['release_time']),
            'recovery_time': get_curr_time(item['_source']['recovery_time']),
        } for item in replies_items['hits']['hits']]
        repliess = []
        for result in replies_result:
            last_comment = {}
            if isinstance(result['comments'],list):
                for comment in result['comments']:
                    if 'uid' in comment.keys() and comment['uid'] == Uid:
                        last_comment = comment
                result['comments'] = last_comment
                result['comments']['date'] = get_curr_time(result['comments']['date'])
                repliess.append(result)
            elif isinstance(result['comments'],dict):
                if 'uid' in comment.keys() and comment['uid'] == Uid:
                    last_comment = comment
                result['comments'] = last_comment
                result['comments']['date'] = get_curr_time(result['comments']['date'])
                repliess.append(result)
        total = replies_items['hits']['total']
        page_num = total // 25 + 2
        if page_num < 11:
            pageList = range(1, page_num)
        else:
            pageList = range(1, page_num)
            if curr_page < 5:
                pageList = range(1, page_num)[:10]
            elif curr_page > page_num - 5:
                pageList = range(1, page_num)[page_num - 11:]
            else:
                pageList = range(1, page_num)[curr_page - 5: curr_page + 5]
        return render(request, 'replies.html', {'type': 'replies', 'user': user_result, 'colleges': college_result, 'uid': Uid, 'repliess': repliess, 'total': total, 'pageList': pageList, 'curr_page': curr_page, 'page_num': page_num})

    def post(self, request, Uid):
        pass


class GetSites(View):
    def get(self, request):
        # sites_items = es.search(index='testerhome_sites', doc_type='sites', body={"query": {"match_all": {}}})
        # sites = sites_items['hits']['hits'][0]['_source']['sites']
        sites_items = sites.find_one({})['sites']
        return render(request, 'sites.html', {'sites': sites_items, 'type': 'sites'})


class GetTTF(View):
    def get(self, request):
        # ttf_items = es.search(index='testerhome_sites', doc_type='sites', body={"query": {"match_all": {}}})
        # ttf = ttf_items['hits']['hits'][0]['_source']['ttf']
        ttf = sites.find_one({})['ttf']
        return render(request, 'sites.html', {'ttf': ttf, 'type': 'ttf'})