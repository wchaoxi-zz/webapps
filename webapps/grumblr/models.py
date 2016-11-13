from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape


class Comment(models.Model):
    content = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    postTime = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.content + "---comment on:" + self.postTime.strftime("%Y-%m-%d %H:%M:%S")

    def html(self):
        return "<li>" \
               "<img src='/grumblr/photo/%s' class='img-rounded' style='height: 20px; width: 20px'>" \
               "<a href='grumblr/profile/%s'> %s</a>:%s" \
               "</li>"\
                % (self.owner, self.owner, self.owner, escape(self.__unicode__()))

class Post(models.Model):
    content = models.CharField(max_length=42)
    postTime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    comments = models.ManyToManyField(Comment)


    def __unicode__(self):
        return self.content + "---" + self.postTime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getnewpost(start, end):
        return Post.objects.all().filter(postTime__range=[start, end]).order_by('postTime')

    @property
    def html(self):
        return "<div class='well' id='%d'>" \
               "<img src='/grumblr/photo/%s' class='img-rounded' style='height: 20px; width: 20px'>" \
               "<a href='/grumblr/profile/%s'> %s</a>:%s<br>" \
               "<input type='text' required><button class='comment'>Comment</button>" \
               "<ul></ul>" \
               "</div>"\
               % (self.id, self.user, self.user, self.user, escape(self.__unicode__()))


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default="", blank=True)
    age = models.CharField(max_length=20, default="", blank=True)
    bio = models.TextField(max_length=420, default="", blank=True)
    email = models.CharField(max_length=200)
    change_pwd = models.CharField(max_length=200, default="", blank=True)
    confirm = models.CharField(max_length=200, default="", blank=True)
    photo = models.ImageField(upload_to="images", blank=True)
    following = models.ManyToManyField("self")
