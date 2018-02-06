from django import forms

from django.core import serializers

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.forms.widgets import DateTimeInput
from django.forms import ModelForm
from datetime import datetime

from .models import *

class registration_form(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user=super(registration_form,self).save(commit=False)
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
            private = Group(title="Private", token = self.cleaned_data['username']+"private")
            private.save()
            private.users.add(user)
        return user

class GroupForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
       user = kwargs.pop("user",None)
       super(GroupForm, self).__init__(*args, **kwargs)
    class Meta:
       model = Group
       fields = ("title", "token", "password")
       widgets = {
        'title' : forms.TextInput(attrs={ 'placeholder': 'enter name'}),
        'token' : forms.TextInput(attrs={ 'placeholder': 'enter token'}),
        'password' : forms.TextInput(attrs={ 'placeholder': 'enter password'})}
    def save(self, commit=True):
        group=super(GroupForm,self).save(commit=True)
        return group

class EventForm(ModelForm):
    def __init__(self,*args,**kwargs):
       super(EventForm, self).__init__(*args, **kwargs)
    class Meta:
       model = Event
       fields = ("name", "datetime", "datetime_end", "event_type")
       widgets = {
          'name': forms.TextInput(attrs={'placeholder':'enter name'}),
          'datetime': forms.DateTimeInput(attrs={'class':'datetime-input'}),
          'datetime_end': forms.DateTimeInput(attrs={'class':'datetime-input'}),
          'event_type': forms.CheckboxSelectMultiple(choices = ( ('availibility', 'Availibility'), ('event', 'Event') ))}
    def save(self, commit=True):
        u=super(EventForm,self).save(commit=True)
        if commit :
            u.save()
        return u

class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name':'username'
        })
    )
    password=forms.CharField(
        label="Password",
        max_length=32,
        widget=forms.PasswordInput()
    )
class EnterGroup(forms.Form):
    token=forms.CharField(
       label = "Token",
       max_length = 140,
       widget=forms.TextInput(attrs={
          'placeholder':"enter group token"
    }))
    password=forms.CharField(
       label = "Password",
       max_length = 140,
       widget=forms.TextInput(attrs={
          'placeholder':"enter group password"
    }))

class CommentForm(ModelForm):
    class Meta:
       model = Comment
       fields=('comment',)
       widgets={
           'comment': forms.TextInput()
       }
    def save(self, commit=True):
       u = super(CommentForm, self).save(commit=True)
