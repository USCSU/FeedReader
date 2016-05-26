from django.conf.urls import include, url
from django.contrib import admin
from feed import views as feed
from login import views as login
urlpatterns = [
    # Examples:
    url(r'^$', login.home, name='home'),
    url(r'^signUp/$', login.signUp, name='signup'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^logout/$','django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
]
