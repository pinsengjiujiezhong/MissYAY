"""testhome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from article.views import GetArticle, Index, GetCommunity, Search, getUser, GetTopics, GetCollege, GetCollegeDetail, \
    GetCollegeUser, GetQuestions, GetNode, GetFollow, GetFavs, GetReplies, GetSites, GetTTF
from django.views.static import serve
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^searcharticle/$', GetArticle.as_view(), name='get_article'),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^community/(?P<Cid>.+)/$', GetCommunity.as_view(), name='community'),
    url(r'^userinfo/(?P<Uid>.+)$', getUser.as_view(), name='userinfo'),
    url(r'^topics/(?P<Uid>.+)$', GetTopics.as_view(), name='gettopics'),
    url(r'^questions/$', GetQuestions.as_view(), name='get_questions'),
    url(r'^node/(?P<Nid>.+)$', GetNode.as_view(), name='get_node'),
    url(r'^college/$', GetCollege.as_view(), name='get_college'),
    url(r'^collegedetail/(?P<Uid>.+)/$', GetCollegeDetail.as_view(), name='get_college_detail'),
    url(r'^collegeuser/(?P<Uid>.+)/$', GetCollegeUser.as_view(), name='get_college_user'),
    url(r'^follow/(?P<Uid>.+)/$', GetFollow.as_view(), name='get_follow'),
    url(r'^favs/(?P<Uid>.+)/$', GetFavs.as_view(), name='get_favs'),
    url(r'^replies/(?P<Uid>.+)/$', GetReplies.as_view(), name='get_replies'),
    url(r'^sites/$', GetSites.as_view(), name='get_sites'),
    url(r'^ttf/$', GetTTF.as_view(), name='get_ttf'),
    # url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
