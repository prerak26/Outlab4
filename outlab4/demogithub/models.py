from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model, ModelStateFieldsCacheDescriptor
from django.db.models.signals import post_save
# Create your models here.
class Profile(models.Model):
    """Models the information to be stored of a person"""
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    followers = models.IntegerField(null=True)
    # last_updated = models.DateTimeField()
    
    def __str__(self):
        return self.name

def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)

class Repository(models.Model):
    """Models the repositories to its users"""
    name = models.CharField(max_length=100)
    stars = models.IntegerField(default=0)
    
    """As one Owner may have multiple repositories"""
    owner = models.ForeignKey('Profile',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
