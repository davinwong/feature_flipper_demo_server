# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import waffle
from waffle.models import Flag
from django.contrib.auth.models import User
from restapi.models import Question, Answer
import json
from waffle.decorators import waffle_flag
from tastypie.utils import trailing_slash
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


# REST api for /feature/1/user/2/, returns True/False for whether given user should see given feature
def feature_user(request, flag_id, user_id):

    # if waffle-"everyone"-setting is already set
    feature = Flag.objects.get(id=flag_id)
    if feature.everyone == True:
        myjson = json.dumps({'active': True})
        return HttpResponse(myjson)
    elif feature.everyone == False:
        myjson = json.dumps({'active': False})
        return HttpResponse(myjson)

    # if "everyone" is unknown/null, check waffle-"user"-setting
    flag_user = Flag.objects.filter(users__id=user_id, id=flag_id)

    if flag_user:
        flag_user_bool = True
    else:
        flag_user_bool = False

    if flag_user_bool:
        myjson = json.dumps({'active': True})
        return HttpResponse(myjson)

    # waffle-percentage-setting, find cookies
    cookie_string = 'dwf_' + feature.name
    flag_cookie = request.COOKIES.get(cookie_string)

    # compare cookie string
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


# sample payment feature
@waffle_flag('payment')
def payment(request, user_id, credit_card_number):
    # fake payment processing
    if int(credit_card_number) >= 100000000000000 and int(credit_card_number) <= 999999999999999:
        myjson = json.dumps({'payment': True})

    else:
        myjson = json.dumps({'payment': False})

    return HttpResponse(myjson)


# fake login / session
@csrf_exempt
def session(request):
    if request.method == 'GET':
        cookie = request.COOKIES.get('user')
        user_id = int(cookie)
        

        if cookie:
            myjson = json.dumps({'auth': True})
        else:
            myjson = json.dumps({'auth': False})

        return HttpResponse(myjson)

    if request.method == 'POST':
        exist = True

        try:
            request_params = json.loads(request.body)
            email = request_params['email']
            user = User.objects.get(email=email)

        except:
            myjson = json.dumps({'auth': False})
            exist = False
            response = HttpResponse(myjson)
            return response

        if exist:
            print 'exist'
            myjson = json.dumps({'auth': True, 'email':email, 'username':user.username, 'id':user.id})
            response = HttpResponse(myjson)
            response.set_cookie('user', user.id, max_age=100000000)

        return response

# login test
def login(request):
    c = {}
    # if waffle.flag_is_active(request, 'vote'):
    #     print "waffle flag is active"
    #     a = 1
    # else:
    #     print "wafle flag is not active"
    #     a = 2
    return render_to_response('login.html',c, context_instance = RequestContext(request))


# random test
def test(request):
    c = {}

    if waffle.flag_is_active(request, 'feature1'):
        c["feature11"] = "View Feature 1 is live!"
    else:
        c["feature11"] = "View Feature 1 is not available right now"

    # question feature
    users = User.objects.all()

    c['question_array'] = []
    if waffle.flag_is_active(request, 'question'):
        for user in users:
            questions = Question.objects.filter(user=user.id)
            c['question_array'].append("")
            c['question_array'].append(user.username + ":")
            if questions:
                for question in questions:
                    c['question_array'].append(question.text)
            else:
                c['question_array'].append("Hasn't asked any questions... sad.")

    if waffle.flag_is_active(request, 'answer'):
        c["answer_array"] = Answer.objects.all()

    c['cookie_answer'] = request.COOKIES.get('dwf_answer')
    c['cookie_question'] = request.COOKIES.get('dwf_question')
    c['cookie_feature1'] = request.COOKIES.get('dwf_feature1')

    return render_to_response('test.html',c, context_instance = RequestContext(request))
