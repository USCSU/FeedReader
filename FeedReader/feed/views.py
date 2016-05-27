from django.shortcuts import render
from feed.models import FeedToSubscribers,Feed,User,Article
from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
import ast
import json
def index(request):
	if request.user.is_authenticated():
		return render(request,'feed/index.html',RequestContext(request))
	else:
		return HttpResponse("You are not authorized to access this page")
def addArticle(request):
	username = None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		return render(request,'feed/addArticle.html',{'username':username})
	else:
		return render(request,'feed/addArticle_response.html',{'username':username})
		# return HttpResponse('<p>add article</p>')
def addFeeds(request):
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		return render(request,'feed/addFeed.html',{'username':username})
	elif request.method == 'POST':
		try:
			data = json.loads(request.POST.get('content')) # change into json format
			url = data['url']
			name = data['name']
			print url
			print name
			#check feed name is in the db
			if  Feed.objects.filter(name =name).filter(url=url):
				newData = {'status':400, 'exception':'Feed name and/or url is existed'}
				return render(request,'feed/addFeed_response.html',{'data':json.dumps(newData)})
			
			userid = User.objects.get(username = username)
			# save db
			feedEntry = Feed(url = url, name=name, creator=userid)
			feedEntry.save()



			newData = {
			'status': 200,
			'url': url,
			'name':name,
			'action':'add feed',
			'media type':'application/json',
			}
		except :

			newData = {
				'status':400,
				'exception':'wrong json format/[url] and [name] is a must in the messgae body',
			}
		#process feed adding
		print newData
		return render(request,'feed/addFeed_response.html',{'data':json.dumps(newData)})
# test more after article add
def getArticles(request):
	username = None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		data = {}
		articles={}
		# get all feeds
		user = User.objects.get(username = username)
		feeds = Feed.objects.filter(creator = user)
		if not feeds:
			data = {
				'status': 204,
				'result': 'empty',
				'creator':username,
				'media_type':'application/json'
			}
		else:
			idx=1
			for singleFeed in feeds:
				singleArticles = Article.objects.filter(feed = singleFeed)
				for item in singleArticles:
					temp={}
					temp['title'] = item.title
					temp['content'] = item.content
					articles[idx] = temp
					idx=idx+1
			
			if not articles:
				data = {
					'status': 204,
					'result': 'empty',
					'creator':username,
					'media_type':'application/json'
				}
			else:
				data = {'status':200,'creator':username,'media_type':'application/json'}
				data['articles']=articles
		#get all articles for each feeds
		return render(request,'feed/getArticles.html',{'data':data})
	else :
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/getFeeds.html',{'data':data})

def getFeeds(request):
	username = None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		user = User.objects.get(username = username)
		feeds = Feed.objects.filter(creator = user)
		if not feeds:
			data = {
				'status': 204,
				'result': 'empty',
				'creator':username,
				'media_type':'application/json'
			}
		else:
			data = {'status':200,'creator':username,'media_type':'application/json'}
			entries = {}
			for idx, entry in enumerate(feeds):
				temp={}
				temp['name'] = entry.name
				temp['url'] = entry.url
				entries[idx+1] = temp
			data['result'] = entries
		return render(request,'feed/getFeeds.html',{'data':data})
	else :
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/getFeeds.html',{'data':data})

def subscribe(request):
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		return render(request,'feed/subscribeFeed.html',{'username':username})

	if request.method == 'POST':
		try:
			data = json.loads(request.POST.get('content')) # change into json format
			user = data['user']
			feed = data['feed']
			#check feed name is in the db
			if not Feed.objects.filter(name =feed):
				newData = {'status':400, 'exception':'Feed not existed in the system'}
				return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})
			userid = User.objects.get(username = user)
			feedid = Feed.objects.get(name = feed)
			if FeedToSubscribers.objects.filter(feed = feedid).filter(subscriber=userid):
				newData = {
					'status':400,
					'exception':'duplicate subscription'
				}
				return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})
			# save db
			subEntry = FeedToSubscribers(feed = feedid, subscriber=userid)
			subEntry.save()



			newData = {
			'status': 200,
			'user': user,
			'feed':feed,
			'action':'subscribe',
			'media type':'application/json',
			}
		except :
			newData = {
				'status':400,
				'exception':'wrong json format/[feed] and [user] is a must in the messgae body',
			}
		#process subscribe

		return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})
def unsubscribe(request):
	username = None
	if request.user.is_authenticated():
		username = request.user.username
	if request.method == 'GET':
		return render(request,'feed/unsubscribeFeed.html',{'username':username})

	if request.method == 'POST':
		try:
			data = json.loads(request.POST.get('content')) # change into json format
			user = data['user']
			feed = data['feed']
			#check feed name is in the db
			if not Feed.objects.filter(name =feed):
				newData = {'status':400, 'exception':'Feed not existed in the system'}
				return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(newData)})
			userid = User.objects.get(username = user)
			feedid = Feed.objects.get(name = feed)
			# save db
			subEntry = FeedToSubscribers.objects.filter(feed = feedid).filter(subscriber=userid)
			subEntry.delete()

			newData = {
			'status': 200,
			'user': user,
			'feed':feed,
			'action':'unsubscribe',
			'media type':'application/json',
			}
		except :
			newData = {
				'status':400,
				'exception':'wrong json format/[feed] and [user] is a must in the messgae body',
			}
		#process subscribe

		return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(newData)})
