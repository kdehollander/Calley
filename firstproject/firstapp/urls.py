from django.conf.urls import url, include

from . import views
from schedule.views import *

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'events/$',views.events, name='events'),
    url(r'groups/$',views.groups, name='groups'),
    url(r'register/$',views.register, name='register'),
    url(r'create_event/group=(?P<token>.+)/$',views.create_event, name='create_event'),
    url(r'create_group/$',views.create_group, name='create_group'),
	url(r'^user=(?P<username>.+)/event=(?P<id>.+)/edit/$', views.edit_event, name='edit_event'),
	url(r'^user=(?P<username>.+)/group=(?P<id>.+)/edit/$', views.edit_group, name='edit_group'),
	url(r'^user=(?P<username>.+)/event=(?P<id>.+)/delete/$', views.delete_event, name='delete_event'),
	url(r'^user=(?P<username>.+)/group=(?P<id>.+)/delete/$', views.delete_group, name='delete_group'),
    url(r'enter_group/$',views.enter_group, name='enter_group'),
	url(r'^user=(?P<username>.+)/event=(?P<id>.+)/$', views.event, name='event'),
	url(r'^view/(?P<id>.+)/$', views.group, name='group'),
	url(r'users/$', views.users, name='users'),
    url(r'messages/$', views.messages, name='messages'),
    url(r'rooms/$', views.rooms, name='rooms'),
    url(r'calendars/$', views.calendars, name='calendars'),
    url(r'^chat/(?P<label>[\w-]{,50})/$', views.chat, name="chat")
]
