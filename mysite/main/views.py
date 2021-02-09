from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cloudinary.forms import cl_init_js_callbacks
from .form import UserForm, RegForm, ImgForm, PostForm
from .models import Profile, Post, FolloweFollowing, LikeDislike


@login_required(login_url='home')
def root(request):
    return redirect('profile2')

def home(request):
    try:
        if request.user.is_authenticated:
            return redirect('profile2')
    except Exception:
        pass
    uncorrect_user = False
    if request.method == 'POST':
        try:
            form = UserForm(request.POST)
            uncorrect_user = False
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect(reverse('profile', args=(user.username,)))
            else:
                uncorrect_user = True
        except Exception:
            return render(request, 'home.html', {'form': UserForm(), 'fl': uncorrect_user})
    form = UserForm()
    context = {
        'form': form,
        'fl': uncorrect_user
    }
    return render(request, 'home.html', context)


def register(request):
    is_exist = False
    fields_not_filled = False
    if request.method == 'POST':
        form = RegForm(request.POST)
        is_exist = True if (User.objects.filter(username=form.instance.username).exists()
                            or User.objects.filter(email=form.instance.email).exists()) else False
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'),
                                            request.POST.get('password'))
            login(request, user)
            return redirect(reverse('profile', args=(user.username,)))
        else:
            fields_not_filled = True
    form = RegForm()
    context = {
        'form': form,
        'fl1': is_exist,
        'fl2': fields_not_filled
    }
    return render(request, 'registration.html', context)


@login_required(login_url='/')
def profile(request, name):
    if name:
        cur_request_user = True if (request.user.username == name) else False
        buf = User.objects.get(username=name)
        user = Profile.objects.get(user=buf)
        posts = Post.objects.filter(username=user)
        main = Profile.objects.get(user=request.user)
        subscribed = True if FolloweFollowing.objects.filter(username=main, following_user=user).exists() else False
        if request.method == 'POST':
            form = ImgForm(request.POST, request.FILES)
            if form.is_valid():
                Profile.objects.filter(user=buf).update(avatar=form.instance.avatar)
                user.avatar = form.instance.avatar
                user.save()
                img_obj = form.instance.avatar
            else:
                img_obj = user.avatar
        else:
            form = ImgForm()
            img_obj = user.avatar
        if not subscribed:
            if request.method == 'POST':
                fol = FolloweFollowing.objects.create(username=main, following_user=user)
                return redirect('profile2')
        else:
            if request.method == 'POST':
                fol = FolloweFollowing.objects.filter(username=main, following_user=user).delete()
                return redirect('profile2')
        context = {
            'form': form,
            'username': buf.username,
            'avatar': img_obj,
            'posts': posts,
            'fl': cur_request_user,
            'subscribed': subscribed,
            'followers': FolloweFollowing.objects.filter(following_user=user)[:10],
            'followed': FolloweFollowing.objects.filter(username=user)[:10]
        }
        return render(request, 'profile.html', context)
    else:
        redirect('home')

def loggout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='home')
def profile2(request):
    buf = User.objects.get(username=request.user.username)
    user = Profile.objects.get(user=buf)
    posts = Post.objects.filter(username=user)
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            Profile.objects.filter(user=buf).update(avatar=form.instance.avatar)
            user.avatar = form.instance.avatar
            user.save()
            img_obj = form.instance.avatar
        else:
            img_obj = user.avatar
    else:
        form = ImgForm()
        img_obj = user.avatar
    context = {
        'form': form,
        'username': buf.username,
        'avatar': img_obj,
        'posts': posts,
        'fl': True,
        'subscribed': True,
        'followers': FolloweFollowing.objects.filter(following_user=user)[:10],
        'followed': FolloweFollowing.objects.filter(username=user)[:10]
    }
    return render(request, 'profile.html', context)

@login_required(login_url='home')
def add_post(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        form.instance.username = Profile.objects.get(user=user)
        form.instance.date = datetime.now()
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', args=(user.username,)))
    context = {
        'form': PostForm(),
    }
    return render(request, 'addpost.html', context)


@login_required(login_url='home')
def all_posts(request):
    posts = Post.objects.all().order_by('-like_num')
    context = {
        'posts': posts
    }
    return render(request, 'posts.html', context)


@login_required(login_url='home')
def feed(request):
    my_following = FolloweFollowing.objects.filter(username=Profile.objects.get(user=request.user)).values('following_user')
    posts = Post.objects.filter(username__in=my_following)
    context = {
        'posts': posts
    }
    return render(request, 'posts.html', context)


@login_required(login_url='home')
def like(request, what):
    post = Post.objects.get(id=what)
    if request.method == 'POST':
        if LikeDislike.objects.filter(user=Profile.objects.get(user=request.user), post=post).exists():
            obj = LikeDislike.objects.get(user=Profile.objects.get(user=request.user), post=post)
            if obj.likes:
                obj.likes = False
                obj.dislikes = False
                post.like_num -= 1
            elif obj.dislikes:
                obj.likes = True
                obj.dislikes = False
                post.like_num += 1
                post.dislike_num -= 1
            else:
                obj.likes = True
                obj.dislikes = False
                post.like_num += 1
            obj.save()
            post.save()
        else:
            LikeDislike.objects.create(user=Profile.objects.get(user=request.user), post=post, likes=True, dislikes=False)
            post.like_num += 1
            post.save()
    return redirect('posts')

@login_required(login_url='home')
def dislike(request, what):
    post = Post.objects.get(id=what)
    if request.method == 'POST':
        if LikeDislike.objects.filter(user=Profile.objects.get(user=request.user), post=post).exists():
            obj = LikeDislike.objects.get(user=Profile.objects.get(user=request.user), post=post)
            if obj.dislikes:
                obj.likes = False
                obj.dislikes = False
                post.dislike_num -= 1
            elif obj.likes:
                obj.likes = False
                obj.dislikes = True
                post.like_num -= 1
                post.dislike_num += 1
            else:
                obj.likes = False
                obj.dislikes = True
                post.dislike_num += 1
            obj.save()
            post.save()
        else:
            LikeDislike.objects.create(user=Profile.objects.get(user=request.user), post=post, likes=False, dislikes=True)
            post.dislike_num += 1
            post.save
    return redirect('posts')