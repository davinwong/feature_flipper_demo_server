from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from restapi.models import Entry, Question, Answer, Vote, Notification # ,User 
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from waffle.models import Flag
from django.db import models
from tastypie import fields, utils
from tastypie.resources import Resource
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()

    # def login(self, request, **kwargs):
    #     self.method_check(request, allowed=['post'])

    #     data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))

    #     username = data.get('username', '')
    #     password = data.get('password', '')

    #     user = authenticate(username=username, password=password)
    #     if user:
    #         if user.is_active:
    #             login(request, user)
    #             return self.create_response(request, {
    #                 'success': True
    #             })
    #         else:
    #             return self.create_response(request, {
    #                 'success': False,
    #                 'reason': 'disabled',
    #                 }, HttpForbidden )
    #     else:
    #         return self.create_response(request, {
    #             'success': False,
    #             'reason': 'incorrect',
    #             }, HttpUnauthorized )

class QuestionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    class Meta:
		queryset = Question.objects.all()
		allowed_methods = ['get', 'delete', 'post', 'put']
		authorization = Authorization()

class AnswerResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    user = fields.ForeignKey(UserResource, 'user',full=True)
    class Meta:
        queryset = Answer.objects.all()
        filtering = {
            "question": ALL_WITH_RELATIONS
        }
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()

    # def dehydrate(self, bundle):
    #     print self.user
    #     bundle.data['username'] = User.objects.get(id=int(self.user.id))

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

class VoteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    answer = fields.ForeignKey(AnswerResource, 'answer')
    class Meta:
        queryset = Vote.objects.all()
        filtering = {
            "answer": ALL_WITH_RELATIONS
        }
        allowed_methods = ['get', 'delete', 'post']
        authorization = Authorization()

class NotificationResource(ModelResource):
    user_from = fields.ForeignKey(UserResource, 'user_from')
    user_to = fields.ForeignKey(UserResource, 'user_to')

    class Meta:
        queryset = Notification.objects.all()
        filtering = {
            "user_to": ALL_WITH_RELATIONS
        }
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()