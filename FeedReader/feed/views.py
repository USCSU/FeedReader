from django.shortcuts import render
from feed.models import FeedToSubscribers,Feed,User,Article
from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from django.template import RequestContext
from dateutil import parser
import ast
import json
def index(request):
	if request.user.is_authenticated():
		return render(request,'feed/index.html',RequestContext(request))
	else:
		return HttpResponse("You are not authorized to access this page")

def addArticle(request):#add article to feed can we add article to other user?
	# Authentication
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/addArticle_response.html',{'data':json.dumps(newData)})


	if request.method == 'GET':
		return render(request,'feed/addArticle.html',{'username':username})
	else:
		try: #exception control to avoid invalid input, and return corresponding json response
			data = json.loads(request.POST.get('content')) # change into json format
			title = data['title']
			content = data['content']
			feed=data['feed']
			currentUser = User.objects.get(username = username)
			feedinstance=Feed.objects.filter(name =feed).filter(creator=currentUser) # get all feeds collections of current user
			# can't add articles to other's feed
			if not feedinstance:
				newData = {'status':400, 'exception':'Feed not existed in your collections'}
				return render(request,'feed/addArticle_response.html',{'data':json.dumps(newData)})
			# duplicate title and content in feed is allowed.

			feedid = Feed.objects.get(name = feed) #get feed object
			# save db
			articleEntry = Article(title = title, content=content, feed=feedid,timestamp=datetime.now())
			articleEntry.save()



			newData = {
			'status': 200,
			'title': title,
			'content':content,
			'feed':feed,
			'action':'add article',
			'media type':'application/json',
			}
		except :#exception happened: give limited notification to users

			newData = {
				'status':400,
				'exception':'wrong json format/[title], [content], [feed] are a must in the messgae body',
			}
			return render(request,'feed/addArticle_response.html',{'data':json.dumps(newData)})
		return render(request,'feed/addArticle_response.html',{'data':json.dumps(newData)})
def addFeeds(request):
	#authentications
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/addFeed_response.html.html',{'data':json.dumps(newData)})


	
	if request.method == 'GET': #display for brower api
		return render(request,'feed/addFeed.html',{'username':username})
	elif request.method == 'POST':
		try:#avoid all misleading operation exception
			data = json.loads(request.POST.get('content')) # change into json format
			url = data['url']
			name = data['name']

			#check feed name is in the db: duplicate feed name is not allowed
			if  Feed.objects.filter(name =name):
				newData = {'status':400, 'exception':'Duplicated:Feed is existed'}
				return render(request,'feed/addFeed_response.html',{'data':json.dumps(newData)})
			
			#get user name 
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
		return render(request,'feed/addFeed_response.html',{'data':json.dumps(newData)})
# test more after article add
def getArticles(request): #checked
	#authentications
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/getArticles.html',{'data':json.dumps(newData)})


	if request.method == 'GET':
		data = {}
		articles={}
		# get all feeds
		user = User.objects.get(username = username)
		relations = FeedToSubscribers.objects.filter(subscriber = user)
		feeds = [x.feed for x in relations]
		if not feeds: #feed is empty
			data = {
				'status': 204,
				'result': 'empty',
				'subscriber':username,
				'media_type':'application/json'
			}
		else: #have feeds there
			idx=1 # for index purpose to display in json
			for singleFeed in feeds: #for each feed
				singleArticles = Article.objects.filter(feed = singleFeed) # get all articles
				for item in singleArticles: # add each article detials into dict
					temp={}
					temp['title'] = item.title
					temp['content'] = item.content
					articles[idx] = temp
					idx=idx+1
			
			if not articles:# not articles yet
				data = {
					'status': 204,
					'result': 'empty',
					'subscriber':username,
					'media_type':'application/json'
				}
			else:# we have articles set
				data = {'status':200,'subscriber':username,'media_type':'application/json'}
				data['articles']=articles # add all articles to json data
		#get all articles for each feeds
		return render(request,'feed/getArticles.html',{'data':data})
	else : #post
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/getArticles.html',{'data':data})

def getFeeds(request):
	#authentications
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/getFeeds.html',{'data':json.dumps(newData)})


	if request.method == 'GET':
		#get current user
		user = User.objects.get(username = username)
		#check current users' subscriptions
		relations = FeedToSubscribers.objects.filter(subscriber = user)#relation set here
		#get set of all feeds subscribers ordered
		feeds = [x.feed for x in relations]
		#empty feed set
		if not feeds:
			data = {
				'status': 204,
				'result': 'empty',
				'subscriber':username,
				'media_type':'application/json'
			}
		else:
			data = {'status':200,'subscriber':username,'media_type':'application/json'}
			#prepare all json response
			entries = {}
			for idx, entry in enumerate(feeds):
				temp={}
				temp['name'] = entry.name
				temp['url'] = entry.url
				entries[idx+1] = temp
			data['result'] = entries
		return render(request,'feed/getFeeds.html',{'data':data})
	else : #post not supported: 404 is bad request
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/getFeeds.html',{'data':data})

def subscribe(request): #subscribe user to a feed, the feed can be anyone's 
	#authentications
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})


	if request.method == 'GET':
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/subscribeFeed.html',{'username':username})

	if request.method == 'POST':
		try: # catch any misleading operation exception
			data = json.loads(request.POST.get('content')) # change into json format
			feed = data['feed'] #reader feed object
			
			#check feed name is in the db
			if not Feed.objects.filter(name =feed):
				newData = {'status':400, 'exception':'Feed not existed'}
				return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})
			
			userid = User.objects.get(username = username)
			feedid = Feed.objects.get(name = feed)
			
			#check if subscription is already there
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
			'user': username,
			'feed':feed,
			'action':'subscribe',
			'media type':'application/json',
			}
		except :
			newData = {
				'status':400,
				'exception':'wrong json format/[feed]  is a must in the messgae body',
			}
		return render(request,'feed/subscribe_response.html',{'data':json.dumps(newData)})

def unsubscribe(request):
	#authentications
	username= None
	if request.user.is_authenticated():
		username = request.user.username
	else: #If user is not authenticated,return corresponding api error code: 
		newData = {
			'status': 401, #bad credential
			'media type':'application/json',
			'exception': 'credential failed. Please check your username and password'
			}
		return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(newData)})

	if request.method == 'GET':
		data = {'status':404,'media_type':'application/json'}
		return render(request,'feed/unsubscribeFeed.html',{'username':username})
	if request.method == 'POST':
		try:
			data = json.loads(request.POST.get('content')) # change into json format
			feed = data['feed']
			
			#check feed name is in the db
			if not Feed.objects.filter(name =feed):
				newData = {'status':400, 'exception':'Feed not existed '}
				return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(newData)})
			
			userid = User.objects.get(username = username)
			feedid = Feed.objects.get(name = feed)
			
			# save db -> remove subscription
			subEntry = FeedToSubscribers.objects.filter(feed = feedid).filter(subscriber=userid)
			if not subEntry:
				data = {'status':404,'exception':'you haven not subscribed this feed','media_type':'application/json'}
				return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(data)})
				
			subEntry.delete()

			newData = {
			'status': 200,
			'user': username,
			'feed':feed,
			'action':'unsubscribe',
			'media type':'application/json',
			}
		except :
			newData = {
				'status':400,
				'exception':'wrong json format/[feed]  is a must in the messgae body',
			}
		return render(request,'feed/unsubscribe_response.html',{'data':json.dumps(newData)})
