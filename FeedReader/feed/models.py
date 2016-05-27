from django.db import models
from django.contrib.auth.models import User
class Feed(models.Model):
	url = models.CharField(max_length=256)
	name = models.CharField(max_length=100)
	creator = models.ForeignKey(User)
	def __unicode__(self):
		return self.url

class Article(models.Model):
	title = models.CharField(max_length = 80)
	content = models.TextField()
	timestamp = models.DateTimeField()
	feed = models.ForeignKey(Feed)
	def __unicode__(self):
		return self.title

class FeedToSubscribers(models.Model):
	feed = models.ForeignKey(Feed)
	subscriber = models.ForeignKey(User)
	 
