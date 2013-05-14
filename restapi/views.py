# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import waffle
from waffle.models import Flag
from django.contrib.auth.models import User
from restapi.models import Question, Answer
import json

def test(request):
	c = {}

	if waffle.flag_is_active(request, 'feature1'):
		c["feature11"] = "View Feature 1 is live!"
	else:
		c["feature11"] = "View Feature 1 is not available right now"

	# question module
	users = User.objects.all()

	c['question_array'] = []
	if waffle.flag_is_active(request, 'question'):
		for user in users:
			questions = Question.objects.filter(user=user.id)
			c['question_array'].append("")
			c['question_array'].append(user.username + ":")
			if questions:
				for question in questions:
					c['question_array'].append(question.question)
			else:
				c['question_array'].append("Hasn't asked any questions... sad.")

	if waffle.flag_is_active(request, 'answer'):
		c["answer_array"] = Answer.objects.all()

	c['cookie_answer'] = request.COOKIES.get('dwf_answer')
	c['cookie_question'] = request.COOKIES.get('dwf_question')
	c['cookie_feature1'] = request.COOKIES.get('dwf_feature1')

	return render_to_response('test.html',c, context_instance = RequestContext(request))

def feature_user(request, feature_number, user_number):
	# flag = Flag.objects.get(id=feature_number)
	# user = User.objects.get(id=user_number)

	# if "everyone" is already set
	feature = Flag.objects.get(id=feature_number)
	if feature.everyone == True:
		myjson = json.dumps({'active': True})
		#json = "[{'active': true }]"
		return HttpResponse(myjson)
	elif feature.everyone == False:
		myjson = json.dumps({'active': False})
		#myjson = "[{'active': false }]"
		return HttpResponse(myjson)

	# if "everyone" is unknown / null: check user
	flag_user = Flag.objects.filter(users__id=user_number, id=feature_number)

	if flag_user:
		flag_user_bool = True
	else:
		flag_user_bool = False

	if flag_user_bool:
		myjson = json.dumps({'active': True})
		return HttpResponse(myjson)

	# check cookies
	cookie_string = 'dwf_' + feature.name
	flag_cookie = request.COOKIES.get(cookie_string)

	# compare string
	if flag_cookie:
		if flag_cookie == "True":
			myjson = json.dumps({'active': True})
			return HttpResponse(myjson)
		if flag_cookie == "False":
			myjson = json.dumps({'active': False})
			return HttpResponse(myjson)

	if not flag_user_bool:
		myjson = json.dumps({'active': False})
		return HttpResponse(myjson)

	myjson = json.dumps({'active': False})
	return HttpResponse(myjson)

