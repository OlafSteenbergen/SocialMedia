from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, CommentPost
from itertools import chain
import random
from collections import Counter


# Create your views here.

def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    all_users = Profile.objects.all()

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':posts.order_by('-created_at'), 'all_users':all_users})

def search(request):
    searchterm = request.POST['searchterm']
    posts = Post.objects.filter(caption__icontains=searchterm)
    search_NoPost = len(posts)
    user_profile = Profile.objects.get(user=User.objects.get(username=request.user.username))
    
    #create suggested keywords
    keywords = []
    for post in Post.objects.all():
        keywords += post.caption.split()    
    keywords_count = list(Counter(keywords).most_common(5))
    occurences = [x[1] for x in keywords_count]
    words = [x[0] for x in keywords_count]
        
    return render(request, 'search.html', {'posts':posts, 
                                           'searchterm':searchterm, 
                                           'search_NoPost': search_NoPost, 
                                           'user_profile': user_profile, 
                                           'words': words,
                                           'occurences': occurences})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        location = request.POST['location']


        new_post = Post.objects.create(user=user_profile, image=image, caption=caption, location=location)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def updatepost(request):
    post_id = request.GET.get('post_id')
    
    if request.method == 'POST':
        caption = request.POST['caption']
        location = request.POST['location']
    
        Post.objects.filter(id=post_id).update(caption=caption, location=location)
    
    return redirect('/')

@login_required(login_url='signin')
def deletepost(request):
    post_id = request.GET.get('post_id')
    Post.objects.filter(id=post_id).delete()    
    return redirect('/')

@login_required(login_url='signin')
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def commentpost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    comment = request.POST['comment']
    
    if not comment:
        messages.info(request, 'Empty comment, please type text.')
        return redirect('/')
    else:
        CommentPost.objects.create(post_id=post_id, username=username, comment=comment).save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user__user__username=pk)

    return render(request, 'profile.html', {'user_object': user_object,'user_profile': user_profile,'user_posts': user_posts})

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
