# urls.py
from django.conf.urls.defaults import *
from api import EntryResource, UserResource, QuestionResource, FlagResource, AnswerResource, VoteResource, NotificationResource
from restapi.views import test
from django.contrib import admin

admin.autodiscover()
entry_resource = EntryResource()
user_resource = UserResource()
question_resource = QuestionResource()
answer_resource = AnswerResource()
flag_resource = FlagResource()
vote_resource = VoteResource()
notification_resource = NotificationResource()

urlpatterns = patterns('',

    (r'^api/', include(entry_resource.urls)),
    (r'^api/', include(user_resource.urls)),
    (r'^api/', include(question_resource.urls)),
    (r'^api/', include(answer_resource.urls)),
    (r'^api/', include(flag_resource.urls)),
    (r'^api/', include(vote_resource.urls)),
    (r'^api/', include(notification_resource.urls)),
    (r'^test/', test),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/feature/(?P<flag_id>\d+)/user/(?P<user_id>\d+)/', 'restapi.views.feature_user'),
    (r'^api/payment/(?P<credit_card_number>\d+)/user/(?P<user_id>\d+)/', 'restapi.views.payment'),
    (r'^api/session/', 'restapi.views.session'), 
    (r'^login/', 'restapi.views.login'), 
)