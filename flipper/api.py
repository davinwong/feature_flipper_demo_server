from tastypie.resources import ModelResource
from restapi.models import Entry, Question, Answer # ,User 
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from waffle.models import Flag
from django.db import models
from tastypie import fields, utils
from tastypie.resources import Resource

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()

class QuestionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
		queryset = Question.objects.all()
		allowed_methods = ['get', 'delete', 'post', 'put']
		authorization = Authorization()

class AnswerResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()

class EntryResource(ModelResource):
    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        authorization = Authorization()

class FlagResource(ModelResource):
    class Meta:
        queryset = Flag.objects.all()
        resoure_name = 'flag'
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()