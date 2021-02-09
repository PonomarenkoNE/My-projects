from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('home', views.home, name='home'),
    path('registration', views.register, name='registration'),
    path('profile/<name>/', views.profile, name='profile'),
    path('profile', views.profile2, name='profile2'),
    path('addpost', views.add_post, name='addpost'),
    path('posts', views.all_posts, name='posts'),
    path('logout', views.loggout, name='logout'),
    path('myfeed', views.feed, name='myfeed'),
    path('like/<what>/', views.like, name='like'),
    path('dislike/<what>/', views.dislike, name='dislike')
]
