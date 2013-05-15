from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Entry(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Entry, self).save(*args, **kwargs)

class Question(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

class Answer(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    question = models.ForeignKey('Question')
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey('Answer')

    def __unicode__(self):
        return self.user.username + ": " + self.answer.text

class Notification(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    user_from = models.ForeignKey(User, related_name='user_from')
    user_to = models.ForeignKey(User, related_name='user_to')

    def __unicode__(self):
        return self.user_from.username + " to " + self.user_to.username + ": " + self.message 



