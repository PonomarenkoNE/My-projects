from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('/home', views.home, name='home'),
    path('/registration', views.register, name='registration'),
    path('/profile', views.profile, name='profile'),
    path('logout', views.loggout, name='logout'),
    path('/addcity', views.add_city, name='addcity'),
    path('/city/<name>/', views.city, name='city')
]
