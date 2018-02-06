from django.shortcuts import render

from django.core import serializers

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

from schedule.models import Event as CalEvent
from schedule.models import Calendar, EventRelation

from .models import *
from .forms import *

# Create your views here.
@login_required(login_url="/login/")
def index(request):
   if request.method == "GET":
       events = Event.objects.filter(users=request.user)
       groups = Group.objects.filter(users=request.user)
       context = {
           'title':"Home",
           'events': events,
           'groups': groups,
           #'friends': friends
       }
       return render(request,'home.html',context)
   return HttpResponse("404")

@csrf_exempt
def events(request):
    if request.method == 'GET':
        #events = Event.objects.filter(users=request.user)
        events = Event.objects.all()
        event = {}
        event['events']=[]
        for e in events:
            event['events']+=[{
                'name': e.name,
                'time': e.datetime,
                'type': e.event_type
                }]
        return JsonResponse(event)
    if request.method == 'POST':
        return HttpResponse("POST successful")
    return HttpResponse("404")

@csrf_exempt
def groups(request):
    if request.method == 'GET':
        groups = Group.objects.filter(users = request.user)
        #groups = Group.objects.all().delete()
        group = {}
        group['groups']=[]
        for g in groups:
            group['groups']+=[{
                'title':g.title,
                'token': g.token,
                'users': serializers.serialize('json', g.users.all(), fields=('username',))
                }]
        return JsonResponse(group)
    if request.method == 'POST':
        return HttpResponse("POST successful")
    return HttpResponse("404")

@csrf_exempt
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user = {}
        user['users']=[]
        for e in users:
            user['users']+=[{
                'name': e.username,
                }]
        return JsonResponse(user)
    if request.method == 'POST':
        return HttpResponse("POST successful")
    return HttpResponse("404")

@csrf_exempt
def messages(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        message = {}
        message['message'] = []
        for m in messages:
            message['message'] += [{
            'message' : m.message,
            'handle' : m.handle,
            }]
        return JsonResponse(message)
    return HttpResponse("404")

@csrf_exempt
def rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        room = {}
        room['room'] = []
        for m in rooms:
            room['room'] += [{
            'label' : m.label,
            'name' : m.name,
            }]
        return JsonResponse(room)
    return HttpResponse("404")

@csrf_exempt
def calendars(request):
    if request.method == 'GET':
        calendars = Calendar.objects.all()
        calendar = {}
        calendar['cal'] = []
        for c in calendars:
            calendar['cal'] += [{
            'name' : c.name,
            'events': serializers.serialize('json', c.events.all()),
            }]
        return JsonResponse(calendar)
    return HttpResponse("404")

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            #login call back
            login(request,user)
            return HttpResponseRedirect('/')

    else:
        form = registration_form()
    context = {
        'title':'Register',
        'form':form
    }
    return render(request, 'register.html', context)

@csrf_exempt
def create_event(request, token):
    groups = Group.objects.filter(users = request.user)
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
           event = form.save(commit = False)
           event.users.add(request.user)
           group = Group.objects.get(token = token)
           event.group.add(group)
           event.save()
           e = CalEvent.objects.create(title=form.cleaned_data.get('name'), start = form.cleaned_data.get('datetime'), end = form.cleaned_data.get('datetime_end'))
           calendar = Calendar.objects.get(name = token)
           calendar.events.add(e)

        else:
           return HttpResponse("It did not work")
        return HttpResponseRedirect('/')
    else:
        form = EventForm()
    context = {
        'title':'Create Event',
        'form':form,
        'groups': groups,
        'token': token,
    }
    return render(request, 'create_event.html', context)

@csrf_exempt
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
           g = form.save()
           user = User.objects.get(username=request.user.username)
           g.users.add(user)
           g.save()
           Room.objects.create(label = form.cleaned_data.get('token'), name = form.cleaned_data.get('title'))
           calendar = Calendar.objects.create(name = form.cleaned_data.get('token'))
           calendar.save()
        else:
           return HttpResponse("Please enter another token. That token is already taken.")
        return HttpResponseRedirect('/')
    else:
        form = GroupForm()
    context = {
        'title':'Create Group',
        'form':form
    }
    return render(request, 'create_group.html', context)

@csrf_exempt
def enter_group(request):
   if request.method == "POST":
      form = EnterGroup(request.POST)
      if form.is_valid():
         group = Group.objects.get(token = form.cleaned_data.get('token'))
         if group:
            group.users.add(request.user)
         return HttpResponseRedirect('/')
   else:
        form = EnterGroup()
   context = {
        'title':'Enter Group',
        'form':form
   }
   return render(request, 'enter_group.html', context)

@csrf_exempt
def edit_event(request, username, id):
    record = Event.objects.get(name=id, users = request.user)
    if request.method == "POST":
        form = EventForm()
        form.name = record.name
        form.datetime = record.datetime
        form.datetime_end = record.datetime_end
        form.event_type = record.event_type
        if form.is_valid():
           form.save()
        else:
           return HttpResponse("It did not work")
        return HttpResponseRedirect('/')
    else:
        form = EventForm(instance=record)
    context = {
        'title':'Edit Event',
        'form':form,
        'groups':groups,
    }
    return render(request, 'create_event.html', context)

@csrf_exempt
def edit_group(request, username, id):
    record = Group.objects.get(title=id, users = request.user)
    if request.method == "POST":
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
           form.save()
        else:
           return HttpResponse("It did not work")
        return HttpResponseRedirect('/')
    else:
        form = GroupForm(instance=record)
    context = {
        'title':'Edit Group',
        'form':form
    }
    return render(request, 'create_group.html', context)

@csrf_exempt
def event(request, username, id):
   if request.method == "GET":
      record = Event.objects.get(name=id, users = request.user)
      form = CommentForm(request.POST)
      comments = Comment.objects.filter(event = record, user = request.user)
      if form.is_valid():
         submit = form.cleaned_data['comment']
         comment = Comment(comment = submit)
         comment.save()
      context = {
         'record' : record,
         'form' : form,
         'comments': comments
      }
   return render(request, 'event.html', context)


@csrf_exempt
def group(request, id):
   if request.method == "GET":
      record = Group.objects.get(token = id)
      events = Event.objects.filter(group = record)
      calendar = Calendar.objects.get(name = id)
      calevents = calendar.events.all()

      #usernames = serializers.serialize("json", Group.users)
      context = {
         'messages' : messages,
         'record' : record,
         'events': events,
         'calevents': calevents,
      }
   return render(request, 'group.html', context)

def chat(request, label):
    room, created = Room.objects.get_or_create(label = label)
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    context = {
       'room': room,
       'messages': messages,
    }
    return render(request, 'chat.html', context)

@csrf_exempt
def delete_event(request, username, id):
   if request.method == "GET":
      event = Event.objects.get(users = request.user, name = id).users.remove(request.user)
   return HttpResponseRedirect('/')

@csrf_exempt
def delete_group(request, username, id):
   if request.method == "GET":
      group = Group.objects.get(users = request.user, title = id)
      group.users.remove(request.user)
   return HttpResponseRedirect('/')
