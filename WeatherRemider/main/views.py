import os
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
import requests
from .serializers import UserSerializer, SubscribeSerializer, CitySerializer
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .form import UserForm, RegForm, CityForm, SubForm
from .models import Subscribe, City


WEATHER_URL = 'https://api.weatherbit.io/v2.0/current?key='


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]


@login_required(login_url='home')
def root(request):
    return redirect('profile')


def home(request):
    try:
        if request.user.is_authenticated:
            return redirect('profile')
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
                return redirect('profile')
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
            return redirect('profile')
        else:
            fields_not_filled = True
    form = RegForm()
    context = {
        'form': form,
        'fl1': is_exist,
        'fl2': fields_not_filled
    }
    return render(request, 'registration.html', context)


@login_required(login_url='home')
def profile(request):
    user = User.objects.get(username=request.user.username)
    subs = Subscribe.objects.filter(follower=user).all()
    context = {
        'username': user.username,
        'subs': subs,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='home')
def add_city(request):
    if request.method == 'GET':
        form = CityForm(request.GET)
        sub = requests.get(f'{WEATHER_URL}{os.environ.get("WEATHER_API_KEY")}&city={request.GET.get("name")}')
        if sub and request.GET.get('name'):
            city_name = sub.text.split(',')[11].split('"')[3]
            return render(request, 'city.html', {'form': form, 'form2': SubForm(),
                                                 'city': city_name, 'fl': False})
        elif (not City.objects.filter(name=request.GET.get('name')).exists()) and request.GET.get('name'):
            return render(request, 'city.html', {'form': form, 'form2': SubForm(), 'city': None, 'fl': False})
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        sub = requests.get(f'{WEATHER_URL}{os.environ.get("WEATHER_API_KEY")}&city={request.GET.get("name")}')
        form2 = SubForm(request.POST)
        city_name = sub.text.split(',')[11].split('"')[3]
        if Subscribe.objects.filter(follower=user, following=city_name).exists():
            sub = Subscribe.objects.get(follower=user, following=city_name)
            period = PeriodicTask.objects.get(name=sub.id)
            sub.notification_period = request.POST.get('notification_period')
            period.interval = IntervalSchedule.objects.get(every=sub.notification_period, period='hours') if \
                IntervalSchedule.objects.filter(every=sub.notification_period, period='hours').exists() else \
                IntervalSchedule.objects.create(every=sub.notification_period, period='hours')
            period.save()
            sub.save()
        else:
            sub = Subscribe.objects.create(follower=user, following=city_name,
                                           notification_period=request.POST.get('notification_period'))
            inter = IntervalSchedule.objects.get(every=sub.notification_period, period='hours') if \
                IntervalSchedule.objects.filter(every=sub.notification_period, period='hours').exists() else \
                IntervalSchedule.objects.create(every=sub.notification_period, period='hours')
            period = PeriodicTask.objects.create(
                name=str(sub.id),
                task='tasker',
                interval=inter,
                args=[sub.id],
                start_time=timezone.now(),
            )
            period.save()
        return render(request, 'city.html', {'form': CityForm(), 'form2': form2,
                                             'city': request.GET.get("name"), 'fl': False})
    return render(request, 'city.html', {'form': CityForm(), 'form2': SubForm(), 'city': None, 'fl': True})


@login_required(login_url='home')
def city(request, name):
    notify = Subscribe.objects.get(following=name).notification_period
    city_name = name
    user = User.objects.get(username=request.user.username)
    notify = Subscribe.objects.get(follower=user, following=city_name).notification_period \
        if Subscribe.objects.filter(follower=user, following=city_name).exists() else 0
    if request.method == 'POST':
        if Subscribe.objects.filter(follower=user, following=city_name).exists():
            obj = Subscribe.objects.get(follower=user, following=city_name)
            period = PeriodicTask.objects.get(name=obj.id)
            form = SubForm(request.GET)
            if request.POST.get('notification_period'):
                obj.notification_period = request.POST.get('notification_period')
                period.interval = IntervalSchedule.objects.get(every=obj.notification_period, period='hours') if \
                    IntervalSchedule.objects.filter(every=obj.notification_period, period='hours').exists() else \
                    IntervalSchedule.objects.create(every=obj.notification_period, period='hours')
                period.save()
                obj.save()
                notify = request.POST.get('notification_period')
                return redirect(reverse('city', args=(name,)))
            PeriodicTask.objects.filter(name=Subscribe.objects.get(follower=user, following=city_name).id).delete()
            Subscribe.objects.filter(follower=user, following=city_name).delete()
            return redirect(reverse('city', args=(name,)))
        obj = Subscribe.objects.create(follower=user, following=city_name, notification_period=2)
        inter = IntervalSchedule.objects.get(every=obj.notification_period, period='hours') if \
            IntervalSchedule.objects.filter(every=obj.notification_period, period='hours').exists() else \
            IntervalSchedule.objects.create(every=obj.notification_period, period='hours')
        period = PeriodicTask.objects.create(
            name=str(obj.id),
            task='tasker',
            interval=inter,
            args=[obj.id],
            start_time=timezone.now(),
        )
        period.save()
        notify = 2
        return redirect(reverse('city', args=(name,)))
    sub = True if Subscribe.objects.filter(follower=user, following=city_name).exists() else False
    data = requests.get(f'{WEATHER_URL}{os.environ.get("WEATHER_API_KEY")}&city={name}')
    data.text[data.text.find('"wind_dir"')]
    return render(request, 'city_prof.html', {'form': SubForm(), 'sub': sub, 'city': city_name, 'notify': notify,
                                              'data': data.text})


def loggout(request):
    logout(request)
    return redirect('home')
