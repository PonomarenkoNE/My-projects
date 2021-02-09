from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import City, Subscribe


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ['url', 'name']


class SubscribeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['url', 'follower', 'following', 'notification_period']
