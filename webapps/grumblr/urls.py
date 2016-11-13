from django.conf.urls import url

import django.contrib.auth.views
import grumblr.views

urlpatterns = [
    url(r'^main$', grumblr.views.home, name='home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name': 'grumblr/signin.html'}, name='login'),
    # Use built-in log-out
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name = 'log_out'),
    # register page
    url(r'^register', grumblr.views.register, name='register'),
    url(r'^post', grumblr.views.post, name='post'),
    url(r'^profile/(?P<user>.+)$', grumblr.views.profile, name='profile'),
    url(r'^editprofile', grumblr.views.editprofile, name='editprofile'),
    url(r'^photo/(?P<user>.+)$', grumblr.views.getphoto, name='photo'),
    url(r'^follow/(?P<user>.+)$', grumblr.views.follow, name='follow'),
    url(r'^followerstream', grumblr.views.followstream, name='fstream'),
    url(r'confirmregistration/(?P<username>.+)/(?P<token>.+)$', grumblr.views.confirm, name='confirm'),
    url(r'resetclick', grumblr.views.resetpassword, name='reset'),
    url(r'resetpassword/(?P<username>.+)/(?P<token>.+)$', grumblr.views.confirmreset, name='resetconfirm'),
    url(r'getnewposts', grumblr.views.getnewposts),
    url(r'^addcomment/(?P<postid>.+)$', grumblr.views.addcomments),
]