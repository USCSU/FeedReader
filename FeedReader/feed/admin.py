from django.contrib import admin
from feed.models import Article, Feed
class feedAdmin(admin.ModelAdmin):
	list_display = ['url','creator']
class articleAdmin(admin.ModelAdmin):
	list_display = ['title','timestamp','feed']
admin.site.register(Feed,feedAdmin)
admin.site.register(Article,articleAdmin)
