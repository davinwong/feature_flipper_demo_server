from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from restapi.models import Entry, Question, Answer, Vote, Notification # ,User 
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from django.contrib.auth.models import User
from waffle.models import Flag
import waffle
from django.db import models
from tastypie import fields, utils
from tastypie.resources import Resource
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from waffle.decorators import waffle_flag




### allows us to use waffle feature lags for resources/models
def feature_user_resource(request, flag_id):

    # if waffle-"everyone"-setting is already set
    feature = Flag.objects.get(id=flag_id)
    if feature.everyone == True:
        return True
    elif feature.everyone == False:
        return False

    # create feature flag cookie if not there
    if waffle.flag_is_active(request, feature.name):
        print "waffle flag is active"
        print feature.name
    else:
        "waffle flag is not active"
        print feature.name

    # abort if not logged in
    logged_in = True
    try:
        user_cookie = request.COOKIES.get('user')
    except:
        logged_in = False
        return False

    user_id = int(user_cookie)

    # if "everyone" is unknown/null, check waffle-"user"-setting
    flag_user = Flag.objects.filter(users__id=user_id, id=flag_id)

    if flag_user:
        flag_user_bool = True
    else:
        flag_user_bool = False

    if flag_user_bool:
        return True

    # waffle-percentage-setting, find cookies
    cookie_string = 'dwf_' + feature.name
    flag_cookie = request.COOKIES.get(cookie_string)

    # compare cookie string
    if flag_cookie:
        if flag_cookie == "True":
            return True
        if flag_cookie == "False":
            return False

    if not flag_user_bool:
        return False

    return False

# upvote feature. assumes vote's flag_id = 2
class VoteFlagAuthentication(Authentication):
    def is_authenticated(self, request, object=None):
        return feature_user_resource(request, 2)

# notification feature. assumes notification's flag_id = 3
class NotificationFlagAuthentication(Authentication):
    def is_authenticated(self, request, object=None):
        return feature_user_resource(request, 3)

### tastypie resources ###

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'delete', 'post', 'put']
        authorization = Authorization()


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
        authentication = VoteFlagAuthentication()


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
        authentication = NotificationFlagAuthentication()