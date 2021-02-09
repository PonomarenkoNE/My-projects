from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('image')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    username = models.ForeignKey(Profile, related_name='posted_by', on_delete=models.CASCADE)
    photo = CloudinaryField('image')
    text = models.TextField()
    date = models.DateTimeField()
    like_num = models.IntegerField(default=0)
    dislike_num = models.IntegerField(default=0)


class LikeDislike(models.Model):
    user = models.ForeignKey(Profile, related_name='who_like_dislike', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='what_like_dislike', on_delete=models.CASCADE)
    likes = models.BooleanField()
    dislikes = models.BooleanField()


class FolloweFollowing(models.Model):
    username = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(Profile, related_name="followed", on_delete=models.CASCADE)


