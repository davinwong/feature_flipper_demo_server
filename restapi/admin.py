from django.contrib import admin
from django.contrib.auth.models import User
from restapi.models import Question, Answer, Vote

# class UserAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(User, UserAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Answer, AnswerAdmin)

class VoteAdmin(admin.ModelAdmin):
	pass
admin.site.register(Vote, VoteAdmin)