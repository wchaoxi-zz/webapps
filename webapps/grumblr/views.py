from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth import login, authenticate

from django.http import HttpResponse, Http404

from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator

from mimetypes import guess_type
from django.utils import timezone
import datetime

from grumblr.models import *
from grumblr.forms import *


# main page that displays global stream
@login_required
def home(request):
    posts = Post.objects.all().order_by("-postTime")
    userprof = UserProfile.objects.get(user=request.user)
    return render(request, 'grumblr/main_page.html', {'posts' : posts, 'userprof' : userprof})


@login_required
def followstream(request):
    posts = []
    myuser = User.objects.get(username=request.user)
    myprofile = UserProfile.objects.get(user=myuser)
    followinglist = myprofile.following
    for userp in followinglist.all():
        posts.extend(Post.objects.filter(user=userp.user).order_by("-postTime"))

    return render(request, 'grumblr/follower_stream.html', {'posts' : posts, 'userprof' : myprofile})


@login_required
def post(request):
    errors = []

    if request.method == 'GET':
        return home(request)

    if not 'content' in request.POST or not request.POST['content']:
        errors.append('You must enter content of a post')
    else:
        curContent = request.POST['content']
        if len(curContent) > 42:
            errors.append('Length of a post must be 42 characters or less.')
        else:
            curPost = Post(content = curContent,
                           user = request.user)
            curPost.save()

        posts = Post.objects.all().order_by("-postTime")
        userprof = UserProfile.objects.get(user=request.user)

        context = {'posts' : posts, 'errors' : errors, 'userprof' : userprof}
        return render(request, 'grumblr/main_page.html', context)


@login_required
def profile(request, user):
    context = {}

    target = get_object_or_404(User, username=user)

    myuser = User.objects.get(username=request.user)
    myprofile = UserProfile.objects.get(user=myuser)


    userprofile = UserProfile.objects.get(user=target)
    posts = Post.objects.filter(user=target).order_by("-postTime")

    if myuser != target:
        if myprofile.following.filter(user=target).count() > 0:
            context['follow'] = 'unfollow'
        else:
            context['follow'] = 'follow'

    context['userprofile'] = userprofile
    context['user'] = target
    context['posts'] = posts
    return render(request, 'grumblr/profile.html', context)


@login_required
def follow(request, user):
    myuser = User.objects.get(username=request.user)
    myprofile = UserProfile.objects.get(user=myuser)

    target = User.objects.get(username=user)
    userprofile = UserProfile.objects.get(user=target)

    if myprofile.following.filter(user=target).count() > 0:
        myprofile.following.remove(userprofile)
    else:
        myprofile.following.add(userprofile)

    return profile(request, user)


@login_required
def editprofile(request):
    profile_to_edit = get_object_or_404(UserProfile, user=request.user)
    username =  request.user

    if request.method == 'GET':
        form = EditProfileForm(instance=profile_to_edit)
        return render(request, 'grumblr/edit_profile.html', {'form' : form, 'username' : username})

    # request is post examine this and save
    form = EditProfileForm(request.POST, request.FILES, instance=profile_to_edit)


    if not form.is_valid():
        return render(request, 'grumblr/edit_profile.html', {'form': form, 'username' : username})

    form.save()

    newpassword = form.cleaned_data.get('change_pwd')
    if newpassword:
        curuser = profile_to_edit.user
        curuser.set_password(newpassword)
        curuser.save()
        login(request, curuser)

    return redirect(reverse('home'))


@login_required
def getphoto(request, user):
    current_user = get_object_or_404(User, username=user)
    current_profile = get_object_or_404(UserProfile, user=current_user)

    if not current_profile.photo:
        return Http404

    content_type = guess_type(current_profile.photo.name)
    return HttpResponse(current_profile.photo, content_type=content_type)



def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        # user = User.objects.get(username='wcx')
        return render(request, 'grumblr/signup.html', context)

    form = RegistrationForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'grumblr/signup.html', context)

    # Create user then redirect
    user = User.objects.create_user(username=request.POST['username'], \
                                    password=request.POST['password'])
    user.save()
    userprofile = UserProfile(user=user, first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'],
                                    email=request.POST['email'])
    userprofile.save()

    new_user = authenticate(username=request.POST['username'], \
                password=request.POST['password'])
    # login(request, new_user)

    token = default_token_generator.make_token(user)

    email_body = """
    Welcome to grumblr, please click on the link below to finish registration:
    http:%s%s
    """ % (request.get_host(),
           reverse('confirm', args=(user.username, token)))

    send_mail(subject="Verify Your Email",
              message=email_body,
              from_email="chaoxiw@andrew.cmu.edu",
              recipient_list=['wchaoxi@gmail.com'],
              fail_silently=False)


    context['email'] = form.cleaned_data.get('email')
    return render(request, 'grumblr/needsconfirmation.html', context)


def confirm(request, username, token):
    user = User.objects.get(username=username)
    if default_token_generator.check_token(user, token):
        login(request, user)
        return redirect(reverse('home'))

    else:
        return redirect(reverse('register'))

@login_required
def resetpassword(request):
    context = {}
    user = User.objects.get(username=request.user)
    userprofile = UserProfile.objects.get(user=user)
    token = default_token_generator.make_token(user)

    email_body = """
        Click the link below to reset password:
        http:%s%s
        """ % (request.get_host(),
               reverse('resetconfirm', args=(user.username, token)))

    send_mail(subject="Verify Your Email",
              message=email_body,
              from_email="chaoxiw@andrew.cmu.edu",
              recipient_list=[userprofile.email])

    context['email'] = userprofile.email
    return render(request, 'grumblr/re setpwd.html', context)


def confirmreset(request, username, token):
    user = User.objects.get(username=username)
    if default_token_generator.check_token(user, token):
        user.set_password("123")
        return redirect(reverse('home'))

    else:
        return redirect(reverse('home'))

@login_required
def getnewposts(request):
    timenow = timezone.now()
    timestart = timenow - datetime.timedelta(seconds=5)
    posts = Post.getnewpost(timestart, timenow)
    context = {'posts' : posts}
    return render(request, 'posts.json', context, content_type='application/json')


@login_required
def addcomments(request, postid):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        p = Post.objects.all().get(id=int(postid))
        u = User.objects.all().get(username=request.user)
        new_comment = Comment(content=request.POST['comment'],
                              owner=u)
        new_comment.save()
        p.comments.add(new_comment)

        context = {'comment' : new_comment}
        return render(request, 'comment.json', context, content_type='application/json')


