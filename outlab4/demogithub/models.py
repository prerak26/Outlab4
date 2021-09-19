from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model, ModelStateFieldsCacheDescriptor
from django.db.models.signals import post_save
import requests
from requests.api import request
from Scripts.fetch_info import search_for_profiles, search_for_repos
from slugify import slugify

# Create your models here.
class Profile(models.Model):
    """Models the information to be stored of a person"""
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=50,null=True)
    slug = models.SlugField(max_length=200,null=True)
    last_name = models.CharField(max_length=50,null=True)
    followers = models.IntegerField(null=True)
    last_updated = models.DateTimeField(null=True)
    
    def __str__(self):
        return str(self.name)


def create_profile(sender,instance,created,**kwargs):
    if created:
        new_user=Profile.objects.create(user=instance)
        temp_user_name= instance.username 
        new_user.name = instance.first_name
        new_user.user_name = temp_user_name
        new_user.last_name = instance.last_name
        new_user.slug = slugify(temp_user_name)
        bahutsare,time_which=search_for_profiles(temp_user_name)
        new_user.followers = bahutsare
        new_user.last_updated = time_which
        

        repos=search_for_repos(temp_user_name)
        for repo in repos:
            new_repo = Repository.objects.create(name=repo[0],owner=new_user)
            new_repo.stars = repo[1]
            new_repo.save()
        new_user.save()
post_save.connect(create_profile,sender=User)

class Repository(models.Model):
    """Models the repositories to its users"""
    name = models.CharField(max_length=100,null=True)
    stars = models.IntegerField(default=0,null=True)
    
    """As one Owner may have multiple repositories"""
    owner = models.ForeignKey('Profile',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.name)
