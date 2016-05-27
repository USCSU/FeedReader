from django.conf.urls import include, url
from django.contrib import admin
from feed import views as feed
from login import views as login
from feed import views as feed
urlpatterns = [
    # Examples:
    url(r'^$', login.home, name='home'),
    url(r'^signUp/$', login.signUp, name='signup'),
    url(r'^subscribe/feeds/$',feed.subscribe,name = 'subscribe'),
    url(r'^unsubscribe/feeds/$',feed.unsubscribe,name = 'unsubscribe'),
    url(r'^add/articles/$',feed.addArticle,name = 'addArticle'),
    url(r'^articles/$',feed.getArticles,name = 'getArticles'),
    url(r'^feeds/$',feed.getFeeds,name = 'getAllFeeds'),
    url(r'^add/feeds/$',feed.addFeeds,name = 'addFeeds'),
    url(r'^change_password/$',login.passwordChange,name = 'passwordchange'),
    url(r'^logout/$','django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^index/$', feed.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
