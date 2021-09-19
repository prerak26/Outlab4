from django.contrib import admin
from demogithub.models import Profile, Repository

# Register your models here.
admin.site.register(Profile)
admin.site.register(Repository)