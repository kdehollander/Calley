from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from schedule.models import Event, EventRelation, Calendar

# Create your models here.

class Group(models.Model):
    title = models.CharField(max_length=140)
    token = models.CharField(max_length=140, unique = True)
    password = models.CharField(max_length=140)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class Event(models.Model):
    name = models.CharField(max_length=140)
    datetime = models.DateTimeField()
    datetime_end = models.DateTimeField()
    group = models.ManyToManyField(Group)
    event_type = models.CharField(max_length = 64)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.OneToOneField(User)
    event = models.OneToOneField(Event)
    comment = models.CharField(max_length = 140)

class Room(models.Model):
   name = models.TextField()
   label = models.SlugField(unique =True)

   def __unicode__(self):
        return self.label

class Message(models.Model):
   room = models.ForeignKey(Room, related_name='messages')
   handle = models.TextField()
   message = models.TextField()
   timestamp = models.DateTimeField(default=timezone.now, db_index = True)

   def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())
   @property
   def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

   def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
