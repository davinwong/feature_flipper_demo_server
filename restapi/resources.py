from tastypie.resources import ModelResource
from restapi.models import User, Question
from tastypie.authorization import Authorization


class UserResource(ModelResource):
    class Meta:
        queryset = models.User.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class QuestionResource(ModelResource):
	class Meta:
		queryset = models.Question.objects.all()
		allowed_methods = ['get']